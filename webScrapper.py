import requests
from bs4 import BeautifulSoup
import time 
import json 
import re


# retry mechanism and  data scriptiing function  
def fetch_data_with_retries(url, retries=3, delay=2):
    for attempt  in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))     #exponential backoff
    return

# function to extract data using beautifulsoup and regular expressions
def extract_data_from_html(html_content):
    if not html_content:
        return ValueError("html content is invalid !!!")
    soup = BeautifulSoup(html_content, 'html.parser')
    titles = []

    #regular expression to find all the link with the specific text (Python)
    for link in soup.find_all('a', href = True):
        title = link.get_text()
        if re.match(r'.*python.*', title, re.IGNORECASE):    #looking for links containig python 
            titles.append(title)
    return titles

#function to save the data in a json file

def save_data_to_json(data, file_name="scraped_data.json"):    
    try :
        with open(file_name, 'w') as file:
            json.dump(data, file , indent=4)
        print (f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving data to {file_name}: {e}")

#url to scrape
url = "https://docs.python.org/3/"

#fetch, extract and save the data
html_content = fetch_data_with_retries(url)
extracted_data = extract_data_from_html(html_content)
save_data_to_json(extracted_data)




