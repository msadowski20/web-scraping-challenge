from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    # NASA Mars News
    news_url = 'https://mars.nasa.gov/news/'
    response = requests.get(news_url)
    soup = bs(response.text, 'html.parser')
    
    results = soup.find_all('div', class_='slide')

    title_list = []
    p_list = []

    for result in results:
        title = result.find('div', class_="content_title").text
        p = result.div.a.text

        title_list.append(title)
        p_list.append(p)

    news_title = title_list[0].strip()
    news_p = p_list[0].strip()
    
    # NASA JPL Featured Image
    browser = init_browser()

    jpl_base_url = 'https://www.jpl.nasa.gov'
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser.visit(jpl_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    result = soup.find('article', class_='carousel_item')
    featured_image = result.a['data-fancybox-href']

    featured_image_url = f"{jpl_base_url}{featured_image}"

    browser.quit()

    # Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(twitter_url)
    soup = bs(response.text, 'html.parser')

    results = soup.find_all('div', class_='tweet')
    
    weather_list = []

    for result in results:
        tweet = result.find('div', class_="js-tweet-text-container")
        weather = tweet.p.text
        weather_list.append(weather)

    mars_weather = weather_list[0].strip()

    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[2]
    df = df.rename(columns={0: 'description', 1: 'value'})
    df = df.set_index('description')
    table_html = df.to_html()
    table_html = table_html.replace('\n', '')

    # Mars Hemispheres
    browser = init_browser()

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    browser.visit(hemisphere_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_='item')

    hemisphere_base_url = 'https://astrogeology.usgs.gov'
    image_url_dict = []

    for result in results:
        title = result.h3.text
        partial_image_url = result.find(
            'a', class_='itemLink product-item')['href']
        browser.visit(hemisphere_base_url + partial_image_url)

        image_html = browser.html
        soup = bs(image_html, 'html.parser')
        image_url = hemisphere_base_url + \
            soup.find('img', class_='wide-image')['src']

        image_url_dict.append({"title": title, "image_url": image_url})

    browser.quit()

    # Store all results into a dictionary
    mars_data = {
        "News_Title": news_title,
        "News_Paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Facts": table_html,
        "Mars_Hemispheres": image_url_dict
    }

    return mars_data




