import httpx
from selectolax.parser import HTMLParser
import time

def getHtml(baseurl,page):
    headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }
    response = httpx.get(baseurl+page, headers=headers, timeout=30,follow_redirects=True)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print("NoMore Page available")
        return False

    html = HTMLParser(response.text)
    return html


def getsaleprice(product,identifier):
    try:
       return product.css_first(identifier).attrs.get("content")
    except AttributeError:
        return None

def getproduct(product,identifier):
    try:
        return product.css_first(identifier).text()
    except AttributeError:
        return None
    
def parser(html):
    try:
        products = html.css("ul#search-result-items li")
        allproducts = []
        for product in products :
            name = getproduct(product,".product-tile .product-tile-name a.name-link")
            fullprice = getproduct(product,".product-tile .product-pricing div .product-standard-price")
            saleprice = getsaleprice(product,".product-tile .product-pricing div meta[itemprop=price]")
            item ={
                    "name" : name,
                    "fullprice" : fullprice,
                    "saleprice" : "$"+ str(saleprice),
                }
            allproducts.append(item)
            print(item)

    except httpx.ReadTimeout:
        print("The request timed out. Try again later.")

def main():
    url = "https://www.boohooman.com/us/mens/promo?start="
    for x in range(0,10):
        time.sleep(1)
        i = x*80;
        html = getHtml(url,f"{i}&sz=80")
        if html == False:
            break
        parser(html)

if __name__ == "__main__":
    main()