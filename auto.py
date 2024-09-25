from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd


# Configure the Chrome driver (or another browser you prefer)
service = Service('/usr/local/bin/chromedriver-linux64/chromedriver')
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

# Google Scholar URL 
url = ""

# Access the page
driver.get(url)

data = []
counter = 1

# Loop until there is no longer a "next" page
while True:
    time.sleep(2) 

    # Finds all elements that match article links
    articles = driver.find_elements(By.CSS_SELECTOR, 'h3.gs_rt a')

    # Finds all elements that correspond to the years of publication
    years = driver.find_elements(By.CSS_SELECTOR, 'div.gs_a')

    print(f"Page {counter} results")

    for article, year in zip(articles, years):
        # Getting the article link
        article_link = article.get_attribute('href')

        # Extracting the year of publication
        year_text = year.text
        try:
           
            year_pub = [int(s) for s in year_text.split() if s.isdigit()][-1]
        except IndexError:
            year_pub = 0 # year not found
        
        # Add data to the list
        data.append([article.text, article_link, year_pub])

        # Displaying the result
        print(f"title: {article.text} link: {article_link}, year: {year_pub}")
    
    # Try to find the 'Next' button (or similar) to move to the next page
    try:
        next_button = driver.find_element(By.LINK_TEXT, 'Mais')
        next_button.click() 
    except:
        print("Last page reached.")
        break

    counter += 1


driver.quit()

df = pd.DataFrame(data, columns=['title', 'link', 'year'])

# Save the DataFrame to a CSV file
df.to_csv('articles_scholar.csv', index=False)
print("Data save in 'articles_scholar.csv'")
