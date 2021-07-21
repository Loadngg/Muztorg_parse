import requests
from bs4 import BeautifulSoup
import time
import csv
import datetime


start_time = time.time()


def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"muztorg_{cur_time}.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название гитары",
                "Цена",
                "Фотография"
            )
        )

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    url = 'https://www.muztorg.ru/category/elektrogitary?in-stock=1&pre-order=1'

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    pages_count = int(soup.find('ul', class_='pagination').find_all('a')[-2].text)

    guitars_data = []
    for page in range(1, pages_count + 1):
        url = f'https://www.muztorg.ru/category/elektrogitary?in-stock=1&pre-order=1&page={page}'

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        guitar_items = soup.find('div', class_='thumbnail-list grid-3').find_all('section', class_='product-thumbnail')

        for item in guitar_items:
            guitar_data = item.find('div', class_='product-caption').find_all('a')
            guitar_price = item.find('p', class_='price').find_all('meta')

            try:
                guitar_photo = item.find('div', class_='product-pictures').find_all('a')[-1].find('img')['data-src']
            except:
                guitar_photo = 'Фото отсутствует'

            try:
                guitar_title = guitar_data[1].text.strip()
            except:
                guitar_title = 'Нет названия'

            try:
                guitar_price = guitar_price[-1]['content'] + ' руб'
            except:
                guitar_price = 'Нет цены'

            guitars_data.append(
                {
                    'guitar_title': guitar_title,
                    'guitar_price': guitar_price,
                    'guitar_photo': guitar_photo
                }
            )

            with open(f"muztorg_{cur_time}.csv", "a") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        guitar_title,
                        guitar_price,
                        guitar_photo
                    )
                )

        print(f"[INFO] Обработана {page}/{pages_count}")
        time.sleep(1)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == "__main__":
    main()
