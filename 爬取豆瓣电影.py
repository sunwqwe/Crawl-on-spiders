import requests
from bs4 import BeautifulSoup
import xlwt
import time  # 添加延时模块防止请求过快


def request_douban(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    }

    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')

n = 1


def save_to_excel(soup):
    global n
    list = soup.find(class_='grid_view').find_all('li')

    for item in list:
        # 修复排名提取问题
        item_index = item.find('em').string  # 排名在<em>标签内

        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text.strip()  # 添加strip()清理空白

        # 简介处理
        inq_element = item.find(class_='inq')
        item_intr = inq_element.string if inq_element else 'NOT AVAILABLE'

        print(f'爬取电影：{item_index} | {item_name} | {item_score} | {item_intr}')

        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_img)
        sheet.write(n, 2, item_index)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_author)
        sheet.write(n, 5, item_intr)

        n += 1


def main(page):
    url = f'https://movie.douban.com/top250?start={page * 25}&filter='
    html = request_douban(url)
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


if __name__ == '__main__':
    for i in range(0, 10):
        main(i)
        time.sleep(2)  # 添加延时防止被封IP
    book.save('豆瓣最受欢迎的250部电影.xls')