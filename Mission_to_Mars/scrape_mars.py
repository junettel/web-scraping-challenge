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


def mars_scrape():

	browser = init_browser()

	mars_scrape_data_dict = {}
	sleep_time = 2

	# ----- NASA Mars News ----- #

	news_title_list = []
	news_p_list = []
	news_href_list = []

	news_url = "https://mars.nasa.gov/news/"
	browser.visit(news_url)
	time.sleep(sleep_time)

	html = browser.html
	soup = bs(html, 'html.parser')

	# News articles iterable list
	articles = soup.find_all('li', class_='slide')

	for article in articles:
		try:
			# Scrape title, paragraph text, link href
			news_title = article.find(class_='content_title').text
			news_p = article.find(class_='article_teaser_body').text
			news_href = article.find('a')['href']

			# Append variable lists with each iteration
			news_title_list.append(news_title)
			news_p_list.append(news_p)
			news_href_list.append(news_href)

		except:
			print('*** Error! ***')

	# Result to mongoDB dictionary
	mars_scrape_data_dict['news_title'] = news_title_list[0] 
	mars_scrape_data_dict['news_paragraph'] = news_p_list[0]
	mars_scrape_data_dict['news_url'] = news_href_list[0]


	# ----- JPL Mars Space Images - Featured Image ----- #

	image_url_base = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
	image_url = f'{image_url_base}index.html'
	browser.visit(image_url)
	time.sleep(sleep_time)

	# Click link to find featured image
	browser.click_link_by_partial_text('FULL IMAGE')
	time.sleep(sleep_time)
	image_html = browser.html
	image_soup = bs(image_html, 'html.parser')

	# Find featured image and scrape url
	featured_image = image_soup.find(class_='fancybox-image')['src']
	featured_image_url = image_url_base + featured_image
	time.sleep(sleep_time)

	# Result to mongoDB dictionary
	mars_scrape_data_dict['featured_image_url'] = featured_image_url


	# ----- Mars Facts ----- #

	table_url = 'https://space-facts.com/mars/'
	mars_table = pd.read_html(table_url)

	# Scrape table containing facts and write to html
	mars_table_df = mars_table[0]
	mars_table_df.columns = ['Description', 'Value']
	mars_table_df.set_index('Description', inplace=True)
	mars_table_html = mars_table_df.to_html()
	mars_table_html = mars_table_html.replace('\n', '')

	# Result to mongoDB dictionary
	mars_scrape_data_dict['facts'] = mars_table_html


	# ----- Mars Hemispheres ----- #

	hemisphere_image_urls = []

	hemi_url_base = 'https://astrogeology.usgs.gov/'
	hemi_url = f'{hemi_url_base}search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hemi_url)
	time.sleep(sleep_time)

	hemi_html = browser.html
	hemi_soup = bs(hemi_html, 'html.parser')

	# Hemisphere items returned in an iterable list
	hemis = hemi_soup.find_all('div', class_='item')

	for hemi in hemis:
		# Scrape title and href for image link
		title = hemi.find('h3').text
		hemi_href = hemi.find('a', class_="itemLink product-item")["href"]
		time.sleep(sleep_time)
		
		# Click link to find full res image url
		browser.visit(hemi_url_base + hemi_href)
		time.sleep(sleep_time)
		
		# Iteration html and soup
		hemi_loop_html = browser.html
		hemi_loop_soup = bs(hemi_loop_html, 'html.parser')
		
		# Scrape full res image url
		img_url = hemi_loop_soup.find(class_='downloads').a['href']
		print(img_url)
		
		# Add to list
		hemisphere_image_urls.append({'title': title, 'img_url': img_url})
		time.sleep(sleep_time)

	# Result to mongoDB dictionary
	mars_scrape_data_dict["hemisphere_image_url"] = hemisphere_image_urls

	browser.quit()

	print("Web scrape complete!")

	return mars_scrape_data_dict 