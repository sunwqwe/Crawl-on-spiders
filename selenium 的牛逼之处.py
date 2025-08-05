from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置Edge浏览器选项
options = Options()
options.add_argument("--start-maximized")  # 启动时最大化窗口
options.add_argument("--disable-extensions")  # 禁用扩展
options.add_argument("--disable-infobars")  # 禁用信息栏

# 创建Edge WebDriver服务
service = Service(executable_path='D:\爬虫和反爬\edgedriver_win64\msedgedriver.exe')  # 替换为你的EdgeDriver路径

# 初始化浏览器驱动
driver = webdriver.Edge(service=service, options=options)

try:
    # 打开百度
    driver.get("https://www.baidu.com")

    # 显式等待搜索框加载完成（最多等待10秒）
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "kw"))
    )

    # 输入搜索词
    search_box.send_keys("曹操历史")

    # 定位搜索按钮并点击
    search_button = driver.find_element(By.ID, "su")
    search_button.click()

    # 等待搜索结果加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content_left"))
    )

    print("搜索成功！页面标题:", driver.title)

    # 实际使用时移除暂停，这里为了演示效果保留
    input("按Enter键结束...")

finally:
    # 关闭浏览器
    driver.quit()