import pyppeteer
import asyncio
import requests
import bs4

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
url = input("输入文件页链接：")


async def main():
    browser = await pyppeteer.launch(headless=False, userDataDir="./userdata", executablePath=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    # browser = await pyppeteer.launch(headless=False)
    page = await browser.newPage()
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver",{get:() =>undefined})')
    await page.goto(url)
    await page.waitForSelector("iframe#file_preview")
    await asyncio.sleep(1)
    iframe = await page.J('iframe#file_preview')
    src = await page.evaluate('(element) => unescape(element.getAttribute("src"))', iframe)

    # 打印解码后的src属性
    print('Decoded src:', src)
    new_link = src.replace("&ssl=1", "")
    response = requests.get(new_link)
    response.encoding = response.apparent_encoding
    soup = bs4.BeautifulSoup(response.text)
    new_new_link = soup.find(attrs={"style": "color:red"}).contents[0]

    response = requests.get(new_new_link.text.replace("\n","").replace(" ",""))
    title = response.headers.get('content-disposition').split(";")[0].strip('"').strip('filename="')
    print(title)
    with open(title, "wb") as file:
        file.write(response.content)

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
