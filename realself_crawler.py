############################################################################
# Instruction: A web crawler on realself.com to crawl doctors' information #
# Author: Yanzhe Li, Liyi Li                                               #
# Date: March 19 2017                                                      #
############################################################################

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

url_list = pd.read_csv('dr_lookup.csv')
df = pd.DataFrame(index=url_list.url, columns=['Name', 'Address', 'Tel'])
count = 1
for url in url_list.url:

    try:
        r = requests.get(url)
        page = BeautifulSoup(r.content, 'html.parser')
        time.sleep(5)

    except:
        print('Connection error, try again later!\n')
        continue

    if ' '.join(re.findall(r'(?:>)(.*)(?:<)', str(page.find_all('h1')))) == 'Oops - that page doesn\'t exist!':
        df.loc[url, 'Name'] = ''
        df.loc[url, 'Address'] = ''
        df.loc[url, 'Tel'] = ''
    else:
        df.loc[url, 'Name'] = ' '.join(re.findall(r'(?:>)(.*)(?:<)', str(page.find_all('h1'))))
        df.loc[url, 'Address'] = ' '.join(re.findall(r'\b(?:(?!\baddress\b|\bclass\b|\bbr\b)\w)+\b',
                                                 str(page.find_all('address', {'class': 'address'}))))
        try:
            df.loc[url, 'Tel'] = re.findall(r'(?:"telephone":")([\+\ \-0-9]+)',
                                    str(page.find_all('script', {'type': 'application/ld+json'})))[0]
        except IndexError:
            df.loc[url, 'Tel'] = ''

df.to_csv('dr_output.csv')