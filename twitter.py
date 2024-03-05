# Set up the Selenium WebDriver (replace with the path to your ChromeDriver)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
import chromedriver_binary
from urllib.request import urlopen
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver as selenium_webdriver
import time
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.common.by import By
from googletrans import Translator
service = Service(executable_path='D:/MaiTexa/projects/safi/safi/Safi_BSC/twitter_deploy/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
# pswd=scrapy673002
# user=scrapy632356143

driver.get("https://twitter.com/explore")
driver.maximize_window()
time.sleep(3)
username = driver.find_element(By.CLASS_NAME,"r-1dz5y72.r-13qz1uu")     
# username.click()
username.send_keys("scrapy632356143")  
time.sleep(3)                      
next=driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
next.click()
time.sleep(3)
password = driver.find_element(By.CLASS_NAME,"r-deolkf.r-homxoj ")     
# password.click()
password.send_keys("scrapy673002")  
time.sleep(3)                        
login=driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
login.click()
time.sleep(4)

explore=driver.find_element(By.XPATH,'//*[@data-testid="AppTabBar_Explore_Link"]')
explore.click()
time.sleep(2)

search_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'

# Find the search element and send keys
search_element = driver.find_element(By.XPATH, search_xpath)
search_element.send_keys("navakerala")
search_element.send_keys(Keys.ENTER)
time.sleep(3)

total_height = int(driver.execute_script("return document.body.scrollHeight"))
for i in range(1, total_height, 5):
    driver.execute_script("window.scrollTo(0, {});".format(i))
data= driver.find_elements(By.XPATH,'//*[@data-testid="tweetText"]')
twit1=[]

for d in data:
    print(d.text)
    twit1.append(d.text)


df=pd.DataFrame({'post':twit1})

# df.to_csv('twitter_data11111111.csv')

from transformers import pipeline


translator = Translator()
df['post'] = df['post'].apply(lambda x: translator.translate(x, dest='en').text)
df = df['post']

nlp_sentence = pipeline('sentiment-analysis')

def predict_toxicity(comment):
    sentiment = nlp_sentence(comment)
    return sentiment[0]['label']
def count_toxicity(df):
    positive_count = 0
    negative_count = 0
    for comment in df:
        sentiment = predict_toxicity(comment)
        if sentiment == 'NEGATIVE':
            positive_count += 1
        else:
            negative_count += 1
    
    total_comments = positive_count + negative_count
    positive_percentage = (positive_count / total_comments) * 100
    negative_percentage = (negative_count / total_comments) * 100
    return positive_percentage, negative_percentage

positive_percentage, negative_percentage = count_toxicity(df)
print(f"Percentage of Positive comments: {positive_percentage:.2f}%")
print(f"Percentage of Negative comments: {negative_percentage:.2f}%")

