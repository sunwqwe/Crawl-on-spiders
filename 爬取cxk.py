# coding=utf-8
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt
import time
import random
import re

# 初始化Edge浏览器
service = Service(executable_path=r"D:\爬虫和反爬\edgedriver_win64\msedgedriver.exe")
browser = webdriver.Edge(service=service)
WAIT = WebDriverWait(browser, 15)
browser.set_window_size(1400, 900)

# Excel设置
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('蔡徐坤篮球', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '地址')
sheet.write(0, 2, '描述')
sheet.write(0, 3, '观看次数')
sheet.write(0, 4, '弹幕数')
sheet.write(0, 5, '发布时间')

n = 1  # Excel行计数器


def random_delay(min=1, max=3):
    """随机延迟1-3秒，模拟人工操作"""
    delay = random.uniform(min, max)
    print(f"等待 {delay:.1f} 秒...")
    time.sleep(delay)


def handle_login_overlay():
    """处理登录遮罩层的多种方法"""
    try:
        # 方法1：尝试直接关闭登录弹窗
        close_btn = WAIT.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".bili-mini-login-close, .close-btn, .bili-login-close")))
        close_btn.click()
        print("已关闭登录弹窗")
        random_delay()
        return True
    except TimeoutException:
        pass

    try:
        # 方法2：如果遮罩层挡住了首页按钮，尝试点击首页按钮
        home_btn = WAIT.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#primary_menu > ul > li.home > a, .header-logo, .bili-header__logo")))
        home_btn.click()
        print("已通过点击首页按钮绕过遮罩层")
        random_delay()
        return True
    except TimeoutException:
        pass

    try:
        # 方法3：使用JS直接移除遮罩层元素
        browser.execute_script("""
            var elements = document.querySelectorAll('.bili-mini-login, .login-layer');
            elements.forEach(function(element) {
                element.style.display = 'none';
            });
        """)
        print("已通过JS移除遮罩层")
        return True
    except Exception:
        pass

    print("未能处理登录遮罩层")
    return False


def search():
    try:
        print('正在访问B站首页...')
        browser.get("https://www.bilibili.com/")
        random_delay()

        # 处理登录遮罩层
        if not handle_login_overlay():
            print("警告：可能存在未处理的登录遮罩层")

        print('正在搜索"蔡徐坤 篮球"...')
        # 等待搜索框和按钮（添加多个备选选择器）
        search_input = WAIT.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            ".nav-search-input, .search-keyword, .header-search-input")))
        search_btn = WAIT.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        ".nav-search-btn, .search-btn, .header-search-submit")))

        search_input.clear()
        search_input.send_keys('蔡徐坤 篮球')
        random_delay()
        search_btn.click()

        # 切换到新标签页
        WAIT.until(lambda d: len(d.window_handles) > 1)
        browser.switch_to.window(browser.window_handles[1])
        print("已切换到搜索结果页")

        # 再次检查是否有遮罩层
        handle_login_overlay()

        # 获取总页数
        try:
            # 等待页面加载完成
            WAIT.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".video-list, .bili-video-card")))

            # 尝试多种方式获取总页数
            try:
                total_pages_element = WAIT.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    ".pagination-btn:last-child, .page-item.last > button, .be-pager-item:last-child")))
                total_pages = int(total_pages_element.text)
            except:
                # 如果找不到分页按钮，尝试从分页信息中提取
                pagination_info = WAIT.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    ".be-pager-total, .pagination-info")))
                # 使用正则表达式提取数字
                match = re.search(r'(\d+)', pagination_info.text)
                if match:
                    total_pages = int(match.group(1))
                else:
                    total_pages = 1

            print(f"总页数: {total_pages}")
            return total_pages
        except:
            print("获取总页数失败，默认返回1页")
            return 1

    except Exception as e:
        print(f"搜索出错: {e}")
        browser.save_screenshot('search_error.png')
        return search()


def next_page(page_num):
    try:
        print(f'正在翻到第 {page_num} 页...')

        # 滚动到底部，确保分页按钮可见
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        random_delay()

        # 尝试点击下一页按钮
        next_btn = WAIT.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        ".pagination-next, .page-item.next > button, .be-pager-next")))
        next_btn.click()

        # 等待页面加载完成
        WAIT.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR,
                 ".pagination-item.active, .page-item.active > button, .be-pager-item-active"),
                str(page_num)
            )
        )
        random_delay()
        get_source()

    except Exception as e:
        print(f"翻页出错: {e}")
        browser.save_screenshot(f'page_{page_num}_error.png')
        browser.refresh()
        random_delay(2, 4)  # 出错后等待更长时间
        return next_page(page_num)


def save_to_excel(soup):
    global n
    try:
        # 查找视频列表
        items = soup.find_all(class_='bili-video-card')
        if not items:
            items = soup.find_all(class_='video-item')

        if not items:
            print("警告：未找到任何视频项目！")
            return

        print(f"找到 {len(items)} 个视频项目")

        for item in items:
            try:
                title_elem = item.find('h3') or item.find(class_='title')
                title = title_elem.get('title') or title_elem.text.strip() if title_elem else "N/A"

                link_elem = item.find('a')
                link = ("https:" + link_elem.get('href')) if link_elem and link_elem.get('href') else "N/A"

                desc_elem = item.find(class_='descript') or item.find(class_='desc')
                desc = desc_elem.text.strip() if desc_elem else "N/A"

                views_elem = item.find(class_='play-text') or item.find(class_='play')
                views = views_elem.text.strip() if views_elem else "N/A"

                danmu_elem = item.find(class_='dm-text') or item.find(class_='dm')
                danmu = danmu_elem.text.strip() if danmu_elem else "N/A"

                date_elem = item.find(class_='time-text') or item.find(class_='time')
                date = date_elem.text.strip() if date_elem else "N/A"

                # 打印简化信息
                short_title = title[:20] + '...' if len(title) > 20 else title
                print(f'爬取: {short_title} | 观看: {views}')

                # 保存到Excel
                sheet.write(n, 0, title)
                sheet.write(n, 1, link)
                sheet.write(n, 2, desc)
                sheet.write(n, 3, views)
                sheet.write(n, 4, danmu)
                sheet.write(n, 5, date)
                n += 1

            except Exception as e:
                print(f"处理单个视频出错: {e}")
                continue

    except Exception as e:
        print(f"保存到Excel出错: {e}")


def get_source():
    try:
        WAIT.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".video-list, .video-list.clearfix, .bili-video-card")))
        random_delay(1, 2)

        # 滚动页面以加载所有内容
        print("滚动页面以加载所有内容...")
        for i in range(3):
            scroll_height = 500 + i * 300  # 每次滚动距离增加
            browser.execute_script(f"window.scrollBy(0, {scroll_height})")
            random_delay(0.5, 1.5)

        # 确保所有内容加载完成
        random_delay(1, 2)

        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        save_to_excel(soup)

    except Exception as e:
        print(f"获取页面源码出错: {e}")
        browser.save_screenshot('source_error.png')


def main():
    global n
    try:
        total_pages = search()
        if total_pages > 10:  # 限制最多爬取10页
            total_pages = 10
            print("限制最多爬取10页数据")

        # 先保存第一页数据
        get_source()

        # 翻页处理
        for page in range(2, total_pages + 1):
            next_page(page)

    except Exception as e:
        print(f"主函数出错: {e}")
        browser.save_screenshot('main_error.png')
    finally:
        browser.quit()
        book.save('蔡徐坤篮球.xlsx')
        print(f"数据已保存到Excel，共{n - 1}条记录")


if __name__ == '__main__':
    main()
