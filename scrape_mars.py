#!/usr/bin/env python
# coding: utf-8

# In[43]:


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import pandas as pd


# In[44]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[45]:


conn = 'mongodb://localhost:27017'
Mars_db = pymongo.MongoClient(conn)
db = Mars_db
collection = db.items
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[46]:
url = "https://mars.nasa.gov/news/"
browser.visit(url)
article = soup.find("div", class_='list_text')
news_title = article.find("div",class_="content_title").text
news_paragraph = soup.find("div", class_="article_teaser_body").text
print(f"Title: {news_title}")
print(f"Para: {news_paragraph}")


# JPL Mars

# In[47]:


J_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path)
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[48]:


featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars2.jpg'
print(featured_image_url)


# Mars Facts

# In[49]:


facts_url = "https://space-facts.com/mars/"


# In[50]:


table = pd.read_html(facts_url)
table[0]


# In[51]:


df_mars = table[0]
df_mars.columns = ["Parameter","Values"]
df_mars.set_index(["Parameter"])


# In[52]:


mars_table = df_mars.to_html()
mars_table = mars_table.replace("\n", "")
mars_table


# Mars Hemisphere

# In[53]:
Hemi_Url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(Hemi_Url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")
mars_hemispheres = []


# In[54]:
products = soup.find("div", class_ = "result-list" )
hemispheres = products.find_all("div", class_="item")
for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    Hemi_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(Hemi_link)
    html = browser.html
    soup=BeautifulSoup(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    mars_hemispheres.append({"title": title, "img_url": image_url})
    links = browser.find_by_css("a.product-item h3")
# In[55]:


mars_hemispheres


# In[ ]:
def scrape_all():
    mars_data ={
		'news_title' : news_title,
		'paragraph': news_paragraph,
        'featured_image': featured_image_url,
		'fact_table': mars_table,
		'hemisphere_image': mars_hemispheres,
        'url': url,
        'J_url': J_url,
        'facts_url': facts_url,
        'hemisphere_url': Hemi_Url,
        }
collection.insert(mars_data)
    return mars_data
if __name__ == "__main__":
    print(scrape_all())