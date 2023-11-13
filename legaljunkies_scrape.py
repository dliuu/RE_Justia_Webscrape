"""clean_rawURLS.ipynb

Takes a directory of URLs and looks for URLs that start with the starting slug
"""

import pandas as pd
import numpy as np
import os
import requests
import json
import urllib.request
from bs4 import BeautifulSoup
import csv


def question_lookup(url_list:list, sub_url:str):
  '''Util Function: Iterates through the list of raw URLs and returns a list of URLs that only contain the 
  desired sub-url
  '''
  return_list = []
  for url in url_list:
      if url.startswith(sub_url):
          return_list.append(url)
  return return_list



def directory_to_cleaned_list(dir:str, sub_url: str):
  '''Iterates through all files of a dictionary and returns a list of URLs 
  matching the sub url.
  '''
  cleaned_URLs = []

  for fname in os.listdir(dir):
    f = f = os.path.join(dir, fname)
    print('reading file: ' + str(fname))
    df = pd.read_csv(f)

    all_urls = df['Unnamed: 1'].tolist()
    all_urls = all_urls[1:]
    question_urls = question_lookup(all_urls, sub_url)
  
    for url in question_urls:
      cleaned_URLs.append(url)

  #Drop duplicate URLs in cleaned list
  unique_URLs = []
  for url in cleaned_URLs:
      if url not in unique_URLs:
          unique_URLs.append(url)
  
  return unique_URLs

  #print('length of cleaned URL list: ' + str(len(unique_URLs)))

def scrape(url:str, filename:str):
  ''' Takes a url from the Question page of Justia and outputs a dictionary in the form:
  {question_title: question_title,
  question_description: question_description,
  answer1: (answer1, upvote_count),
  answer2: (answer2, upvote_count)}
  '''
  print('scraping ' + str(url))
  return_dict = {}

  apikey = '4916e294a8357d561fab297cbd2089552578b2bc'
  params = {
    'url': url,
    'apikey': apikey,
    'js_render': 'true',
    'antibot': 'true',
    'premium_proxy': 'true',
}
  response = requests.get('https://api.zenrows.com/v1/', params=params)

  soup = BeautifulSoup(response.text, 'html.parser')
  data = soup.find_all('div', {"js-post__content-text restore h-wordwrap"})

  with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        rows=[]
        header = ['scraped_text']

        rows.append([data])

        #check if file exists
        file_exists = os.path.isfile(filename)
        
        if not file_exists:
            writer.writerow(header)

        writer.writerows(rows)

def save_to_csv(data, filename):
    header = ['question_title', 'question_description', 'answer', 'upvote_count']

    rows = []
    for key, value in data.items():
        if key.startswith('answer'):
            answer, upvote_count = value
            question_title = data['question_title']
            question_description = data['question_description']
            rows.append([question_title, question_description, answer, upvote_count])

    #Check if file exists --> append header if not
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        if not file_exists:
            writer.writerow(header)

        writer.writerows(rows)

#__Main__

directory = 'Justia_rawURLs'
url = "https://forum.legaljunkies.com/forum/real-estate-and-property-law/buying-and-selling-property/mortgages-refinancing-foreclosure/658349-what-is-the-proof-of-income-for-a-mortgage-loan"

scrape(url, 'legaljunkies_test.csv')





'''
 apikey = '4916e294a8357d561fab297cbd2089552578b2bc'
params = {
    'url': url,
    'apikey': apikey,
    'js_render': 'true',
    'antibot': 'true',
    'premium_proxy': 'true',
}
response = requests.get('https://api.zenrows.com/v1/', params=params)
#print(response.text)


soup = BeautifulSoup(response.text, 'html.parser')
data = soup.find_all('div', {"js-post__content-text restore h-wordwrap"})
print(data)
'''

#url_list = directory_to_cleaned_list(directory)
#for url in url_list:
#save_to_csv(scrape(url), 'Justia_data.csv')

