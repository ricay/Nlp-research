import requests
from bs4 import BeautifulSoup
import nltk
import numpy
import re
import io
import csv


def request(url):
    result = requests.get(url)
    # ensure that we obtain a 200 OK response to indicate
    # print(result.status_code)

    src = result.content
    soup = BeautifulSoup(src, features="html.parser")
    return soup

def program_name(soup):
#name on home page
    chair = soup.find(text ='General Chair:')
    chair_name = chair.findNext('div').contents[0]

    cochair = soup.find(text = 'Program Cochairs:')
    cochair_name = cochair.findNext('div').contents[0]
    next_one = cochair_name.next_element.next_element.get_text()

    file_name = open("organization_name.txt","w")

    file_name.writelines(chair +'\n')
    file_name.writelines(chair_name +'\n')
    file_name.write(cochair +'\n')
    file_name.write(cochair_name +'\n')
    file_name.write(next_one +'\n')
    file_name.close()

def get_all_links(soup):
# all relevant links
    all_links = soup.find_all("a")
    should = ['senior', 'committee', 'chairs']

    links = []
    for link in all_links:
        href = link.get("href")
        if any(x in href for x in should): #relevant hyperlink
            if 'pdf' not in href: # ignore pdf
                if 'call' not in href:
                    if 'iaai' not in href:
                        if href not in links: # reduce duplicate
                            links.append(href)
    # print(links)
    return links


def clean_format(item):
    item = re.sub(r'^Sponsor.+', '', item)
    item = re.sub(r'Sponsorship', '', item)
    item = re.sub(r'Registration', '', item)
    item = re.sub(r'Hotel and Travel', '', item)
    item = re.sub(r'^This site.+', '', item)
    return item


def relevant_pages(links):  # links must be a list
    all_page = ''

    for i in range(len(links)):
        all_name = ''
        soup = request(links[i])
        if soup.find('h2') != None:  # area chair
            header = soup.find('h2').text
            all_name = all_name + header + ':'
            all_p = soup.findAll('p')
            # print(all_p)
            for element in all_p:
                item = element.text
                item = clean_format(item)
                all_name = all_name + item
                # print(all_name)
                all_name = text_to_line(all_name)
            all_page = all_page + all_name +'\n'
        if soup.find('h1') != None:
            header = soup.find('h1').text
            if str(header) == 'AAAI-20 Conference Committee':
                all_name = all_name + header +':'
                all_p = soup.findAll('p')
                for element in all_p:
                    item = str(element.text)
                    item = clean_format(item)
                    all_name = all_name + item
                    all_name = text_to_line(all_name)
                    # all_name.strip()
                all_page = all_page + all_name + '\n'
            if str(header) == 'AAAI-20 Senior Program Committee':
                all_name = all_name + header + ':'+ '\n'
                all_p = soup.findAll('div',class_='et_pb_text_inner')
                for element in all_p:
                    if not bool(element.find('h1')):
                        item = str(element.text)
                        item = clean_format(item)
                        all_name = all_name + item
                        all_name = text_to_line(all_name)
                all_page = all_page + all_name + '\n'
                all_page.strip()
    file_name = open("organization_name.txt", "a")
    file_name.writelines(all_page)

    return all_page


def clean_name(name_lst): #name_lst is a list of list
    list1 = []
    list_name = []
    list_insit = []
    list_country = []
    for i in name_lst:
        for j in i:
            count = len(j.split(' '))
            if count < 5:
                print(list1)
                # list1 = list1.append(j) # list1 = ['AAAI program committee']
                #write to frst column of csv

            else:
                nw = j.split('\n') # list
                # print(nw)
                # with open('fileName.csv', 'w') as f:
                #     writer = csv.writer(f,delimiter = ',')
                new_list = []
                for item in nw: # item format - name (insititute)
                    if re.match(r'^This site', item):
                        break
                    else:
                        a = [item]
                        new_list.append(a)
                        print(new_list)


def invited_speaker(soup):
    all_links = soup.find_all("a")
    should = ['speakers']

    links = []
    for link in all_links:
        href = link.get("href")
        if any(x in href for x in should):  # relevant hyperlink
            if 'pdf' not in href:  # ignore pdf
                if 'call' not in href:
                    if 'iaai' not in href:
                        if href not in links:  # reduce duplicate
                            # if bool(re.search(r'aaai-20',href,flags=re.I)):
                            links.append(href)
    for j in links:
        if '#' in j:
            links.remove(j)
    soup = request(links[0])
    text = ''
    for i in soup.select('div.et_pb_text_inner', limit= 3):
        if (i.find('h1')):
            # nohyphen = re.sub('-','',i.find('h1').get_text())
            text = text + i.find('h1').get_text() +'\n'
        if (i.find('p')):
            for p in i.select('p'):
                count = p.get_text().split(" ")  # avoid long paragraph
                if len(count) < 40:
                    nohyphen = re.sub('\-', '',p.get_text())
                    # text.replace('\n', '')
                    text = text + nohyphen + '\n'

    #clean time
    text = re.sub(r"([A-Z])\w+\,\s([A-Z])\w+\s\d+\,\s\d+\:[\d -]+", '', text, flags=re.I)
    # clean format
    text = re.sub(r"[A-Z 0-9]+\:", '', text,flags=re.I)
    text = re.sub(r"[-]\w*\d+\w(AM)*(PM)*",'', text,flags=re.I)
    # text = re.sub(r"AAAI20.+", '', text, flags=re.I)
    text = re.sub(r"[A-Z]+\,[\d-]+",'',text,flags=re.I)
    text = re.sub(r"(This).+", '', text, flags=re.I)
    text = re.sub(r"Debaters.+", '', text, flags=re.I)
    text = re.sub(r"Grand.+", '', text, flags=re.I)
    text = re.sub(r"Academic.+", '', text, flags=re.I)
    text = re.sub(r"Ben Shapiro.+", '', text, flags=re.I)
    text = re.sub(r'Robert S. Engelmore Memorial Award Lecture','',text)
    text = re.sub(r'EAAI Outstanding Educator Award Lecture', '', text)
    text = re.sub(r"\(Details", '', text, flags=re.I)
    text = re.sub(r"\W\d+\W([A-Z])+", '', text, flags=re.I)
    text = re.sub(r"^am", '', text)

    text = text_to_line(text)

    text = re.sub(r"^\,", '', text, flags=re.I)
    # print(text)
    file_name = open("organization_name.txt", "a")
    file_name.writelines(text)
    file_name.close()

    return text

def text_to_line(text):
    text_list = text.split(')')
    new = ''
    for item in text_list:
        new = new + item + '\n'
    return new

def clean_txt(file):

    with open(file) as infile, open('output.txt', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            line = re.sub(r"^am", '', line)
            line = re.sub(r"^,", '', line)
            outfile.write(line)  # non-empty line. Write it to output



if __name__ == '__main__':
    url = "https://aaai.org/Conferences/AAAI-20/"
    soup = request(url)

    program_name(soup)

    links = get_all_links(soup)
    organization_name = relevant_pages(links)

    speaker_name = invited_speaker(soup)

    clean_txt('organization_name.txt')
