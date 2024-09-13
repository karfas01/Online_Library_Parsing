from pathlib import Path
import requests


for id in range(1, 11):
    url = f"https://tululu.org/txt.php?id={id}"

    response = requests.get(url)
    response.raise_for_status()

    folder_name = Path("books_db")
    file_name = folder_name / f"book_{id}.txt"

    if not folder_name.exists():
        folder_name.mkdir()

    with open(file_name, 'wb') as file:
        file.write(response.content)

