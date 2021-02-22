#!/usr/bin/env python
# coding: utf-8

# In[69]:


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[70]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[71]:

def mars_news(browser):
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[72]:


article = soup.find("div", class_='list_text')
news_title = article.find("div",class_="content_title").text
news_paragraph = soup.find("div", class_="article_teaser_body").text
print(f"Title: {news_title}")
print(f"Para: {news_paragraph}")


# JPL Mars

# In[83]:

def featured_image(browser):
url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path)
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[88]:


featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars2.jpg'
print(featured_image_url)


# Mars Facts

# In[31]:
def mars_facts():
facts_url = "https://space-facts.com/mars/"


# In[32]:


table = pd.read_html(facts_url)
table[0]


# In[34]:


df_mars = table[0]
df_mars.columns = ["Parameter","Values"]
df_mars.set_index(["Parameter"])


# In[35]:


mars_table = df_mars.to_html()
mars_table = mars_table.replace("\n", "")
mars_table


# Mars Hemisphere

# In[64]:

def hemisphere(browser):
    
import time
Hemi_Url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(Hemi_Url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")
mars_hemispheres = []


# In[65]:


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


# In[66]:


return mars_hemispheres


# In[ ]:

def scrape_all():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())
