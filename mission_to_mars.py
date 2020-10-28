#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Declare Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time


# ### Step 1 - Scraping from NASA Mars News

# In[2]:


# Windows Users Chromedriver.exe setup
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Define URL to scrape and inform the browser to visit the page
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[4]:


# HTML Object
html = browser.html


# In[5]:


# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

#soup.prettify()


# In[6]:


# Using Beautiful Soup, we can find News Title and Paragraph Content. results = soup.find_all("div", class_="slide")

news_title = soup.find('li', attrs={'class': 'slide'}).find('h3').text

news_p = soup.find('div', class_='article_teaser_body').text

print(news_title)
print(news_p)


# ### JPL Mars Space Images - Featured Image

# In[7]:


# Windows Users Chromedriver.exe setup
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[8]:


image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(image_url)


# In[9]:


# Click to find full large image
browser.click_link_by_partial_text('FULL IMAGE')


# In[10]:


# Click to find full large image
time.sleep(2)
browser.click_link_by_partial_text('more info')


# In[11]:


# HTML Object 
html_image = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html_image, 'html.parser')
# soup.prettify()


# In[12]:


# Retrieve background image
results = soup.find('figure', class_="lede")
results.prettify()


# In[13]:


href = results.a['href']
print(href)


# In[14]:


# Create website url with scrapped route
featured_image_url = 'https://www.jpl.nasa.gov' + href

# Display full link to featured image
featured_image_url


# In[ ]:





# ### Mars Facts

# In[15]:


# Mars Facts URL
mars_facts_url = 'http://space-facts.com/mars/'


# In[16]:


# Read html and parse
mars_facts = pd.read_html(mars_facts_url)


# In[17]:


# Find mars facts dataframe in list of dataframe
mars_facts_dataframe = mars_facts[0]
mars_facts_dataframe


# In[18]:


# Assign Column names and set index. Display final datframe

mars_facts_dataframe.columns = ["Description", "Measurement"]
mars_facts_dataframe = mars_facts_dataframe.set_index("Description")
mars_facts_dataframe


# In[19]:


# Save html code
mars_facts_dataframe.to_html()


# ### Mars Hemisphere

# In[20]:


# Windows Users Chromedriver.exe setup
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[21]:


# Mars Hemisphere URL
mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(mars_hemisphere_url)


# In[22]:


# Parse HTML with Beautiful Soup
mars_hemisphere_html = browser.html
soup = BeautifulSoup(mars_hemisphere_html, 'html.parser')


# In[23]:


# results are returned as an iterable list
items = soup.find_all('div', class_='item')
items


# In[24]:


titles = soup.find_all('h3')
titles


# In[25]:


# Parse HTML with Beautiful Soup
mars_hemisphere_html = browser.html
soup = BeautifulSoup(mars_hemisphere_html, 'html.parser')

# results are returned as an iterable list
results = soup.find_all('div', class_='description')

# Create empty list for hemisphere urls 
hemisphere_image_urls = []

# Store the main_ul 
hemispheres_main_url = 'https://astrogeology.usgs.gov'

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

# Display full link to featured image
hemisphere_image_urls


# In[ ]:




