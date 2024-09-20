from pathlib import Path
import requests


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError()


for id in range(1, 11):
    url = f"https://tululu.org/txt.php?id={id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)

        folder_name = Path("books_db")
        file_path = f"{folder_name}/book_{id}.txt"

        if not folder_name.exists():
            folder_name.mkdir()

        with open(file_path, 'wb') as file:
            file.write(response.content)
    except:
        print("Такой книги нет")
