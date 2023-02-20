import os
import pandas as pd

class FinalProduct:

    def __init__(self):
        pass

    def run(self):
        print()
        path_to_holdings_dump = '/Users/gedeonvogt/Desktop/RWTH Aachen/WHF-FiRRM/Projekte/Dokumentendownload/F13_Downloader_and_Parser/Filedump/Holdings Dump'
        paths = os.listdir(path_to_holdings_dump)
        df = [pd.read_csv(f'{path_to_holdings_dump}/{path}', index_col=0) for path in paths if path.endswith('.csv')]

        df_concat = pd.concat(df[:10], axis=0, ignore_index=True)
        df_concat['cusip'] = [str(cusip) for cusip in df_concat['cusip']]
        df_concat = df_concat.sort_values(by='cusip')

        df_concat.to_csv('parsed_holdings.csv')

        x = pd.read_csv('/Users/gedeonvogt/Downloads/scrape_parsed.csv', nrows=1000)

obj = FinalProduct().run()