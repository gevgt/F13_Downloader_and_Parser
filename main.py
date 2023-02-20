from f13_download import FileDownload
from get_relevant_paths import GetRelevantPaths
from xlm_file_to_data_frame import XlmFileToDataFrame
from final_product import FinalProduct


def runner(action_index: int):
    path_to_file_dump       = '/Users/gedeonvogt/Desktop/RWTH Aachen/WHF-FiRRM/Projekte/Dokumentendownload/F13_Downloader_and_Parser/Filedump'
    path_to_holdings_dump   = '/Users/gedeonvogt/Desktop/RWTH Aachen/WHF-FiRRM/Projekte/Dokumentendownload/F13_Downloader_and_Parser/Filedump/Holdings Dump'

    # Download
    if action_index == 0:
        filing_types    = ['13F-HR', '13F-NT', '13FCONP']
        start_date      = '2017-01-01'
        FileDownload(path_to_file_dump, filing_types, start_date).download()

    # Parsing
    elif action_index == 1:
        XlmFileToDataFrame(GetRelevantPaths(path_to_file_dump).get_paths(), path_to_holdings_dump).main()

    # Final Product
    elif action_index == 2:
        FinalProduct(path_to_holdings_dump).run()


    else:
        raise Exception('Action Index Out Of Bounds. Has to be either 0, 1 or 2.')


if __name__ == '__main__':
    action_index = 0
    runner(action_index)
