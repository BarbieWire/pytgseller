from bs4 import BeautifulSoup
import aiohttp


async def get_currency(dollars=6):
    async with aiohttp.ClientSession() as session:
        url = f'https://www.xe.com/currencyconverter/convert/?Amount={dollars}&From=USD&To=XBT'
        data = await session.get(url=url)
        data = await data.text()
        soup = BeautifulSoup(data, 'lxml')
        btc = soup.find('p', class_="result__BigRate-sc-1bsijpp-1 iGrAod")
        return btc.text
