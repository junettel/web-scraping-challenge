import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time


"""
======================================

Step 2 - MongoDB and Flask Application

Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

* Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will 
  execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
* Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
  * Store the return value in Mongo as a Python dictionary.
* Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
* Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate 
  HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.

======================================
"""


def init_browser():
	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=False)


def scrape():

	browser = init_browser()

	mars_scrape_data_dict = {}
	sleep_timer = 2

	# NASA Mars News
	
	title_list=[]
	txt_list=[]
	link_list=[]

	url = "https://mars.nasa.gov/news/"
	browser.visit(url)
	time.sleep(sleep_timer)
	html = browser.html 
	soup = bs(html,"html.parser")
	results = soup.find_all('li', class_="slide")

	for result in results:
		try:
			title_list.append(result.find(class_="content_title").text)
			txt_list.append(result.find(class_="rollover_description_inner").text)
			link_list.append("https://mars.nasa.gov" + result.a['href'])

		except AttributeError as e: # Error handling
			print(e)

	mars_scrape_data_dict['news_title'] = title_list[0] 
	mars_scrape_data_dict['news_paragraph'] = txt_list[0]
	mars_scrape_data_dict['news_url'] = link_list[0]


	# JPL Mars Space Images

	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" 
	browser.visit(url) 
	time.sleep(sleep_timer) 
	browser.find_by_css('.fancybox').click() 
	time.sleep(sleep_timer) 
	browser.click_link_by_partial_text('more info')
	#browser.links.find_by_partial_text('more info').click() 
	time.sleep(sleep_timer) 
	html = browser.html 
	soup = bs(html,"html.parser")
	results = soup.find_all(class_="download_tiff")
	image_link = results[1].a['href'] 
	featured_image_url = "https:" + image_link 

	# result to mongoDB dictionary
	mars_scrape_data_dict['featured_image_url'] = featured_image_url


	# Mars Weather
	import re
	url = "https://twitter.com/MarsWxReport" 
	browser.visit(url)
	time.sleep(sleep_timer) 
	html = browser.html 
	soup = bs(html,"html.parser")
	mars_weather=soup.find(text=re.compile("InSight sol")) 
	#print(mars_weather)

	# result to mongoDB dictionary
	mars_scrape_data_dict['weather'] = mars_weather


	# Mars Facts

	url = "https://space-facts.com/mars/" 
	tables = pd.read_html(url) 
	mars_table_df = tables[0]
	mars_table_df.columns = ["Description", "Info"] 
	mars_table_df.set_index('Description', inplace=True) 

	mars_html_table = mars_table_df.to_html() 
	mars_html_table = mars_html_table.replace("\n", "")

	# result to mongoDB dictionary
	mars_scrape_data_dict['facts'] = mars_html_table


	# Mars Hemispheres
	hemisphere_img_urls = []

	## Cerberus
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars" 
	browser.visit(url)
	time.sleep(sleep_timer) 
	browser.click_link_by_partial_text('Cerberus')
	#browser.links.find_by_partial_text('Cerberus').click() 
	time.sleep(sleep_timer) 
	html = browser.html 
	soup = bs(html,"html.parser")

	results_link_01 = soup.find(class_="downloads").a['href']
	results_title_01 = soup.find('h2', class_="title").text 

	dictionary_entry_01 = {"title":results_title_01, "image_url": results_link_01} 
	hemisphere_img_urls.append(dictionary_entry_01)

	browser.back() 

	## Schiaparelli
	time.sleep(sleep_timer) 
	browser.click_link_by_partial_text('Schiaparelli')
	#browser.links.find_by_partial_text('Schiaparelli').click() 
	time.sleep(sleep_timer) 
	html = browser.html 
	soup = bs(html,"html.parser")

	results_link_02 = soup.find(class_="downloads").a['href'] 
	results_title_02 = soup.find('h2', class_="title").text 

	dictionary_entry_02 = {"title":results_title_02, "image_url": results_link_02} 
	hemisphere_img_urls.append(dictionary_entry_02) 

	browser.back() 

	## Syrtis
	time.sleep(sleep_timer) 
	browser.click_link_by_partial_text('Syrtis')
	#browser.links.find_by_partial_text('Syrtis').click() 
	time.sleep(sleep_timer) 
	html = browser.html 
	soup = bs(html,"html.parser")

	results_link_03 = soup.find(class_="downloads").a['href'] 
	results_title_03 = soup.find('h2', class_="title").text 

	dictionary_entry_03 = {"title":results_title_03, "image_url": results_link_03}
	hemisphere_img_urls.append(dictionary_entry_03) 

	browser.back() 

	## Valles
	time.sleep(sleep_timer) 
	browser.click_link_by_partial_text('Valles')
	#browser.links.find_by_partial_text('Valles').click() 
	time.sleep(sleep_timer) 
	html = browser.html 
	soup = bs(html,"html.parser")

	results_link_04 = soup.find(class_="downloads").a['href']
	results_title_04 = soup.find('h2', class_="title").text 

	dictionary_entry_04 = {"title":results_title_04, "image_url": results_link_04} 
	hemisphere_img_urls.append(dictionary_entry_04) 

	browser.quit() 

	# result to mongoDB dictionary
	mars_scrape_data_dict["hemisphere_img_url"] = hemisphere_img_urls

	print("puhhhh all done scraping ... I'm tiered now")

	return mars_scrape_data_dict 