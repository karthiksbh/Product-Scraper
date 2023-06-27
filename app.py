from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random

app = Flask(__name__)

def scrape_amazon(search_query):
    search_query = urllib.parse.quote(search_query)
    url = f"https://www.amazon.in/s?k={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    listings = soup.find_all("div", {"data-component-type": "s-search-result"})
    results = []

    for listing in listings[:2]:
        title_element = listing.find("span", {"class": "a-size-medium"})
        if title_element:
            title = title_element.text.strip()
        else:
            continue

        price_element = listing.find("span", {"class": "a-price-whole"})
        if price_element:
            price = price_element.text.strip()
        else:
            continue

        url_element = listing.find("a", {"class": "a-link-normal"})
        if url_element:
            url = "https://www.amazon.in" + url_element["href"]
        else:
            continue

        image_element = listing.find("img", {"class": "s-image"})
        if image_element:
            image_url = image_element["src"]
        else:
            continue

        results.append({"platform": "Amazon", "title": title, "price": price, "url": url, "image_url": image_url})

    return results


def scrape_snapdeal(search_query):
    search_query = urllib.parse.quote(search_query)
    url = f"https://www.snapdeal.com/search?keyword={search_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    listings = soup.find_all("div", {"class": "col-xs-6"})

    results = []

    for listing in listings[:2]:
        title_element = listing.find("p", {"class": "product-title"})
        if title_element:
            title = title_element.text.strip()
        else:
            continue

        price_element = listing.find("span", {"class": "lfloat product-price"})
        if price_element:
            price = price_element.text.strip()
        else:
            continue

        url_element = listing.find("a", {"class": "dp-widget-link noUdLine"})
        if url_element:
            url = url_element["href"]
        else:
            continue

        image_element = listing.find("img", {"class": "product-image"})
        if image_element:
            image_url = image_element["src"]
        else:
            continue

        results.append({"platform":"Snapdeal","title": title, "price": price, "url": url, "image_url": image_url})

    return results


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query')

    if not search_query:
        return jsonify(error="Missing search query"), 400

    amazon_results = scrape_amazon(search_query)
    snapdeal_results = scrape_snapdeal(search_query)

    all_results = amazon_results + snapdeal_results
    random.shuffle(all_results)

    return jsonify(all_results)

if __name__ == '__main__':
    app.run()