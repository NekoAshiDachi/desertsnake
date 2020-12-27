from application.scripts.cov_parser.process_CAs import *
from application.scripts.cov_parser.train import *


def quick_model(df_true: pandas.DataFrame, df_all: pandas.DataFrame, cov: str) -> Dict:

    most_common_titles = get_most_common(df_true[f'{cov}_title'].dropna().values)
    # most_common_first = get_most_common(df_true[f'{cov}_first'].dropna().values)[:2]  # excludes unigrams

    df_false = df_all.loc[(
        df_all[['title', 'first']].notnull().all(axis=1) &
        ~df_all.title.dropna().apply(
            lambda x: True if True in extract_ngram_features(x, most_common_titles).values() else False)
    )][['title', 'first']]

    df_false = df_false.append([pandas.DataFrame(
        df_true[[f'{cov}_title', f'{cov}_first']].dropna(how='all').rename(columns=lambda x: x.replace(f"{cov}_", '')))
        for cov in {re.sub(r'_.*', '', cov) for cov in df_true.filter(regex=f'(?<!{cov}_)((title)|(first))').columns} ])

    most_common_title, model_title = train_naive_bayes(labeled_strings= \
        [Labeled_String((text, False)) for text in df_false.title.dropna().values] + \
        [Labeled_String((text, True)) for text in df_true[f'{cov}_title'].dropna().values])

    most_common_first, model_first = train_naive_bayes(labeled_strings= \
        [Labeled_String((text, False)) for text in df_false['first'].dropna().values] + \
        [Labeled_String((text, True)) for text in df_true[f'{cov}_first'].dropna().values])

    model_dicts = dict({'most_common_title': most_common_title, 'model_title': model_title,
                 'most_common_first': most_common_first, 'model_first': model_first})

    pickle.dump(model_dicts, open(edgar_filings(f"model_dicts"), 'wb'))
    return model_dicts


def find_cov(sec_doc: Sec_Doc, model_dict: Dict) -> List[Dict]:
    # finds single covenant as passed to model_dict arg

    most_common_title, model_title, most_common_first, model_first = \
        model_dict['most_common_title'], model_dict['model_title'], \
        model_dict['most_common_first'], model_dict['model_first']

    matches = nltk.defaultdict(lambda: 0)
    for section in sec_doc.sections.values():
        if section['title'] and model_title.classify(extract_ngram_features(section['title'][0], most_common_title)):
            matches[section['title'][0]] += model_title.prob_classify(
                extract_ngram_features(section['title'][0], most_common_title)).prob(True)
        if section['first'] and model_first.classify(extract_ngram_features(section['first'][0], most_common_first)):
            matches[section['title'][0]] += model_first.prob_classify(
                extract_ngram_features(section['first'][0], most_common_title)).prob(True)

    matched_title = {k: v for k, v in matches.items() if v == max(matches.values())}
    matched = [i for i in sec_doc.sections.values() if i['title'] and i['title'][0] in matched_title]

    if matched:
        logger.info(f"\tMatched: {matched_title}")
        return matched

    logger.info('No match found in title or first.')


def find_covs(sec_doc: Sec_Doc, model_dicts: Dict[str, Dict]):
    # finds all covenant types within model_dicts
    results_dict = nltk.defaultdict(None)

    logger.info(f"Matching by maximum summed probabilities.")
    for cov_name, cov_dict in model_dicts.items():
        logger.info(f"{cov_name}:")
        results_dict.update({cov_name: find_cov(sec_doc, cov_dict)})
        firsts = '\n'.join([f"\t{results_dict[cov_name][n]['first'][0]}" for n in range(len(results_dict[cov_name]))])
        logger.info(f"\tFirst: {firsts}")

    logger.info('Classification finished.')
    return results_dict
