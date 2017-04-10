############################################################################
# Instruction: transcripts crawler on SeekingAlpha.com                     #
# Version: 2.0                                                             #
# Date: April 08 2017                                                      #
############################################################################

from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

class tscpCrawler():
    def __init__(self, ticker, user_name=None, pwd=None):
        self.ticker = ticker.upper()
        self.headers = {'User-Agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
               'AppleWebKit/537.36 (KHTML, like Gecko)'
               'Chrome/39.0.2171.95 '
               'Safari/537.36'}
        self.user_name = user_name
        self.pwd = pwd

    def links(self):
        allLinks = []
        page = 1
        flag = 2
        while page < 10 and flag:
            url = 'https://seekingalpha.com/symbol/' + self.ticker + '/earnings/more_transcripts?page=' + str(page)
            wb = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(wb.text, 'lxml')
            if not soup.select('div div a'):
                break
            else:
                for i in soup.select('div div a'):
                    if i.get('href').strip('\"\\') == 'https://www.perimeterx.com':
                        time.sleep(600)
                        page = 1
                        flag -= 1
                        continue
                    elif i.get('href').strip('\"\\').find('transcript') > 0:
                        allLinks.append('https://seekingalpha.com' + i.get('href').strip('\"\\') + '?part=single')

            page += 1

            time.sleep(10)

        return allLinks

    def transcripts(self):

        with requests.Session() as c:
            requestUrl = 'http://seekingalpha.com/account/orthodox_login'

            USERNAME = self.user_name
            PASSWORD = self.pwd

            userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'

            login_data = {
                "slugs[]": None,
                "rt": None,
                "user[url_source]": None,
                "user[location_source]": "orthodox_login",
                "user[email]": USERNAME,
                "user[password]": PASSWORD
            }

            c.post(requestUrl, data=login_data,
                   headers={"referer": "http://seekingalpha.com/account/login", 'user-agent': userAgent})

            df = pd.DataFrame(columns=['Ticker', 'Date', 'Time', 'Links'])

            for ind, link in enumerate(self.links()):

                page = c.get(link, headers=self.headers)
                soup = BeautifulSoup(page.text, 'lxml')
                titleline = soup.select('#a-hd > h1')
                try:
                    title = titleline[0].get_text()
                    file_name = self.ticker + '-' + title[title.find('Q'):title.find('Q') + 2] + '-' \
                                + title[title.find('Q') + 3:title.find('Q') + 7] + '.txt'
                    contexts = '\n'.join([text.get_text() for text in soup.select('#a-body > p.p')])

                    df.loc[ind, 'Ticker'] = self.ticker
                    df.loc[ind, 'Links'] = link
                    df.loc[ind, 'Date'] = soup.select('#a-body > p.p.p1')[1].get_text()
                    df.loc[ind, 'Time'] = soup.select('#a-body > p.p.p1')[2].get_text()

                    with open(r'all_output/'+file_name, 'w') as f:
                        f.write(contexts)
                except IndexError:
                    df.loc[ind, 'Ticker'] = self.ticker
                    df.loc[ind, 'Links'] = link
                    print(link)
                    continue
                except FileNotFoundError as error:
                    print(error)
                    pass

                time.sleep(60)

            if not df.empty:
                df.to_csv(r'all_output/'+self.ticker+'_data.csv')


if __name__ == '__main__':
    user_info = {'user_name': 'maxwelllee54@gmail.com',
                 'pwd': 'lee890504'}
    ticker_list = ['RIO', 'XOM', 'GE', 'F', 'MO', 'XRX', 'GS', 'HBC', 'JPM', 'LYG', 'MS', 'RF']
    #ticker_list = pd.read_csv('ticker_list.txt', header=None).iloc[:,0]
    for ticker in ticker_list:

        print(ticker)
        tscpCrawler(ticker, **user_info).transcripts()
        time.sleep(60)








