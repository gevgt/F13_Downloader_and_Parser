import os
import pandas as pd

class FinalProduct:

    def __init__(self, path_to_holdings_dump):
        self.path_to_holdings_dump = path_to_holdings_dump

    def run(self):
        paths = os.listdir(self.path_to_holdings_dump)
        df = [pd.read_csv(f'{self.path_to_holdings_dump}/{path}', index_col=0) for path in paths if path.endswith('.csv')]

        df_concat = pd.concat(df[:10], axis=0, ignore_index=True)
        df_concat['cusip'] = [str(cusip) for cusip in df_concat['cusip']]
        df_concat = df_concat.sort_values(by='cusip')

        df_concat.to_csv('parsed_holdings.csv', index=False)
