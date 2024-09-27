from bs4 import BeautifulSoup
from pathlib import Path
import requests


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError()

def download_books(folder_db_name, book_name, download_response):
    file_path = f"{folder_db_name}/{book_name}.txt"

    with open(file_path, 'wb') as file:
            file.write(download_response.content)


for id in range(1, 11):
    download_page_url = f"https://tululu.org/txt.php"
    pages_book_url = f"https://tululu.org/b{id}/"

    try:
        params = {
        "id":id,
        }

        download_response = requests.get(download_page_url, params)
        download_response.raise_for_status()
        check_for_redirect(download_response)

        response_book_pages = requests.get(pages_book_url)
        soup = BeautifulSoup(response_book_pages.text, 'lxml')
        title_tag = soup.find('td', class_='ow_px_td').find('h1')
        title_text = title_tag.text
        title_split_text = title_text.split(" :: ")
        book_name = f"{title_split_text[0].strip()}"
        book_author = f"{title_split_text[1].strip()}"

        folder_db_name = Path("books_db")
        if not folder_db_name.exists():
            folder_db_name.mkdir()
        
        download_books(folder_db_name, book_name, download_response)

    except:
        print("Такой книги нет")
