from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape1(browser):
    
    heading = {}

    url ="https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "lxml")

    heading["title"] =soup.select_one('li.slide').find('div', class_="image_and_description_container").find('div', class_='content_title').get_text()
    heading["paragraph"]=soup.select_one('li.slide').find('div', class_="image_and_description_container").find('div', class_='article_teaser_body').get_text()

    browser.quit()

    return heading

def scrape2(browser):
    
    url2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    baseimageurl2='https://www.jpl.nasa.gov'        
    browser.visit(url2)

    html=browser.html
    soup=BeautifulSoup(html,"lxml")
    images= soup.find('article', class_='carousel_item')['style']
    featured=images.split("'")
    featured_image =baseimageurl2 + featured[1]

    browser.quit()
    return featured_image

def scrape3():
    #  we did not use browser for this (only pandas); delete all components
    # Marsfacts={}

    url3="https://space-facts.com/mars/"
    
    # browser.visit(url3)

    #html=browser.html
    #soup=BeautifulSoup(html,"lxml")
    Marsfacts = pd.read_html(url3)
    MarsFactsMain = Marsfacts[0]
    MarsFactsMain = MarsFactsMain.rename(columns={0: "Description", 1: "Mars"})

    ## do we need this code, where it is converted back to html
    #Factstablehtml=MarsFactsMain.to_html()
    # browser.quit()
    return MarsFactsMain

def scrape4(browser):    
    
    hemispheresList=[]

    url4="https://space-facts.com/mars/"
    
    browser.visit(url4)

    html=browser.html
    soup=BeautifulSoup(html,"lxml")

    hemispherehtml=soup.find_all('div', class_="item")
    for link in hemispherehtml:
        hemispheredict={}
        imagelink=link.find("a")['href']
        imagetitle=link.find("h3").get_text()
    
        hemispheredict["ImageTitle"]=imagetitle
        hemispheredict["ImageLink"]=imagelink

        hemispheresList.append(hemispheredict)   
    browser.quit()
    return hemispheresList
    
def scrapeALL():
    browser=init_browser()
    marsdata={}

    
    marsdata["Heading"] = scrape1(browser)
    marsdata["Image"] = scrape2(browser)
    # we dont need a browser for this scrape 3 because we used pd.html in pandas
    marsdata["Facts"] = scrape3()
    marsdata["Hemispheres"] = scrape4(browser)

    return marsdata
  
# heading
    #   Title
    #   Paragraph
#image
#Facts
#hemispheres
    # 0
        #ImageTitle
        #ImageLink
    #1