import httpx
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin
from dataclasses import asdict,dataclass,fields,field
import re
import json,csv


@dataclass
class Item:
    Name : str | None
    Price : str| None
    Discount : str | None
    Color : str | None
    Sizes : list | None

def getHtml(baseurl,**kwargs):
    headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }

    if(kwargs.get("page")):
        response = httpx.get(baseurl+kwargs.get("page"), headers=headers, timeout=30,follow_redirects=True)
    else:
        response = httpx.get(baseurl, headers=headers, timeout=30,follow_redirects=True)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print("NoMore Page available")
        return False

    html = HTMLParser(response.text)
    return html


def getproduct(product,identifier):
    try:
        return product.css_first(identifier).text()
    except AttributeError:
        return None

def getproductinformationlink(product,identifier):
    try: return urljoin("https://www.boohooman.com" , product.css_first(identifier).attributes["href"])
    except AttributeError: return None

def getproductinformtion(htmlpage):
    try:
        sizes = htmlpage.css("ul.swatches li.variation-value")
        allsizes = []
        for size in sizes:
            pro = getproduct(size,"span .swatchanchor-text")
            if pro is None:
                continue
            else:
                allsizes.append(re.sub(r"[\s\\n]", "", pro))
        
        newitem = Item(
            Name = re.sub(r"[\s\\n]", "",htmlpage.css_first(".product-name").text()),
            Price = re.sub(r"[\s\\n]", "", htmlpage.css_first(".price-standard").text()),
            Discount = re.sub(r"[\s\\n]", "", htmlpage.css_first(".price-sales").text()),
            Color = re.sub(r"[\s\\n]", "", htmlpage.css_first(".selected-value").text()),
            Sizes = allsizes,
        )

        return asdict(newitem)
    except AttributeError: return None

def convert_to_JSON(product):
    with open("products.json","w",encoding="utf-8") as f:
        json.dump(product,f,ensure_ascii=False,indent=4)
    print("Saved to JSON")

def convert_to_csv(product):
    fields_names = [field.name for field in fields(Item)]
    with open("products.csv","w") as f:
        if(product != "null"):
            writer = csv.DictWriter(f,fields_names)
            writer.writeheader()
            writer.writerows(product)
    print("Saved to CSV")

def parser(html):
    try:
        products = html.css("ul#search-result-items li")
        allproducts = []
        for product in products :
            product_link = getproductinformationlink(product,".product-tile .product-tile-name a.name-link")
            htmlpage = getHtml(product_link)
            newitem = getproductinformtion(htmlpage)
            if(newitem != None and newitem != "null"):
                allproducts.append(newitem)
            print("item added")
        convert_to_JSON(allproducts)
        convert_to_csv(allproducts)    

    except httpx.ReadTimeout:
        print("The request timed out. Try again later.")

def main():
    url = "https://www.boohooman.com/us/mens/promo?start="
    for x in range(0,1):
        time.sleep(1)
        i = x*80
        html = getHtml(url,page = f"{i}&sz=80")
        if html == False:
            break
        parser(html)

if __name__ == "__main__":
    main()