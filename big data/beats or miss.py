from bs4 import BeautifulSoup
import requests
import time



headers = {'User-Agent': 'Mozilla/5.0 '}

file = open("BPOP.txt")


cnames = []
wcontent = ''

while 1:
    line = file.readline()
    cnames.append(line.split('\n')[0])

    if not line:
        break


for cname in cnames:
    time.sleep(0.5)
    start_url = 'https://seekingalpha.com/symbol/' + cname + '/earnings'
    print(start_url)
    wb_data = requests.get(start_url, headers=headers)
    Soup = BeautifulSoup(wb_data.text, 'lxml')
    contents = Soup.select('#accordion h4 a ')
    for content in contents:
        # print(content.get_text())
        wcontent = wcontent + content.get_text() + '\n'
    print(wcontent)

    if(len(wcontent)):
        filename = './1/' + cname + '.txt'
        print(filename)
        wcontent = wcontent
        f = open(filename, 'w')
        f.write(wcontent)
        f.close()
        wcontent = ''
        name = ''
    else:
        print('fail to get page')
