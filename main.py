from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import argparse
import os


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_book(folder_name, book_name, response):
    file_path = f"{folder_name}/{book_name}.txt"
    with open(file_path, 'wb') as file:
            file.write(response.content)


def download_image(folder_name, image_name, img_url):
    response = requests.get(img_url)
    response.raise_for_status()
    
    file_path = f"{folder_name}/{image_name}"
    with open(file_path, 'wb') as file:
            file.write(response.content)


def parse_book_page(response_page):
    soup = BeautifulSoup(response_page.text, 'lxml')

    title_tag = soup.find('td', class_='ow_px_td').find('h1')
    title_text = title_tag.text
    title_split_text = title_text.split(" :: ")
    book_name = f"{title_split_text[0].strip()}"
    book_author = f"{title_split_text[1].strip()}"

    genres = soup.select("d_book a")
    
    genres = [genre.text for genre in genres]
    comments = [
        comment_tag.find(class_="black").text 
        for comment_tag in soup.find_all(class_="texts")
    ]


    img_url = soup.find('div', class_="bookimage").find('img')['src']

    book_params = {
         "tittle": book_name,
         "autor": book_author,
         "genre": genres,
         "coments": comments,
         "img_url": img_url,
    }
    return book_params


def main():
    parser = argparse.ArgumentParser(description="программа для загрузки книг")
    parser.add_argument("--start_id",default=1, type=int, help="начальный id книги")
    parser.add_argument("--end_id",default=10, type=int, help="конечный id книги")
    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id

    book_url = "https://tululu.org/txt.php"

    folder_book_name = Path("books")
    os.makedirs(folder_book_name, exist_ok=True)

    folder_name = Path("images")
    os.makedirs(folder_name, exist_ok=True)

    for number in range(start_id, end_id):
        page_url = f"https://tululu.org/b{number}/"
        params = {
                "id":number,
            }
        try:
            book_response = requests.get(book_url, params)
            book_response.raise_for_status()
            check_for_redirect(book_response)

            response_page = requests.get(page_url)
            response_page.raise_for_status()
            check_for_redirect(response_page)
            
        except requests.exceptions.HTTPError:
            print("Такой книги нет")

        book_params = parse_book_page(response_page)

        book_name = book_params["tittle"]
        download_book(folder_book_name, book_name, book_response)

        img_url = book_params["img_url"]
        image_name = img_url.split("/")[-1]
        img_url = urljoin(page_url, img_url)
        download_image(folder_name, image_name, img_url)

        print(f"Заголовок: {book_params["tittle"]} \n Автор: {book_params["autor"]}")


if __name__ == '__main__':
     main()