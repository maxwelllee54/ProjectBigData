############################################################################
# Instruction: transcripts crawler on SeekingAlpha.com                     #
# Date: April 05 2017                                                      #
############################################################################

from bs4 import BeautifulSoup
import requests
import time
import re
import pandas as pd
import numpy as np
from newspaper import Article
import os


class tscpCrawler():
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.headers = {'User-Agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
               'AppleWebKit/537.36 (KHTML, like Gecko)'
               'Chrome/39.0.2171.95 '
               'Safari/537.36'}
        self.url = 'https://seekingalpha.com/search/transcripts?term='+ ticker + '&all=true'

    def links(self):
        allLinks = []
        try:
            s = requests.Session()
            r = s.get(self.url, headers=self.headers)
            time.sleep(3)
            page = BeautifulSoup(r.content, 'html.parser')
            pageNo = re.findall(r'(?:>)(\d+)(?:<)', str(page.find_all('div', {'id': 'paging'})))

            print(page)

            for p in pageNo:
                pageUrl = self.url+'&page='+p
                newS = requests.Session()
                newR = newS.get(pageUrl, headers=self.headers)
                time.sleep(3)
                newPage = BeautifulSoup(newR.content, 'html.parser')

                links = re.findall(r'(?:href=")(.*?)(?:">)', str(newPage.find_all('div', {'class': 'transcript_link'})))
                allLinks.extend(links)
            # remove old links
            try:
                df = pd.read_csv('output.xlsx', self.ticker)
                oldLink = list(df.loc[:, 'Link'])
                return [newLink for newLink in allLinks if newLink not in oldLink]
            except:
                print('\n\nNo previous records!\n\n')
                pass

            return allLinks

        except:
            print('Connection Error!\n')
            return allLinks

    '''def transcripts(self, links=None):
        if not links:
            links = self.links()

        textData = pd.DataFrame(index=np.arange(len(links)), columns=['Company', 'Date', 'Time', 'Text'])

        for i in range(len(links)):
            tscpSession = requests.Session()
            tscp = tscpSession.get('https://seekingalpha.com'+links[i], headers=self.headers)
            time.sleep(3)
            tscpPage = BeautifulSoup(tscp.content, 'html.parser')
            content = tscpPage.find_all('p', {'class': 'p'})
            print(i)
            try:
                textData.loc[i, 'Company'] = content[0].get_text()
                textData.loc[i, 'Date'] = content[1].get_text()
                textData.loc[i, 'Time'] = content[2].get_text()
                textData.loc[i, 'Text'] = '\n'.join([t.get_text() for t in content[3:]])
            except IndexError:
                print(textData)
                print(tscpPage)
                continue

        textData.to_csv('data.csv')'''

    def artical(self, links=None):

        if not links:
            links = self.links()

        print(links)

        textData = pd.DataFrame(columns=['Company', 'Ticker', 'Date', 'Time', 'Text', 'Link'])
        fileName = 'output.xlsx'

        if os.path.isfile(fileName) == False:
            mode = 'w'
            header = True
        else:
            mode = 'a'
            header = False

        for i in range(len(links)):
            link = 'https://seekingalpha.com' + links[i]
            print(link)
            art = Article(link, language='en', fetch_images=False, memoize_articles=False)
            art.download()
            try:
                art.parse()
            except:
                continue
            content = re.split(r'\n+', art.text)
            print(content)
            try:
                textData.loc[i, :] = [content[0], self.ticker, content[1],
                                      content[2], '\t'.join([t for t in content[3:]]), links[i]]
                print(textData)

            except IndexError:
                print(content)
                print(i)
                continue
        print(textData)

        if not textData.empty:
            writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
            textData.to_excel(writer, self.ticker)
            writer.save()


if __name__ == '__main__':
    tscpCrawler('GS').artical()







