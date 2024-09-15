'''Main code'''
from infrastructure.file_downloader import FileDownloader
from infrastructure.pdf_generator import PdfCreator
from infrastructure.file_manager import read_queue
from infrastructure.my_logger import get_logger
from feature.manga_strategy.manga_factory import MangaFactory
from feature.manga_strategy.manga_scrapper_context import MangaScraper

_logger = get_logger(__name__)

def main():
  download_queue = read_queue()

  for item in download_queue:
    manga_url = item[0]
    folder_name = item[1]
    page_number = item[2]
    pdf_name = item[3]
    print("*************************************************")
    strategy = MangaFactory.get_manga_strategy(manga_url)
    scrapper = MangaScraper(strategy)

    folder_manager = FileDownloader(f"../{folder_name}")
    folder_manager.create_folder_if_not_exist()

    if manga_url is not None:
      run_manga_downloader(
        scrapper,
        folder_manager,
        folder_name,
        manga_url,
        page_number)

    if pdf_name is not None:
      create_pdf(folder_manager, pdf_name)

  return

def run_manga_downloader(
    scrapper: MangaScraper,
    folder_manager: FileDownloader,
    folder_name: str,
    url: str,
    page_number:int):
  
  _logger.info("Start manga download for [%s]", folder_name)
  error_by_manga = scrapper.run_manga_download_async(
    folder_manager, page_number)

  if len(error_by_manga) > 0:
    print(f"Error in these images from [{url}]", error_by_manga)

  _logger.info("End manga download for [%s]", folder_name)

def create_pdf(folder_manager: FileDownloader, pdf_name:str):
  pdf_creator = PdfCreator(folder_manager, pdf_name)
  pdf_creator.create_pdf()
  pass
  

if __name__ == "__main__":
  main()
