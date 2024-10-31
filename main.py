import pyppeteer
import asyncio
import requests
import bs4

title_selector = "#xy_app_content > div.ta-frame > div.ta_panel.ta_panel_group.ta_group > section > section > main > div > div.group-resource-body > div > div.disk_previewer_with_banner > div.common_node_content_banner.flex_panel.hor > h5"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
url = input("输入小雅链接：")


async def main():
    # 请修改executablePath为Chrome浏览器路径
    # browser = await pyppeteer.launch(headless=False, userDataDir="./userdata", executablePath=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    browser = await pyppeteer.launch(headless=False, userDataDir="./userdata")
    page = await browser.newPage()
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver",{get:() =>undefined})')
    await page.goto(url)
    await page.waitForSelector("iframe#file_preview")
    await asyncio.sleep(1)
    iframe = await page.J('iframe#file_preview')
    src = await page.evaluate('(element) => unescape(element.getAttribute("src"))', iframe)
    title_element = await page.J(title_selector)
    title = await page.evaluate(f'(element) => element.textContent', title_element)
    if not title.endswith((".txt", ".pdf", ".doc", ".docx", ".ppt", ".pptx")):
        title = await page.evaluate(f'(element) => element.title', title_element)
    await browser.close()
    # 打印解码后的src属性
    print('Decoded src:', src)
    print('File Name:', title)
    new_link = src.replace("&ssl=1", "")
    response = requests.get(new_link)
    response.encoding = response.apparent_encoding
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    new_new_link = soup.find(attrs={"style": "color:red"}).contents[0]

    response = requests.get(new_new_link.text.replace("\n", "").replace(" ", ""))
    with open(title, "wb") as file:
        file.write(response.content)


asyncio.get_event_loop().run_until_complete(main())
