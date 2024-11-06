import requests
from bs4 import BeautifulSoup
import pandas as pd


def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Referer": "https://www.google.com",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error fetching the page: {e}")
        


products = []
prices = []
original_prices = []
discounts = []
assureds = []
straps = []
images = []


def main():
    try:
        pageno = 0

        while True:
            pageno = 1 + pageno
            print("Fetching the data of page no.", pageno)
            URL = f"https://www.flipkart.com/search?q=smart+watch&otracker=search&marketplace=FLIPKART&page={pageno}"

            page_content = fetch_page(URL)

            content = BeautifulSoup(page_content, "html.parser")

            watch_data = content.find_all("div", {"class": "_1sdMkc LFEi7Z"})
            if not watch_data:
                break

            for watch in watch_data:
                name = watch.find("a", {"class": "WKTcLC"})
                price = watch.find("div", {"class": "Nx9bqj"})
                original_price = watch.find("div", {"class": "yRaY8j"})
                discount = watch.find("div", {"class": "UkUFwK"})
                assured = watch.find("div", {"class": "iW2uHd"})
                strap = watch.find("div", {"class": "Br9IW+"})
                img = watch.find("img", {"class": "_53J4C-"})
                

                products.append(name.text if name else "N/A")
                prices.append(price.text if price else "N/A")
                original_prices.append(original_price.text if original_price else "N/A")
                discounts.append(discount.text if discount else "N/A")
                straps.append(strap.text if strap else "N/A")
                assureds.append("Flipkart Assured" if assured else "Not Assured")
                images.append(img["src"])

        df = pd.DataFrame(
            {
                "Product_Name": products,
                "Original Price": original_prices,
                "Price": prices,
                "Discount": discounts,
                "Flipkart Assured": assureds,
                "Strap size": strap,
                "Image": images,
            }
        )
        df.to_csv("products.csv")
        print("Data Fetched Successfully")
    except Exception as e:
        print(f"Error fetching the page: {e}")
       


main()
