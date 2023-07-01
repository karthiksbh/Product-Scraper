from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

    for listing in listings[:3]:
        if listing:
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

            rating_element = listing.find("div", {"class": "a-row a-size-small"})
            if rating_element:
                rating = rating_element.find('span', class_ = "a-icon-alt").text
            else:
                continue
    #             rating = "Cannot Fetch"

            review_element = listing.find("span", {"class": "a-size-base s-underline-text"})
            if review_element:
                review = '('+review_element.text+')';
            else:
                continue


    #         image_element = listing.find("img", {"class": "s-image"})
    #         if image_element:
    #             image_url = image_element["src"]
    #         else:
    #             continue

            results.append({"platform": "Amazon", "title": title, "price": price, "rating": rating, "review": review, "url": url}) 
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

    for listing in listings[:3]:      
        if listing:
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

            # image_element = listing.find("img", {"class": "product-image"})
            # if image_element:
            #     image_url = image_element.get('src')
            # else:
            #     continue

            rating_element = listing.find("div", {"class" : "filled-stars"})
            if rating_element:
                ratingLst = rating_element.get('style').split(":");
                rating = float(ratingLst[1][0:-1])
            else:
                continue

            review_element = listing.find("p", {"class" : "product-rating-count"})
            if review_element:
                review = review_element.text
    #             print(review)
            else:
                continue
            
        
        results.append({"platform":"Snapdeal","title": title, "price": price, "rating": rating, "review": review, "url": url})#, "image_url": image_url})
    return results

def scrape_flipkart(search_query):
    search_query = urllib.parse.quote(search_query)
    linkStr = f"https://www.flipkart.com/search?q={search_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(linkStr, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    elements=soup.find_all("div", class_="_13oc-S")

    result = []
    
    for e in elements[:3]:
        elePrefix = e.find("div", class_="_2kHMtA").find('a')
        
        url = "https://www.flipkart.com" + elePrefix.get('href')

#         image_url = elePrefix.find("div", class_ = "_2QcLo-").find('img').get('src')
        
        
        title=e.find("div", class_="col col-7-12").find("div", class_="_4rR01T").text

        reviews = e.find("span", class_="_2_R_DZ")#.find("div", class_= "_3LWZlK")
        if reviews:
            reviews = reviews.get_text(strip = True)

    
        rating = e.find("div", class_="_2kHMtA").find('a').find("div", class_ = "col col-7-12").find("div", class_="_3LWZlK")
        
        if rating:
            rating = rating.text
            reviewLst = reviews.split('&')
            rating += " ("+reviewLst[0]+")"
            reviews = reviewLst[0]+" & "+reviewLst[1]
            
#         print("Title: ", title,"Rating: ", rating)

        #Price
        price = e.find("div", class_="col col-5-12 nlI3QM").find("div", class_="_30jeq3 _1_WHN1").text

        result.append({"platform": "Flipkart", "title": title, "price": price, "rating": rating, "review": reviews, "url": url})
        
    return result
    
@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query')

    if not search_query:
        return jsonify(error="Missing search query"), 400

    amazon_results = scrape_amazon(search_query)
    snapdeal_results = scrape_snapdeal(search_query)
    flipkart_results = scrape_flipkart(search_query)

    all_results = amazon_results + snapdeal_results+flipkart_results
    random.shuffle(all_results)

    return jsonify(all_results)

if __name__ == '__main__':
    app.run(debug=True)