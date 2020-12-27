from application.scripts.cov_parser.create_docs import *
import pandas
import numpy


# FIND TRUE CREDIT AGREEMENTS ==========================================================================================

def get_true_CA_Docs(credit_df: pandas.DataFrame, year: int) -> List[Doc]:

    logger.info('Getting URLs and creating Docs from CA title DataFrame.')

    sys.setrecursionlimit(10000)

    pickle_name = f"true_CA_Docs_from_df_{year}"
    pickled_Docs = get_pickle(edgar_filings(pickle_name))

    for n, CA in enumerate(credit_df.Link.dropna().drop_duplicates()):
        if CA in [i.url for i in pickled_Docs]:
            continue

        logger.info(f'{n} {CA}')

        pickled_Docs.append(Doc(CA))
        pickle.dump(pickled_Docs, open(edgar_filings(pickle_name), 'wb'))
        pickled_Docs = get_pickle(edgar_filings(pickle_name))

    logger.info(f'{len(pickled_Docs)} Docs from CA title DataFrame retrieved.\n')

    return pickled_Docs


def get_CAs(exhibit_Docs: List[Doc]) -> Tuple[ List[Doc], List[Doc] ]:

    logger.info('Getting true and false CAs from exhibits.')

    true_CA_Docs = [D for D in exhibit_Docs
        if re.search(r"""
            (?<!(CONVERTIBLE)\s)
            ((TERM\s*[A-z0-9]*\s*LOAN\s*[A-z0-9]*\s*)|(CREDIT)|(LOAN))\s*
            (AND\s*((SECURITY)|(GUARANTY))\s*)?
            AGREEMENT""", '\n'.join(D.header), re.I | re.VERBOSE) and \
            not re.search(r"AMENDMENT.*?TO.*?AGREEMENT", '\n'.join(D.header), re.I | re.DOTALL)]

    false_CA_Docs = [D for D in exhibit_Docs if D.url not in [ca.url for ca in true_CA_Docs]]

    logger.info(f'\t{len(true_CA_Docs)} true and {len(false_CA_Docs)} false CAs found.\n')

    get_pickle(edgar_filings('true_exhibit_Docs'))
    pickle.dump(true_CA_Docs, open(edgar_filings('true_exhibit_Docs'), 'wb'))

    return true_CA_Docs, false_CA_Docs


# PREP TRUE CA DATAFRAME ===============================================================================================


def prep_true_cov_df(ods_path: str) -> pandas.DataFrame:

    logger.info(f'Creating CA title DataFrame from {ods_path}.')
    df_true = pandas.read_excel(ods_path)

    df_true = df_true.assign(**{k: v for cov in ['Debt', 'Liens', 'RP', 'Asset Sales'] for k, v in {
        f'{cov}_title': df_true[cov].str.extract(r'^[A-z\s]*[0-9.]*\s*([\sA-z,;]+)(?:(?:\.)|(?:\n))'),
        f'{cov}_first': df_true[cov].str.extract(r"""
            ^[A-z\s]*[0-9.]*\s*             # section number
            [\sA-z,;]+(?:(?:\.)|(?:\n))\s*  # section name
            (.*?)(?:(?:(?:except)?[.:])|(?:provided,*(?:\s*\w+,*)?\s*that)|(?:not(?: \w+)? exce[eds]{2}))(.*)
            """, flags=re.VERBOSE).iloc[:, 0]}.items()})

    df_true = df_true.assign(**{
        col: df_true[col].apply(
            lambda x: x[0] if type(x) in [tuple] else x) for col in df_true.filter(regex='first')})

    return df_true


# PREP ALL COV DATAFRAME -----------------------------------------------------------------------------------------------


def prep_all_cov_df(sec_docs: List[Sec_Doc]) -> pandas.DataFrame:
    df_all = pandas.DataFrame.from_records({k: v for sec_doc in sec_docs for k, v in sec_doc.sections.items()})
    df_all = df_all.T.reset_index().drop('index', axis=1)

    df_all.title = df_all.title.apply(lambda x: x[0] if len(x) >= 1 else numpy.NaN)
    df_all['first'] = df_all['first'].apply(lambda x: x[0] if len(x) >= 1 else numpy.NaN)

    return df_all
