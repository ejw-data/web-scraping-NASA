# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd




def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    
    url_base = "https://www.jpl.nasa.gov"
    url_add = '/spaceimages/?search=&category=Mars'
    browser.visit(url_base+url_add)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    bttn_image_url = soup.find('article', class_='carousel_item').get('style')
    start=bttn_image_url.find("url('")
    end=bttn_image_url.find("');")
    featured_image_url=url_base+bttn_image_url[start+3+len("('"):end]
    
    
    
    url_base = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_base)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_weather = soup.find('p', class_='TweetTextSize').text
    
    
    url_base = "https://space-facts.com/mars/"
    browser.visit(url_base)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    table = pd.read_html(url_base)
    htmltable=table[0].to_html()
    
    
    
    link2=[]
    link3=[]
    link4=[]
    url_base = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_base)
    time.sleep(2)
    links = browser.find_link_by_partial_text('Hemisphere')
    [link2.append(link['href']) for link in links]
    for link in link2:
        browser.visit(link)
        time.sleep(2)
        url_link = browser.find_link_by_partial_text('Sample') 
        title_text = browser.find_by_css('.title')
        link3.append(url_link['href'])
        link4.append(title_text.html)
    hemisphere_image_urls = []
    for i in range(len(link3)):
        hemisphere_image_urls.append({"title": link4[i], "img_url": link3[i]})
    
    
    
    listings["news_p"] = news_p
    listings["news_title"]=news_title
    listings["featured_image_url"] = featured_image_url
    listings["mars_weather"] = mars_weather
    listings["html_table"] = htmltable
    listings["hemisphere_img_dict"] = hemisphere_image_urls

    return listings
    
    