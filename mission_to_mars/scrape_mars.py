from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrape():

    #----- Get latest Mars news from NASA site----

    url_nasa = "https://mars.nasa.gov/news/"

    response_nasa = requests.get(url_nasa)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response_nasa.text, 'html.parser')

    # Finds news title based on its div class

    news_title = soup.find('div', class_="content_title").find('a').text

    # Finds news summary based on its div class

    news_p = soup.find('div', class_="rollover_description_inner").text



    #--- Get newest Mars image from JPL site----

    #-- NOT ABLE TO RELIABLY GET MARS IMAGE WITHOUT CRASHING__ REMOVED CODE--

    #---------------
    # Scrape Twitter for latest Mars weather--------

    url_twitter = "https://twitter.com/marswxreport?lang=en"

    response_twitter = requests.get(url_twitter)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_twitter = BeautifulSoup(response_twitter.text, 'html.parser')

    # Finds latest tweet based on class

    mars_weather = soup_twitter.find('div', class_="js-tweet-text-container").find('p').text



    # ---------Uses Pandas to scrape tables from Mars facts site--------
    url_facts = "https://space-facts.com/mars/"

    tables = pd.read_html(url_facts)

    # Creates a dataframe from the first table

    facts_df = tables[0]

    # Creates an html table from the df, leaving off the header row and index column

    facts_html = facts_df.to_html(header = False, index = False)

    #----- Scrapes USGS site for Mars hemispere images----------

   #Scrapes main page that houses links to Mars Hemisphere images

    url_usgs = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    response_usgs = requests.get(url_usgs)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_usgs = BeautifulSoup(response_usgs.text, 'html.parser')

    # Gets image link for each hemisphere

    # Enables string search within href
    import re

    # Creates list of dictionaries to store urls
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere","short_name":"cerberus","img_url": ""},
        {"title": "Schiaparelli Hemisphere","short_name":"schiaparelli","img_url": ""},
        {"title": "Syrtis Major Hemisphere","short_name":"syrtis_major","img_url": ""},
        {"title": "Valles Marineris Hemisphere","short_name":"valles_marineris","img_url": ""}
        ]

    # Loops through the four hemispheres
    for hemisphere in hemisphere_image_urls:

        # Gets link from main page to hemisphere page, using the short name
        hemi_link = soup_usgs.find(href=re.compile(hemisphere["short_name"])).get('href')
        
        response_hemi = requests.get("https://astrogeology.usgs.gov" + hemi_link)

        # Create BeautifulSoup object for that hemisphere's page and gets the link for image
        soup_hemi = BeautifulSoup(response_hemi.text, 'html.parser')
        
        image_src = soup_hemi.find('img', class_='wide-image').get('src')
        
        image_link = ("https://astrogeology.usgs.gov" + image_src)
        
        # Inserts link into the hemisphere image urls list
        
        hemisphere["img_url"] = image_link


        # --------Dictionary for storing all the scraped Mars Data

    mars_data_dict = {"NewsTitle":news_title, 
                    "NewsSummary":news_p, 
                    "MarsWeather":mars_weather,
                    "MarsFacts":facts_html,
                    "Hemi1url":hemisphere_image_urls[0]['img_url'],
                    "Hemi2url":hemisphere_image_urls[1]['img_url'],
                    "Hemi3url":hemisphere_image_urls[2]['img_url'],
                    "Hemi4url":hemisphere_image_urls[3]['img_url']
                    }


    return mars_data_dict