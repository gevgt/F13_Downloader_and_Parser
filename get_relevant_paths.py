import os


class GetRelevantPaths:

    def __init__(self, path_to_file_dump):
        self.path_to_file_dump = path_to_file_dump

    def get_paths(self) -> dict:
        ciks            = [cik for cik in os.listdir(f'{self.path_to_file_dump}/sec-edgar-filings/') if cik[0].isnumeric() and cik not in self.get_done_ciks_for_holdings_df()]
        cik_paths_dict  = {}
        for cik in ciks:
            filing_types            = [filing_type for filing_type in os.listdir(f'{self.path_to_file_dump}/sec-edgar-filings/{cik}') if filing_type.startswith('13F')]
            filings_by_type_dict    = {}
            for filing_type in filing_types:
                path    = f'{self.path_to_file_dump}/sec-edgar-filings/{cik}/{filing_type}'
                filings = [filing for filing in os.listdir(path) if filing[0].isnumeric()]
                paths   = [f'{path}/{filing}/full-submission.txt' for filing in filings]
                filings_by_type_dict[filing_type] = paths
            cik_paths_dict[cik] = filings_by_type_dict
        return cik_paths_dict

    @staticmethod
    def get_done_ciks_for_holdings_df() -> set[str]:
        with open('done_ciks_for_holdings_df.txt') as f:
            ciks = f.read()
        done_ciks = set(ciks.split('\n'))
        if '' in done_ciks:
            done_ciks.remove('')
        return done_ciks
