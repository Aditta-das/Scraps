from fastapi import FastAPI
from enum import Enum

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time

from pydantic import BaseModel

app = FastAPI()

class ModelName(str, Enum):
	posts = "Posts"
	igtv = "IGTV"
	tagged = "Tagged"

class InstaName(BaseModel):
	name: str


def scroll():
    pass


@app.get("/")
def name_specific(name: str, iterat: int, model_name: ModelName):
	# options = FirefoxOptions()
	# # options.add_argument("--headless")
	driver = webdriver.Firefox(executable_path="F:\gecko\geckodriver-v0.28.0-win64\geckodriver.exe")
	driver.implicitly_wait(30)
	url = "https://www.instagram.com/"
	driver.get(url)
	fb_login = driver.find_elements_by_xpath('//*[@id="loginForm"]/div/div[5]/button')[0].click()
	c = driver.find_element_by_xpath('//*[@id="email"]').send_keys("#")
	d = driver.find_element_by_xpath('//*[@id="pass"]').send_keys("#")
	e = driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
	time.sleep(10)
	driver.find_element_by_css_selector('button.aOOlW:nth-child(2)').click()
	
	if model_name == ModelName.posts:
		driver.get(f"https://www.instagram.com/{name}/")
		all_post = []
		det_post = []
		

		last_height = driver.execute_script("return document.body.scrollHeight")

		for _ in range(iterat):
			posts = driver.find_elements_by_class_name("v1Nh3.kIKUG._bz0w")
			for post in posts:
				post_link = post.find_element_by_tag_name('a').get_attribute('href')
				time.sleep(2)
				all_post.append(post_link)

			time.sleep(2)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)

		for de_post in all_post:
			driver.get(de_post)
			upload = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[2]/a/time').get_attribute('title')
			try:
				likes = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/a/span').text
				datas = {
					'link': de_post,
					'upload_at': upload,
					'likes': likes,
				}
				det_post.append(datas)
			except:
				views = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/span/span').text
				datas = {
					'link': de_post,
					'upload_at': upload,
					'views': views
				}
				det_post.append(datas)
				
		

		return {
			'details': det_post
		}

	if model_name == ModelName.igtv:
		igtvs = []
		
		driver.get(f"https://www.instagram.com/{name}/channel/")
		links = driver.find_elements_by_class_name('_bz0w')
		for tv in links:
			ig = tv.get_attribute('href')
			time.sleep(1)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1)
			igtvs.append(ig)
		return {
			'igtv': igtvs
		}

	if model_name == ModelName.tagged:
		return f"https://www.instagram.com/{name}/tagged/"
	
