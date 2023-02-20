from sec_edgar_downloader import Downloader
import time
import pandas as pd


class FileDownload:

    def __init__(self, path_to_file_dump: str, filing_types: list[str], start_date: str):
        self.dl             = Downloader(path_to_file_dump)
        self.filing_types   = filing_types
        self.start_date     = start_date
        self.cik_lookup     = self.get_cik_lookup()

    def download(self):
        ciks        = self.get_list('ciks.txt')
        done_ciks   = self.get_list('done_ciks.txt')
        todo_ciks   = set(ciks).difference(set(done_ciks))

        for cik in todo_ciks:
            for filing_type in self.filing_types:
                try:
                    self.dl.get(filing_type, cik, after=self.start_date)
                except:
                    time.sleep(1)
                    try:
                        self.dl.get(filing_type, cik, after=self.start_date)
                    except:
                        self.write_list(self.get_list('loading_errors.txt') + [f'{cik} - {filing_type}'], 'loading_errors.txt')

            done_ciks = self.get_list('done_ciks.txt') + [cik]
            self.write_list(done_ciks, 'done_ciks.txt')
            self.print_loading_percentage(cik, ciks, done_ciks)

    @staticmethod
    def get_list(path: str) -> list[str]:
        with open(path) as f:
            list_elements = f.read()
        return list_elements.split('\n')

    @staticmethod
    def write_list(liste: list[str], path: str) -> None:
        liste = [list_element for list_element in liste if len(list_element) > 0]
        with open(path, 'w') as f:
            for list_element in liste:
                f.write(f'{list_element}\n')

    @staticmethod
    def print_loading_percentage(cik: str, ciks: list[str], done_ciks: list[str]) -> None:
        len_done_ciks = len(done_ciks) - 1 if '' in done_ciks else len(done_ciks)
        print(f'{cik} - {int((len_done_ciks/len(ciks))*100)}%')

    @staticmethod
    def get_cik_lookup():
        with open('cik-lookup-data.txt', encoding = "ISO-8859-1") as f:
            lines = f.readlines()

        lines = [line[:-2] for line in lines]

        splitted_lines = []
        for line in lines:
            splitted_line = line.split(":")
            if len(splitted_line) == 2:
                splitted_lines.append(reversed(splitted_line))
            else:
                for i, letter in enumerate(line):
                    if not line[-(i + 1)].isnumeric():
                        break
                splitted_lines.append([line[:len(line)-(i+1)], line[-i:]])

        return dict(splitted_lines)

    @staticmethod
    def save_ciks_to_txt():
        with open('/Users/gedeonvogt/Desktop/RWTH Aachen/WHF-FiRRM/Projekte/Dokumentendownload/F13_Downloader_and_Parser/master', encoding="ISO-8859-1") as f:
            lines = f.readlines()

        col_names = ['cik', 'company name', 'filing', 'date', 'link']
        subset_lines = pd.DataFrame([line.split("|") for line in lines], columns=col_names)
        sl = subset_lines.loc[subset_lines['filing'].isin(['13F-HR', '13F-NT', '13FCONP'])]['cik']
        lines = list(sl)
        with open('ciks.txt', 'w') as f:
            f.writelines('\n'.join(lines))
