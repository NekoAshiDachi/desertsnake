from datetime import datetime
from application.scripts.cov_parser.find_covs import *

# ALL 4 or 10 EXHIBITS -------------------------------------------------------------------------------------------------

# scrape EDGAR for CAs
year = datetime.now().year
qtrn = 'QTR' + str(round(datetime.now().month / 4 + 1))
index_n = 1

# Filings created from https://www.sec.gov/Archives/edgar/full-index//2019/QTR1/sitemap.quarterlyindex1.xml;
# everything following, include model, are based on these filings.
Filings = get_pickle(edgar_filings(f'Filings_{year}_{qtrn}_{index_n}'))
if not Filings:
    Filings = get_filings_from_full_index(year, qtrn, index_n)

# get URLs of exhibit type 4 or 10
exhibit_urls = get_exhibits(
    Filings, exhibits_path=edgar_filings(f'URLs - Ex 4, 10 - {year} {qtrn} {index_n}'), exhibit_types=[4, 10])

# get Docs
exhibit_Docs = get_filings(file_path=edgar_filings('exhibit_Docs_2019'), url_list=exhibit_urls, class_type=Doc)
exhibit_true_Docs, exhibit_false_Docs = get_CAs(exhibit_Docs)

# TRUE CREDIT AGREEMENTS -----------------------------------------------------------------------------------------------

# create true CA df
df_true = prep_true_cov_df('./application/scripts/cov_parser/true_credit_docs.ods')

for url in [i.url for i in exhibit_true_Docs]:
    df_true = df_true.append({'Link': url}, ignore_index=True)

# create/get true CA Docs; 53 total
true_Docs = get_filings(file_path=edgar_filings('true_df_Docs'), url_list=df_true.Link.dropna(), class_type=Doc)

true_Sec_Docs = get_filings(
    file_path=edgar_filings('true_df_Sec_Docs'), url_list=df_true.Link.dropna(), class_type=Sec_Doc)  # 73 total

# create all cov df
df_all = prep_all_cov_df(true_Sec_Docs)

# find covs
model_dicts = {cov: quick_model(df_true, df_all, cov) for cov in ('Debt', 'Liens', 'RP', 'Asset Sales')}

# ----------------------------------------------------------------------------------------------------------------------

# final: create Flask page in which URL can be submitted and return with source data
