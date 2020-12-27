import re
import os
import sys
import requests, bs4
import pickle
import logging

from dotenv import load_dotenv
from unidecode import unidecode
from typing import List, Tuple, NewType

# Processes up to exhibit n URLs (does not specify CAs).

# ======================================================================================================================

load_dotenv()
base_dir = os.environ['COVPARSER_BASEDIR']

logging.basicConfig(level='INFO', format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
logger = logging.getLogger('covparser')
handler = logging.FileHandler(filename='./application/static/logs/covparser.log', mode='a')
logger.addHandler(handler)

request_soup = lambda url: bs4.BeautifulSoup(requests.get(url).text, 'lxml')

URL = NewType('URL', str)
Labeled_String = NewType('Labeled_String', Tuple[str, bool])

# PICKLES ==============================================================================================================


def edgar_filings(file_name: str) -> str:
    edgar_filings_path = os.path.join(base_dir, 'edgar_filings')
    return os.path.join(edgar_filings_path, file_name)


def get_pickle(file_path: str):
    """Creates or returns pickle file."""

    directory, file = os.path.dirname(file_path), os.path.basename(file_path)
    os.makedirs(directory, exist_ok=True)

    if file not in os.listdir(directory) or os.stat(os.path.abspath(file_path)).st_size <= 0:
        pickle.dump([], open(file_path, 'wb'))

    return pickle.load(open(file_path, 'rb'))


# FILINGS ==============================================================================================================
# Company filings archived on EDGAR


class Filing:
    def __init__(self, filing_url: URL):
        """Filing object organizes meta, doc, and data sections of passed filing URL."""

        self.url = filing_url

        soup = request_soup(filing_url)

        # info
        filing_div = [i for i in soup.select('#formDiv') if i.select('.infoHead')][0]
        filing_div_headers = [i.text for i in filing_div.select('.infoHead')]
        filing_div_info = [i.text for i in filing_div.select('.info')]

        self.info = {}
        self.info.update({ filing_div_headers[n]: filing_div_info[n] for n in range(len(filing_div_headers)) })

        # docs
        doc_div = [i for i in soup.select('#formDiv') if i.table and i.table['summary'] == 'Document Format Files'][0]
        doc_div_docs = [[unidecode(i.text) for i in row.select('td') if i] for row in doc_div.select('tr')][1:]

        self.docs = {}
        for doc in doc_div_docs:
            self.docs[doc[0]] = {
                'desc': doc[1], 'file': doc[2], 'type': doc[3], 'size': doc[4],
                'url': filing_url.replace('-', '').replace('index.htm', f"/{doc[2]}") }

        # data
        data_div = [i for i in soup.select('#formDiv') if i.table and i.table['summary'] == 'Data Files']

        self.data = {}
        if data_div:

            data = [[unidecode(i.text) for i in row.select('td') if i] for row in data_div[0].select('tr')][1:]

            for datum in data:
                self.data[datum[0]] = {'desc': datum[1], 'file': datum[2], 'type': datum[3], 'size': datum[4]}


def get_filings_from_full_index(year: int, QTRN: str, index_n: int) -> List[URL]:

    logger.info(f"Scraping EDGAR {year} {QTRN} full index {index_n} and pickling filing URLs.")

    index_url = f'https://www.sec.gov/Archives/edgar/full-index//{year}/{QTRN}/sitemap.quarterlyindex{index_n}.xml'
    index_soup = request_soup(index_url)

    filings = [i.text for i in index_soup.select('loc')]
    pickle.dump(filings, open(edgar_filings(f"index_{year}_{QTRN}_{index_n}"), 'wb'))  # ensures directory exists

    return filings


def create_Filings(year: int, QTRN: str, index_n: int) -> List[Filing]:

    filings = get_pickle(edgar_filings(f"index_{year}_{QTRN}_{index_n}"))
    pickled_Filings_dir = f'Filings_{year}_{QTRN}_{index_n}'
    pickled_Filings = get_pickle(edgar_filings(f"Filings_{year}_{QTRN}_{index_n}"))

    for n, f in enumerate(filings):
        if f in [F.url for F in pickled_Filings]:
            continue

        logger.info(f'{n}/{len(filings)} {f}')

        pickled_Filings.append(Filing(f))
        pickle.dump(pickled_Filings, open(edgar_filings(pickled_Filings_dir), 'wb'))
        pickled_Filings = get_pickle(edgar_filings(pickled_Filings_dir))

    return pickled_Filings


# EXHIBITS =============================================================================================================


def get_exhibits(Filings, exhibits_path: str, exhibit_types: List) -> List[URL]:

    logger.info(f"Pickling non-XML Exhibit {','.join([str(n) for n in exhibit_types])} URLs from Filings.")

    sys.setrecursionlimit(10000)

    exhibit_n = '|'.join([f"(?:{n})" for n in exhibit_types])
    regex = f'(ex(?:hibit)?[-\s]?(?:{exhibit_n}))'

    matched_exhibit_urls = [
        URL(F.url.replace('-', '').replace('index.htm', f"/{doc['file']}"))
        for F in Filings for doc in F.docs.values()
        if (re.search(regex, doc['desc'], re.I) or re.search(regex, doc['type'], re.I))
           and not doc['file'].endswith('xml')]

    get_pickle(exhibits_path)
    pickle.dump(matched_exhibit_urls, open(os.path.abspath(exhibits_path), 'wb'))

    logger.info(
        f"\t{len(matched_exhibit_urls)} URLs for exhibit type [{', '.join(str(i) for i in exhibit_types)}] found.\n")

    return matched_exhibit_urls


# TOOLS ================================================================================================================

import webbrowser


def open_urls(urls: List[URL]):
    """Opens in browser each URL in list."""
    [webbrowser.open(i) for i in urls]