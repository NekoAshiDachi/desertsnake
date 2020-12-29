import pandas
import re
import nltk
from typing import List, Dict

from cov_parser.webscrape import logger
from cov_parser.create_docs import Sec_Doc
from cov_parser.train import Labeled_String, get_most_common, extract_ngram_features, train_naive_bayes


class CovModel:

    def __init__(self, df_true: pandas.DataFrame, df_all: pandas.DataFrame, cov: str):
        most_common_titles = get_most_common(df_true[f'{cov}_title'].dropna().values)
        # most_common_first = get_most_common(df_true[f'{cov}_first'].dropna().values)[:2]  # excludes unigrams

        df_false = df_all[['title', 'first']].dropna()
        df_false = df_false.loc[df_false.title.apply(
            lambda title: set(extract_ngram_features(title, most_common_titles).values())) == {False}]

        df_false = df_false.append([
            df_true.filter(regex=f'{false_cov}_(title|first)')
                .dropna(how='all').rename(columns=lambda x: x.replace(f"{cov}_", ''))
                for false_cov in re.findall(f'~([\\w+\\s*]+)(?<!{cov})_title', '~'.join(df_true.columns))])

        title_labeled_strings, first_labeled_strings = [
            [Labeled_String((text, False)) for text in df_false[title_first].dropna().values] +
            [Labeled_String((text, True)) for text in df_true[f'{cov}_{title_first}'].dropna().values]
            for title_first in ('title', 'first')]

        self.name = cov
        self.df_false = df_false
        self.most_common_title, self.title = train_naive_bayes(labeled_strings=title_labeled_strings)
        self.most_common_first, self.first = train_naive_bayes(labeled_strings=first_labeled_strings)

    def classify(self, title_or_first: str, classified: str) -> bool:
        return getattr(self, title_or_first) \
            .classify(extract_ngram_features(classified, getattr(self, f'most_common_{title_or_first}')))

    def classify_probability(self, title_or_first: str, classified: str) -> float:
        return getattr(self, title_or_first) \
            .prob_classify(extract_ngram_features(classified, getattr(self, f'most_common_{title_or_first}'))) \
            .prob(True)

    def find_cov(self, sec_doc: Sec_Doc) -> List[Dict]:

        matches = nltk.defaultdict(lambda: {})
        for section in sec_doc.sections.values():
            if section['title'] and self.classify('title', section['title'][0]):
                prob = self.classify_probability('title', section['title'][0])
                matches[section['title'][0]].update(prob={'title': prob})
            if section['first'] and self.classify('first', section['first'][0]):
                prob = self.classify_probability('first', section['first'][0])
                m = matches[section['title'][0]]
                m['prob'].update({'first': prob}) if 'prob' in m else m.update(prob={'first': prob})

        if matches:
            # add section data, and probability sum and string, to each match in matches dict
            [matches[s['title'][0]].update(s) for s in sec_doc.sections.values() if
             s['title'] and s['title'][0] in matches]

            [m['prob'].update(sum=sum(m['prob'].values())) for m in matches.values()]

            [m['prob'].update(string=', '.join(
                [f"{p} - {round(p_n, 4)}" for p, p_n in m['prob'].items()])) for m in matches.values()]

            # max_sum = max(map(lambda x: x['prob']['sum'], matches.values()))
            # match = {k: v for k, v in matches.items() if v['prob']['sum'] == max_sum}  # may be >1 match to max sum

            # ordered list of matches by descending probability
            matches = [matches[m] for m in sorted(matches, key=lambda m: matches[m]['prob']['sum'], reverse=True)]

            logger.info(f"\t{self.name}:\n\t\t" + f'\n\t\t'.join([
                f"{n + 1}. {m['title'][0].strip()}: " + m['prob']['string'] for n, m in enumerate(matches)]))

            return matches

        logger.info('\tNo match found in title or first.')

    def __repr__(self):
        return f"<{self.name} CovModel>"


class CovModels:
    def __init__(self, df_true: pandas.DataFrame, df_all: pandas.DataFrame):
        self.df_true, self.df_all = df_true, df_all
        self.cov_names = ('Debt', 'Liens', 'RP', 'Asset Sales')

        self.models = [CovModel(self.df_true, self.df_all, cov) for cov in self.cov_names]
        [setattr(self, f"model_{cov.name.lower()}", cov) for cov in self.models]

    def find_covs(self, sec_doc: Sec_Doc):
        logger.info(f"Matching by summed probabilities in descending order:")
        covs = [model.find_cov(sec_doc) for model in self.models]

        logger.info('Classification finished.')
        return covs
