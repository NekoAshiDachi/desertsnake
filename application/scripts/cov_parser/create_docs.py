import sys
import pickle
import re
import bs4
import webbrowser
from datetime import datetime
from unidecode import unidecode
from typing import List, Callable, Union

from cov_parser.webscrape import logger, URL, request_soup, get_pickle, edgar_filings, Filing, \
    get_filings_from_full_index, get_exhibits


# ======================================================================================================================

def unidecode_strip_tags(tags, stripped_tags):

    def unidecode_strip(string: str) -> str:
        return re.sub(r'\s+', ' ', unidecode(string)).strip()

    for tag in tags:
        if isinstance(tag, bs4.Tag) and unidecode_strip(tag.text):
            stripped_tags = unidecode_strip_tags(tag.contents, stripped_tags)
        elif isinstance(tag, bs4.NavigableString) and unidecode_strip(tag):
            stripped_tags.append(unidecode_strip(tag))

    return stripped_tags


def get_idx_by_tag(text, css_selector: Callable, start_idx: int=0) -> int:

    anchor_tag = text.find(css_selector)

    if not anchor_tag:
        return start_idx + 1

    while anchor_tag.parent.name != 'text':
        anchor_tag = anchor_tag.parent

    idx = None
    for n, i in enumerate(text.contents[start_idx:]):
        if i == anchor_tag:
            idx = n + start_idx
            break

    return idx


def get_idx_by_regex(text: List, pattern: str) -> int:

    section_key = re.findall(r'((?:section\s*)?\w*\d+\.\d*\.*\s*.*$)', pattern, re.I | re.DOTALL)[0]
    # logger.info(f"\t{section_key}")

    idx = [n for n, i in enumerate(text)
           if type(i) in [str, bs4.NavigableString] and re.search(pattern + r'\b', i, re.I | re.DOTALL)]

    if not idx:
        pattern_split = re.findall(r'((?:section\s*)?\d+\.\d*\.*)\s*(.*$)', pattern, re.I | re.DOTALL)
        label, header = pattern_split[0] if pattern_split else (pattern, None)
        idx = [n for n, i in enumerate(text)
               if re.search(f"^\s*\\b{label}\\b(?!\()", text[n], re.I) and
               re.search(f"^\s*{label}[.\s]*{header}", ''.join(text[n: n + 10]), re.I | re.DOTALL)]

    def check_strings(section_key, n):

        def strip_chars(string): return ''.join(re.findall(r'\w', string))

        if re.search('^(section)?' + strip_chars(section_key), strip_chars(''.join(text[n: n + 10])),
            flags=re.I | re.DOTALL):

            return n

    if not idx:
        idx = [n for n, i in enumerate(text) if check_strings(section_key, n) and not re.search('^\W', text[n])]

    return min(idx) if idx else logger.info(f"\tPattern not found: {pattern}")


# DOC CLASSES ==========================================================================================================


class Doc:
    def __init__(self, url: URL):
        """
        Organizes URL's bs4 data as header, table of contents, paragraph objects, and more. Does not have tags in
        attributes since tags do not pickle.
        """

        soup = request_soup(url)
        text = soup.find('text')

        logger.info(f'Contents: {len(list(text.contents))}')
        logger.info(f'Descendants: {len(list(text.descendants))}')

        witnesseth_lambda = lambda t: \
            type(t.next_element) == bs4.NavigableString and t.next_element.strip() and \
            re.search('(IN WITNESS WHEREOF)|(parties hereto.*?agreement.*?duly executed.*?above)', t.next_element, re.I)

        if not text.find(witnesseth_lambda):
            witnesseth_lambda = lambda t: \
                type(t.next_element) == bs4.NavigableString and t.next_element.strip() and \
                re.search('signature.*?((begin)|(follow))', t.next_element, re.I)

        post_witnesseth = [
            t for t in text.find(witnesseth_lambda).find_all_next()] if text.find(witnesseth_lambda) else []

        logger.info(f"Decomposing {len(post_witnesseth)} post-witnesseth tags.")
        [t.decompose() for t in text.find(witnesseth_lambda).find_all_next()] if post_witnesseth else None

        logger.info(f"\tUnwrapping {len(text.find_all('center'))} <center>.")
        while text.find('center'):
            text.center.unwrap()

        # remove tags with only '\n' value
        [blank.extract() for blank in
         [i for i in text.descendants if (type(i) == bs4.Tag and not i.text.strip())
          or (type(i) == bs4.NavigableString and not i.strip())]]

        div_lambda = lambda t: t.name == 'div' and not [
            i for i in t.contents if type(i) == bs4.NavigableString or i.name in ['u', 'table', 'tr', 'font']]

        logger.info(f"\tUnwrapping {len(text.find_all(div_lambda))} <div> indirect to NavStrings.")
        [t.unwrap() for t in text.find_all(div_lambda)]

        # HEADER -------------------------------------------------------------------------------------------------------

        logger.info('Finding indices:')

        header_start = lambda t: \
            t.text and re.search(r'\w+', t.text) and re.search(
                'center', ';'.join([','.join(v) if type(v) == list else v for v in t.attrs.values()]), re.I)

        header_idx = get_idx_by_tag(text, css_selector=header_start)

        logger.info(f'\tHeader idx: {header_idx}')

        # ToC ----------------------------------------------------------------------------------------------------------

        toc_lambda = lambda t: \
            t.text and re.search(r'(((contents*)|((?<!/)index))|(^\s*article)\s*$)', t.text, re.I) and \
            not re.search('^h\d', t.name, re.I) and \
            not re.search('h\d', ';'.join([','.join(i.name) if type(i) == list else i.name for i in t.parents]))

        not_center_lambda = lambda t: \
            not re.search('center', ';'.join([','.join(v) if type(v) == list else v for v in t.attrs.values()]), re.I) \
            and t.find_previous_sibling(header_start)

        toc_idx = get_idx_by_tag(text, css_selector=toc_lambda, start_idx=header_idx)

        if not toc_idx or toc_idx > len(text.contents) * 0.1:
            toc_idx = get_idx_by_tag(text, css_selector=not_center_lambda, start_idx=header_idx)

        if toc_idx > len(text.contents) * 0.1:
            toc_idx = header_idx + 1

        logger.info(f'\tToC idx: {toc_idx}')

        # BODY ---------------------------------------------------------------------------------------------------------

        body_toc_lambda = lambda t: \
            t.text and not re.search(r'CUSIP|000', t.text) and t.find_previous_sibling(toc_lambda) and \
            re.search("""((?:
                (?:(?<!letters of )CREDIT(?!or))|(?:(TERM\\s*)?LOAN))   # credit | term loan
                (\\s+\\w+\\s+\\w+)?                                     # x x
                \\s*AGREEMENT.*?(?:(?:dated)|(?:entered)))              # agreement dated | entered              
                """, t.text, re.I | re.VERBOSE)

        body_idx = get_idx_by_tag(text, body_toc_lambda, toc_idx)

        body_toc_lambda = lambda t: \
            t.text and t.find_previous_sibling(toc_lambda) and \
            re.search("(?:(?:(?<!letters of )CREDIT(?!or))|(?:(TERM\\s*)?LOAN))\s*AGREEMENT", t.text, re.I)

        body_idx = get_idx_by_tag(text, body_toc_lambda, toc_idx) \
            if (len(''.join(unidecode_strip_tags(text.contents[:body_idx], []))) >
                len(''.join(unidecode_strip_tags(text.contents[body_idx:], []))) * .1) \
            else body_idx

        logger.info(f'\tBody idx found: {body_idx}\n')

        header = unidecode_strip_tags(text.contents[header_idx: toc_idx], [])
        toc = unidecode_strip_tags(text.contents[toc_idx: body_idx], [])
        body = unidecode_strip_tags(text.contents[body_idx:], [])

        self.url, self.header, self.toc, self.body = url, header, toc, body
        self.idx = {'header': header_idx, 'toc': toc_idx, 'body': body_idx}

        self.form_8k = [i for i in self.header if re.search('form\s8-k', i, re.I)] != []

    def open_url(self):
        webbrowser.open(self.url)


class Sec_Doc(Doc):

    def __init__(self, url: URL):
        Doc.__init__(self, url)
        toc, body = self.toc, self.body
        logger.info('Doc instantiated for url %s' % url)

        # toc list -> '\n'.join(toc); rejects e.g., "Updated Schedules"
        toc_match = re.findall(r"(^.*?)(?<![a-z] )((?:(?:schedule)|(?:exhibit)).*)", '\n'.join(toc), re.I | re.DOTALL)
        toc, schedules = toc_match[0] if toc_match and len(toc_match[0]) == 2 else ('\n'.join(toc), None)

        toc_sections = [
            i.strip().replace('\n', ' ') for i in re.findall(r"""
                ((?:section)?\s*\w*\d+\.(?![A-z])\d*\.*\d*\.*    # (Section) X.X(.X)
                \s[ A-z,;\-'\[\]]+)\n*\d*      # header""", toc, re.I | re.DOTALL | re.VERBOSE)]

        # sections = {
        #     section_key: {'body': [i.replace('\n', ' ') for i in body[
        #         get_idx_by_regex(body, f"^\\s*" + re.sub('([\[\]])', r'\\\1', section_key)):
        #         get_idx_by_regex(body, f"^\\s*" + re.sub('([\[\]])', r'\\\1', toc_sections[n + 1])) \
        #             if n != len(toc_sections) - 1 else -2] ]}
        #     for n, section_key in enumerate(toc_sections)}

        sections = {}
        def idx_regex(toc_list): return get_idx_by_regex(body, f"^\\s*" + re.sub('([\[\]])', r'\\\1', toc_list))

        for n, section_key in enumerate(toc_sections):
            section_end = idx_regex(toc_sections[n + 1]) if n != len(toc_sections) - 1 else -2
            section = body[idx_regex(section_key): section_end]
            sections.update({section_key: {'body': [i.replace('\n', ' ') for i in section]}})

        logger.info('\n'.join(f"\t{s}" for s in sections))

        [sections[k].update({
            'title': re.findall(r"""
                ^[A-z\s]*                           # section label
                [0-9.]*\s*                          # section number
                ([\sA-z,;:\-']+)                     # section name
                (?:(?:[.\]])|(?:\n))                # ends with . or line break
                """, string='\n'.join(sections[k]['body']), flags=re.I | re.DOTALL | re.VERBOSE),
            'first': re.findall(r"""
                ^[A-z\s]*[0-9.]*\s*[\sA-z,;:\-']+    # section title
                (?:(?:[.\]])|(?:\n))\s*             # end of section title with . or line break
                (.*?)                               # matched group: first general clause
                (?:(?:(?:except)?[.:])|(?:provided,*(?:\s*\w+,*)?\s*that)|(?:not(?: \w+)? exce[eds]{2}))
                """, string='\n'.join(sections[k]['body']), flags=re.DOTALL | re.VERBOSE)})
            for k in sections]

        self.sections = sections

        if not toc_sections:
            logger.info('No table of contents.')
        else:
            logger.info(f"Missing titles: {[i for i in self.sections if not self.sections[i]['title']]}")
            logger.info(f"Missing firsts: {[i for i in self.sections if not self.sections[i]['first']]}")

        logger.info('Sec_Doc initialization inished.\n')

    def report(self):
        logger.info('Missing title:')
        logger.info('\t', [i for i in self.sections if not self.sections[i]['title']])

        logger.info('Missing first:')
        logger.info('\t', [i for i in self.sections if not self.sections[i]['first']])


# ======================================================================================================================


def get_filings(file_path: str, url_list: List[URL], class_type=Union[Filing, Doc, Sec_Doc]) \
        -> List[Union[Filing, Doc, Sec_Doc]]:

    logger.info(
        f"Loading {file_path}: updating pickled {class_type.__name__}s.")

    sys.setrecursionlimit(10000)

    pickled_filings = get_pickle(file_path)

    for filing_n, filing_url in enumerate(url_list):

        if filing_url not in [i.url for i in pickled_filings]:
            logger.info(f'\t{filing_n}/{len(url_list)} {filing_url}')

            new_filing = class_type(filing_url)
            pickled_filings.append(new_filing)

            pickle.dump(pickled_filings, open(file_path, 'wb'))
            pickled_filings = get_pickle(file_path)

        # if filing_n == 0 or not filing_n % 1000:
        #     logger.info(f'\t\tURL list completed: {filing_n}')

    logger.info(f'\t\tPickled filings total: {len(pickled_filings)}')

    return pickled_filings


def create_exhibit_filings(year: int = datetime.now().year, qtrn:str = 'QTR' + str(round(datetime.now().month / 4 + 1)),
                   index_n: int = 1) -> List[Doc]:

    # scrape EDGAR for CAs and create Filing objects
    filings = get_pickle(edgar_filings(f'Filings_{year}_{qtrn}_{index_n}'))
    if not filings:
        filings = get_filings_from_full_index(year, qtrn, index_n)

    # get exhibit type 4 or 10 URLs
    exhibit_urls = get_exhibits(
        filings, exhibits_path=edgar_filings(f'URLs - Ex 4, 10 - {year} {qtrn} {index_n}'), exhibit_types=[4, 10])

    # get Docs for exhibit URLs
    exhibit_docs = get_pickle(edgar_filings(f'exhibit_Docs_{year}'))
    if not exhibit_docs:
        exhibit_docs = get_filings(
            file_path=edgar_filings(f'exhibit_Docs_{year}'), url_list=exhibit_urls, class_type=Doc)

    return exhibit_docs


# ======================================================================================================================
