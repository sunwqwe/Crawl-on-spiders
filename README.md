# Crawl-on-spiders
requests/BeautifulSoup/selenium 



requests
用途：
发送 HTTP 请求（GET/POST 等），获取网页原始内容（HTML/JSON/二进制文件等）。
特点：

轻量级，高效，适合静态页面抓取

直接处理网络请求和响应

不支持 JavaScript 渲染
典型场景：

获取静态 HTML 页面

调用 RESTful API

下载文件
示例代码：


<img width="441" height="134" alt="屏幕截图 2025-08-05 213534" src="https://github.com/user-attachments/assets/a508bf3e-8276-4d3a-995d-206dbf1b10e6" />




BeautifulSoup（需配合 requests 使用）
用途：
解析 HTML/XML 文档，提取结构化数据（如文本、链接、属性）。
特点：

仅用于解析，不能发送网络请求

提供简单易用的 API（如 find(), select()）

依赖解析器（如 lxml, html.parser）
典型场景：

从静态 HTML 中提取标题、表格、链接等

清理和转换文档结构
示例代码：


<img width="440" height="215" alt="屏幕截图 2025-08-05 213719" src="https://github.com/user-attachments/assets/e6eb7515-8db6-4ca5-b92e-4bcdb50742c2" />




selenium
用途：
自动化浏览器操作，处理动态加载内容（如 JavaScript 渲染的页面）。
特点：

模拟真实用户行为（点击、输入、滚动等）

支持所有现代浏览器（需安装对应 WebDriver）

资源消耗大，速度慢
典型场景：

抓取 JavaScript 动态生成的内容（如 React/Vue 应用）

自动化登录、表单提交

网页截图或测试
示例代码：


<img width="528" height="292" alt="屏幕截图 2025-08-05 213750" src="https://github.com/user-attachments/assets/19e87dd6-28b5-4e33-a5fd-73729e816033" />



三者的协作关系

<img width="1357" height="522" alt="三者关系" src="https://github.com/user-attachments/assets/8a420a47-bd0b-42c3-a58a-c0dd0db3aac4" />


静态页面：requests + BeautifulSoup（高效）

动态页面：selenium + BeautifulSoup（功能全面）

<img width="736" height="288" alt="屏幕截图 2025-08-05 213926" src="https://github.com/user-attachments/assets/675a753c-4801-4314-ab76-e0f14cbee503" />



