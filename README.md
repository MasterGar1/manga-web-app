# manga-web-app
Manga reader app in python, using the [MangaDexAPI](https://api.mangadex.org/docs/).

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/MasterGar1/manga-web-app
    ```
2. Navigate to the project directory:
    ```bash
    cd manga-web-app
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.Run the app:
    ```bash
    python main.py
    ```

## How to use
After running the app by following the beforementioned steps, you will be greeted with the Log in page. There you will be able to create or log into an existing account.

Logging in will lead you to the home page. There, you can either search manga or read ones you have read before.

Searching can be done by title, genre, status and demographic. You can also choose how many, and in what way the output mangas will be. Note that an illegal search input may yield unexpected results or no result at all.

After you search a manga, you can check it out by clicking on it. There you will get a description and chapter list from which you can pick, if you want to read.

Manga chapters will be displayed vertically, thus you will have to scroll down to look through all images.

After you have read a manga, it will be added to your library. In the library, you can browse through your past reads, using some filters and sorts, which can be found on the top of the page.

## License
This project is licensed under the MIT License.
