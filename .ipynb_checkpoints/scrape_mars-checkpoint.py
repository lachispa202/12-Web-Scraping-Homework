# Declare Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import time


# ### Step 1 - Scraping from NASA Mars News

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Define URL to scrape and inform the browser to visit the page
def scrape():
    browser = init_browser()
    
    url = 'https://mars.nasa.gov/news/'
    
    browser.visit(url)

    time.sleep(1)

    # HTML Object
    html = browser.html
    
    time.sleep(2)

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    time.sleep(2)

# Using Beautiful Soup, we can find News Title and Paragraph Content. results = soup.find_all("div", class_="slide")
#     title_text = soup.find('li', attrs={'class': 'slide'}).find('h3').text
    title_text = soup.find('li', attrs={'class': 'slide'})
    news_title = title_text.text
    news_title = news_title.strip()

    time.sleep(2)
    news_summary = soup.find('div', class_='article_teaser_body')
    news_p = news_summary.text
    news_p = news_p.strip()


# # ### JPL Mars Space Images - Featured Image
    time.sleep(2)
    
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    time.sleep(2)
    
# Click to find full large image
    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(2)
    
# Click to find full large image
    browser.click_link_by_partial_text('more info')

    time.sleep(2)

# HTML Object 
    html_image = browser.html


# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')


# Retrieve background image
    results = soup.find('figure', class_="lede")

    href = results.a['href']


# # Create website url with scrapped route
    featured_image_url = 'https://www.jpl.nasa.gov' + href

    
# ### Mars Facts

# Mars Facts URL
    mars_facts_url = 'http://space-facts.com/mars/'
    
        
# Read html and parse
    mars_facts = pd.read_html(mars_facts_url)

    
# Find mars facts dataframe in list of dataframe
    mars_facts_dataframe = mars_facts[0]
    
    
# Assign Column names and set index. Display final datframe

    mars_facts_dataframe.columns = ["Description", "Measurement"]
    mars_facts_dataframe = mars_facts_dataframe.set_index("Description")
    
    
# Save html code
    facts_html = mars_facts_dataframe.to_html()

    time.sleep(5)
    
# ### Mars Hemisphere

# Mars Hemisphere URL
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemisphere_url)

    time.sleep(5)
    
# Parse HTML with Beautiful Soup
    mars_hemisphere_html = browser.html
    soup = BeautifulSoup(mars_hemisphere_html, 'html.parser')

    time.sleep(5)
    
# results are returned as an iterable list
    items = soup.find_all('div', class_='item')
    items

    titles = soup.find_all('h3')
    titles

    time.sleep(5)
    
# Parse HTML with Beautiful Soup
    mars_hemisphere_html = browser.html
    soup = BeautifulSoup(mars_hemisphere_html, 'html.parser')

    time.sleep(5)
    
# results are returned as an iterable list
    results = soup.find_all('div', class_='description')

    time.sleep(5)
    
# Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    time.sleep(5)
    
# Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    time.sleep(5)
    
# Loop through returned results
    for result in results:
        link = result.find('a')

        title = result.find('h3').text

        #Sub image url
        sub_img = result.find('a', class_='itemLink product-item')['href']

        # Browser Visit of the found link
        browser.visit(hemispheres_main_url + sub_img)
        image_html = browser.html
        soup = BeautifulSoup(image_html, 'html.parser')

        picture = soup.find('img', class_='wide-image')
        picture_img = picture['src']

        image_url = hemispheres_main_url + picture_img

        # Append information to dictionary
        hemisphere_image_urls.append({"title": title, "image_url": image_url})

# Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "mars_facts": facts_html,
        "hemispheres": hemisphere_image_urls
    }
        
# Close the browser after scraping
    browser.quit()

# Return results
    return mars_data

