import os
import pickle

if os.path.basename(os.getcwd()) != 'desertsnake':
    os.chdir(os.path.join(os.path.expanduser('~'), 'Coding', 'desertsnake'))

from cov_parser.webscrape import URL, edgar_filings
from cov_parser.create_docs import Sec_Doc
from cov_parser.process_CAs import create_df_true_all
from cov_parser.find_covs import CovModels


def get_client_covs(doc_url: URL) -> dict:
    # clears log file
    with open('./application/static/logs/covparser.log', 'w'):
        pass

    sec_doc = Sec_Doc(doc_url)
    covenants = pickle.load(open(edgar_filings('CovModels'), 'rb'))
    covenants = covenants.find_covs(sec_doc)
    return covenants


if __name__ == '__main__':
    df_true, df_all = create_df_true_all()  # 2019 - QTR1 - index 1 default
    models = CovModels(df_true, df_all)
    pickle.dump(models, open(edgar_filings(f"CovModels"), 'wb'))
