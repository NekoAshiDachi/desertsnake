from application.scripts.cov_parser.find_covs import URL, Sec_Doc, get_pickle, edgar_filings, find_covs

# -------------------------------------------------------------------------------------------------

# TODO PA: covparser_basedir dotenv
# TODO have table of most recent exhibit 4s and 10s that can be classified

def get_client_covs(doc_url: URL) -> dict:
    # clears log file
    with open('./application/static/logs/covparser.log', 'w'):
        pass

    sec_doc = Sec_Doc(doc_url)
    model_dicts = get_pickle(edgar_filings('model_dicts'))
    covenants = find_covs(sec_doc, model_dicts)
    return covenants

