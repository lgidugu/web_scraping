import os
import time
from flask import Flask, render_template
from bs4 import BeautifulSoup as bs
import pymongo
import requests
from splinter import Browser

app = Flask(__name__)

str_conn = "mongodb://localhost:27017"
client_conn = pymongo.MongoClient(str_conn)
client_conn.server_info()

obj_db = client_conn.db_mars
obj_mars = obj_db.tbl_marsInfo
    

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

@app.route("/scrape")
def scrape():
    browser = init_browser()
    scrape_data = {}    
    
    headlines_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    obj_db = client_conn.db_mars
    obj_collection = obj_db.tbl_marsInfo
    # Retrieve page with the requests module
    response = requests.get(headlines_url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    news_title = soup.find('div', class_='content_title').text
    print(news_title)

    news_p = soup.find('div', class_='rollover_description_inner').text
    print(news_p)
    
    scrape_data['heading'] = news_title
    scrape_data['desc'] = news_p
    
    url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_images)
    html = browser.html
    soup_1 = BeautifulSoup(html, 'lxml')
    link = soup_1.find('article', class_='carousel_item')['style']
    url_link = link.split('(')[1]
    url_link = url_link.split(')')[0]
    url_link = url_link.split("'")[1]

    featured_image_url = "https://www.jpl.nasa.gov" + str(url_link)
    print(featured_image_url)
    
    scrape_data['featured_image'] = featured_image_url

    url = 'https://twitter.com/MarsWxReport'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    tweets = [p for p in soup2.find('p', class_='tweet-text')]
    mars_weather = tweets[0]
    print(mars_weather)
    scrape_data['weather'] = mars_weather

    url_table = "https://space-facts.com/mars/"
    tables = pd.read_html(url_table, header=0)
    for table in tables:
        print(table)
    df = tables[0]
    df.columns = ['Description', 'Value']
    html_table = df.to_html()
    
    scrape_data['table'] = html_table

    url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    browser.visit(url)
    html = browser.html
    soup4 = BeautifulSoup(html, 'lxml')
    image_link2 = soup5.find_all('img')[0]['src']
    image_title2 = image_link2.split('.')[3]
    image_title2 = str(image_title2.split('/')[3]) + " " + str(image_title2.split('/')[4])
    image_title2 = str(image_title2.split('_')[0]) + " " + "Hemisphere"

    url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    browser.visit(url)
    html = browser.html
    soup6 = BeautifulSoup(html, 'lxml')
    image_link3 = soup6.find_all('img')[0]['src']
    image_title3 = image_link3.split('.')[3]
    image_title3 = str(image_title3.split('/')[3]) + " " + str(image_title3.split('/')[4])
    image_title3 = str(image_title3.split('_')[0]) + " " + str(image_title3.split('_')[1]) + " " + "Hemisphere"

    url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    browser.visit(url)
    html = browser.html
    soup6 = BeautifulSoup(html, 'lxml')
    image_link3 = soup6.find_all('img')[0]['src']
    image_title3 = image_link3.split('.')[3]
    image_title3 = str(image_title3.split('/')[3]) + " " + str(image_title3.split('/')[4])
    image_title3 = str(image_title3.split('_')[0]) + " " + str(image_title3.split('_')[1]) + " " + "Hemisphere"

    url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'
    browser.visit(url)
    html = browser.html
    soup7 = BeautifulSoup(html, 'lxml')
    image_link4 = soup7.find_all('img')[0]['src']
    image_title4 = image_link4.split('.')[3]
    image_title4 = str(image_title4.split('/')[3]) + " " + str(image_title4.split('/')[4])
    image_title4 = str(image_title4.split('_')[0]) + " " + str(image_title4.split('_')[1]) + " " + "Hemisphere"

    hemisphere_image_urls = [{"Hemisphere title": image_title1, "image_url": image_link1},
                            {"Hemisphere title": image_title2, "image_url": image_link2},
                            {"Hemisphere title": image_title3, "image_url": image_link3},
                            {"Hemisphere title": image_title4, "image_url": image_link4}]
    hemisphere_image_urls

    
    scrape_data['images'] = hemisphere_image_urls
    
    post = {
            "Title": news_title,
            "Description": news_p,
            "Featured Image":featured_image_url,
            "Mars Table":table,
            "Mars Weather":mars_weather,
            "Mars Images":hemisphere_image_urls,
                }
    
    obj_mars.insert_one(post)
    mars_list = list(obj_mars.find())

    return render_template("index.html", scrape_list=mars_list)
    

    return scrape_data

if __name__ == "__main__":
    app.run(debug=True)


    




    

    
