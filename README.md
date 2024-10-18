# Парсер книг с сайта tululu.org

Это приложение позволяет загружать книги с онлайн библиотеки [tululu.org](https://tululu.org). С помощью этого парсера вы можете автоматически скачивать книги, указав диапазон страниц.

## Как установить

Для запуска приложения вам потребуется установленный Python (рекомендуется версия 3.6 и выше). Также необходимо установить несколько библиотек. Вы можете сделать это, используя команду:

```bash
pip install -r "requirements.txt"
```
## Аргументы
Приложение поддерживает следующие аргументы:

 -start_id: Указывает номер первой книги, с которой начнется парсинг.
Например, если вы хотите начать с первой книги, укажите -start_id 1.

-end_id: Указывает номер последней книги, до которой будет производиться парсинг. 
Например, если вы хотите закончить на пятой книге, укажите -end_page 5.
Пример запуска приложения:

```bush
python main.py -start_id 1 -end_id 5
```
Это команда загрузит книги с первой по пятую страницу.

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.