from bs4 import BeautifulSoup
import requests
import time



headers = {'User-Agent': 'Mozilla/5.0 '}

file = open("BPOP.txt")

cnames = []
while 1:
    line = file.readline()
    cnames.append(line.split('\n')[0])

    if not line:
        break



for cname in cnames:
    print(cname)
    #read one name 
    start_url = 'https://seekingalpha.com/symbol/'+cname+'/earnings/transcripts'
    print(start_url)
    wb_data = requests.get(start_url, headers=headers)
    Soup = BeautifulSoup(wb_data.text, 'lxml')
    links = Soup.select('#headlines_transcripts  div  ul  li  div.content > div > a')
    linklist = []
    for link in links:
        if link.get_text().find('Transcript') > 0:
            linklist.append('https://seekingalpha.com' + link.get('href'))

    #all links in linklist
    print(linklist)

    for onelink in linklist:
        time.sleep(0.5)
        print(onelink)
        url = onelink
        wb_data = requests.get(url, headers=headers)
        Soup = BeautifulSoup(wb_data.text, 'lxml')


        name = cname
        titleline = Soup.select('#a-hd > h1')  #取出title
        print(titleline)
        #if successfully read
        if(len(titleline)):
            title = titleline[0].get_text()
            #file name
            name = name + '-' + title[title.find('Q'):title.find('Q') + 2] + '-' + title[title.find('Q') + 3:title.find('Q') + 7]
            #print(name)

            wcontent = ''
            #main context
            contexts = Soup.select('#a-body > p.p.p1')
            for context in contexts:
                context = context.get_text()
                wcontent = wcontent + context + '\n'

            wcontent = wcontent.encode('ascii', 'ignore').decode('ascii')
            # print(type(wcontent))
            #write into txt
            filename = name + '.txt'
            f = open(filename, 'w')
            f.write(wcontent)
            f.close()
            wcontent = ''
            name = ''
        #can't read
        else:
            time.sleep(2)
            #wait 2 seconds reread
            titleline = Soup.select('#a-hd > h1')
            if (len(titleline)):
                title = titleline[0].get_text()
                name = name + '-' + title[title.find('Q'):title.find('Q') + 2] + '-' + title[title.find('Q') + 3:title.find('Q') + 7]
                # print(name)

                wcontent = ''
                contexts = Soup.select('#a-body > p.p.p1')
                for context in contexts:
                    context = context.get_text()
                    wcontent = wcontent + context + '\n'

                wcontent = wcontent.encode('ascii', 'ignore').decode('ascii')
                # print(type(wcontent))
                filename = name + '.txt'
                f = open(filename, 'w')
                f.write(wcontent)
                f.close()
                wcontent = ''
                name = ''
            else:
                #print(Soup)
                print('fali to read this page')