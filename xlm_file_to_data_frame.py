import pandas as pd
from get_relevant_paths import GetRelevantPaths as grp
from f13_download import FileDownload as fd


class XlmFileToDataFrame:

    def __init__(self, dict_with_cik_and_path: dict):
        self.dict_with_cik_and_path = dict_with_cik_and_path

    @staticmethod
    def __bring_xlm_file_in_correct_format(text: str) -> str:
        return text[text.rfind('<?xml version="1.0"'): text.find('informationTable>') + len('informationTable>')]

    def __parse(self, cik: str, filing_type: str):
        results_df = []
        for path in self.dict_with_cik_and_path[cik][filing_type]:
            with open(path) as f:
                text = f.read()
            text = self.__bring_xlm_file_in_correct_format(text)
            try:
                df = pd.read_xml(text)
            except:
                continue
            date = self.__extract_date_from_path(path)
            df = pd.concat([
                df[['cusip', 'value']],
                pd.DataFrame([date] * len(df), columns=['fdate']),
                pd.DataFrame([filing_type] * len(df), columns=['filetype'])
            ], axis=1)

            results_df.append(df)
        return pd.concat(results_df, ignore_index=True) if len(results_df) > 0 else None

    def __save_cik_holding_dfs(self, data_frame: pd.DataFrame, cik: str) -> None:
        path        = self.dict_with_cik_and_path[cik][list(self.dict_with_cik_and_path[cik])[0]][0]
        saving_path = f'{path[:path.find(cik) + len(cik)]}/{cik}_holdings.json'
        data_frame.to_json(saving_path)

    @staticmethod
    def __extract_date_from_path(path: str) -> str:
        path = f'{path[:-len("/full-submission.txt")]}/filing-details.xml'
        with open(path) as f:
            text_with_date = f.read()

        start               = text_with_date.find('<periodOfReport>')+len('<periodOfReport>')
        end                 = text_with_date.find('<', start)
        month, day, year    = text_with_date[start:end].split('-')

        day     = day if len(day) == 2 else f'0{day}'
        moth    = month if len(month) == 2 else f'0{month}'
        year    = year if len(year) == 4 else f'00{year}'

        return f'{year}{month}{day}'


    def main(self) -> None:
        ciks = list(self.dict_with_cik_and_path.keys())

        for cik in ciks:
            filing_types                = list(self.dict_with_cik_and_path[cik].keys())
            holdings_per_filing_type    = []
            for filing_type in filing_types:
                df0 = self.__parse(cik, filing_type)
                if df0 is not None:
                    holdings_per_filing_type.append(pd.concat([pd.DataFrame([cik]*len(df0), columns=['cik']), df0], axis=1))
            if len(holdings_per_filing_type) > 0:
                df = pd.concat(holdings_per_filing_type, axis=0, ignore_index=True)
                self.__save_cik_holding_dfs(df, cik)
            fd.write_list(list(grp.get_done_ciks_for_holdings_df()) + [cik], 'done_ciks_for_holdings_df.txt')
            print(f'{cik} Done!')
