"""clean_rawURLS.ipynb

Takes a directory of URLs and looks for URLs that start with the starting slug
"""

import pandas as pd
import numpy as np
import os

def question_lookup(url_list):
  return_list = []
  for url in url_list:
      if url.startswith("https://answers.justia.com/question/"):
          return_list.append(url)
  return return_list

directory = 'Justia_rawURLs'
cleaned_URLs = []

for fname in os.listdir(directory):
  f = f = os.path.join(directory, fname)
  print('reading file: ' + str(fname))
  df = pd.read_csv(f)

  all_urls = df['Unnamed: 1'].tolist()
  all_urls = all_urls[1:]

  question_urls = question_lookup(all_urls)
  
  for url in question_urls:
    cleaned_URLs.append(url)

#Drop non-unique elements in cleaned list
unique_URLs = []

for url in cleaned_URLs:
    if url not in unique_URLs:
        unique_URLs.append(url)

print('length of cleaned URL list: ' + str(len(unique_URLs)))