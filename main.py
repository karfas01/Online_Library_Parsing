from bs4 import BeautifulSoup
from pathlib import Path
import requests


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError()

def download_books(folder_name, book_name, response):
    

    file_path = f"{folder_name}/{book_name}.txt"
    with open(file_path, 'wb') as file:
            file.write(response.content)

def download_images(folder_name, image_name, img_url):
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

    genre_tags = soup.find_all(class_="d_book")[1]
    genrs_urls = genre_tags.find_all("a")
    genrs = []
    for genre_url in genrs_urls:
        genrs.append(genre_url.text)

    comment_tags = soup.find_all(class_="texts")
    comments = []
    for comment_tag in comment_tags:
        comments.append(comment_tag.find(class_="black").text)

    img_url = soup.find('div', class_="bookimage").find('img')['src']

    book_params = {
         "tittle": book_name,
         "autor": book_author,
         "genre": genrs,
         "coments": comments,
         "img_url": img_url,
    }
    return book_params


book_url = "https://tululu.org/txt.php"

folder_book_name = Path("books")
if not folder_book_name.exists():
    folder_book_name.mkdir()  

folder_name = Path("images")
if not folder_name.exists():
    folder_name.mkdir()

for id in range(1, 11):
    page_url = f"https://tululu.org/b{id}/"

    try:
        params = {
            "id":id,
        }

        book_response = requests.get(book_url, params)
        book_response.raise_for_status()
        check_for_redirect(book_response)

        response_page = requests.get(page_url)
        book_params = parse_book_page(response_page)

        book_name = book_params["tittle"]
        download_books(folder_book_name, book_name, book_response)

        img_url = book_params["img_url"]
        image_name = img_url.split("/")[-1]
        img_url = f"https://tululu.org{img_url}"
        download_images(folder_name, image_name, img_url)

        print(f"Заголовок: {book_params["tittle"]} \n {book_params["genre"]}")

    except:
        print("Такой книги нет")
