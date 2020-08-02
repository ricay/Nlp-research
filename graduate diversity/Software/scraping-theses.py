import requests
from bs4 import BeautifulSoup
import re
import os.path
from tika import parser
import urllib.request

def request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    result = requests.get(url,headers)

    src = result.content
    soup = BeautifulSoup(src, features="html.parser")
    return soup


def check_year(url):
    year = re.findall(r"[0-9]+",url) #year is a list
    if 'aaai' in url:
        file_name = year[0] + 'aaai_conference_name.txt'
    else:
        file_name = '20' + 'applied_name.txt'
    return file_name


def clean_format(item):
    item = re.sub(r'^Sponsor.+', '', item)
    item = re.sub(r'Sponsorship', '', item)
    item = re.sub(r'Registration', '', item)
    item = re.sub(r'Hotel and Travel', '', item)
    item = re.sub(r'^This site.+', '', item)
    return item


def combine_name(all_p):
    all_name = ''
    for element in all_p:
        item = element.text
        item = clean_format(item)
        all_name = all_name + item
        all_name = text_to_line(all_name)
    return all_name


def year_and_name(url):
    year_name = []
    soup = request(url)
    all_p = soup.findAll('td', {'class': 'evenRowEvenCol'})
    for element in all_p:
        name = str(element.text)
        print(name)
        name = re.sub(r"[0-9]+.[a-zA-Z]+.[0-9]+", '', name)
        name = re.sub(r"[a-zA-Z]+.[0-9]+", '', name)
        name = re.sub(r"[0-9]+", '', name)
        if ';' in name:
            text_list = name.split(';')
            for item in text_list:
                if item is not '' and item not in year_name:
                    year_name.append(item.strip())
        else:
            if name is not '' and name not in year_name:
                year_name.append(name.strip())
    print(year_name)

    file = '18chemistry.txt'
    file_name = open(file, "a")
    # file_name.write('Engineering:\n')
    file_name.write('\n'.join(year_name))
    return year_name

def ubc_name(url):
    year_name = []
    soup = request(url)
    print(soup)
    all_p = soup.findAll('span')
    for element in all_p:
        name = str(element.text)
        print(name)

        if name is not '' and name not in year_name:
            year_name.append(name.strip())
    print(year_name)

    file = 'ubc15.txt'
    file_name = open(file, "a")
    file_name.write('\n'.join(year_name))

    return year_name

def check_ubc():
    response = urllib.request.urlopen('https://open.library.ubc.ca/search?q=*&p=0&sort=0&view=0&perPage=2&circle=n&dBegin=1420156800000&dEnd=1451692800000&c=5&program=Electrical%20and%20Computer%20Engineering&ubc_repo_label=cIRcle')
    html = response.read()
    text = html.decode()
    print(re.findall('(.*?)', text))


def mcgill_name(url):
    year_name = []
    soup = request(url)
    all_p = soup.findAll('span', {'itemprop': 'creator'})
    for element in all_p:
        name = str(element.text)
        name = re.sub(r"\,", ' ', name)
        print(name)
        if name is not '' and name not in year_name:
            year_name.append(name.strip())

    # file = 'mgcill19.txt'
    # file_name = open(file, "a")
    # file_name.write('\n'.join(year_name))

def text_to_line(text):
    text_list = text.split(')')
    new = ''
    for item in text_list:
        new = new + item + '\n'
    return new


def clean_txt(file):
    year = re.findall(r"[0-9]+", file)  # year is a list
    if 'aaai' in file:
        out_file = year[0] + '_aaai_output.txt'
    else:
        out_file = year[0] + '_applied_ai_output.txt'

    save_path = 'new/'

    complete = os.path.join(save_path, out_file)

    with open(file) as infile, open(complete, 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            line = re.sub(r"^\,.+", '', line)
            outfile.write(line)  # non-empty line. Write it to output

def clean_name():
    all_name = []
    lst = ['18chemistry.txt']
    file = open('18chemistry.txt','r')
    # for line in file:
    #     if ":" not in line:
    #         all_name.append(line)
    # lst2 = ['16.txt']
    for item in lst:
        year = re.findall(r"[0-9]+", item)  # year is a list

        # out = 'ut_' + year[0] + '.txt'
        out = '18-Chemistry.txt'
        name_dict = []
        with open(item) as infile, open(out, 'w') as outfile:

            for line in infile:
                if not line.strip(): continue  # skip the empty line
                line = re.sub(r"\,", ' ', line)
                if line not in name_dict:
                    name = re.sub(r"\,", ' ', line)
                    name_dict.append(name)
                    all_name.append(name)

            # outfile.write('Engineering:\n')
            outfile.write(''.join(name_dict))
            # non-empty line. Write it to output

def duplicate():
    all_name = []
    lst = ['ut_15.txt','ut_16.txt','ut_17.txt','ut_18.txt','ut_19.txt']
    file = open('ut_15.txt','r')
    for item in lst:
        year = re.findall(r"[0-9]+", item)  # year is a list

        out = year[0] + '.txt'
        name_dict = []
        with open(item) as infile, open(out, 'a') as outfile:

            for line in infile:
                if not line.strip(): continue  # skip the empty line
                if line not in all_name:
                    name = line
                    name_dict.append(name)
                    all_name.append(name)

            # outfile.write('Engineering:\n')
            outfile.write(''.join(name_dict))

if __name__ == '__main__':

    mcg = 'https://escholarship.mcgill.ca/catalog?f%5Bdate_sim%5D%5B%5D=2019&f%5Bdepartment_sim%5D%5B%5D=Department+of+Chemistry&locale=en&per_page=100&q=&search_field=all_fields'

    # mcgill_name(mcg)

    url = 'https://tspace.library.utoronto.ca/simple-search?location=%2F&query=chemistry&rpp=25&sort_by=score&order=desc&filter_field_1=dateIssued&filter_type_1=contains&filter_value_1=%5B2010+TO+2020%5D&filter_field_2=dateIssued&filter_type_2=equals&filter_value_2=2018'

    url2='https://tspace.library.utoronto.ca/simple-search?query=chemistry&filter_field_1=dateIssued&filter_type_1=contains&filter_value_1=%5B2010+TO+2020%5D&filter_field_2=dateIssued&filter_type_2=equals&filter_value_2=2018&sort_by=score&order=desc&rpp=25&etal=0&start={}'
    # year_and_name(url)
    # page = 0
    # lst = []
    # for i in range(10):
    #     page+=25
    #     lst.append(page)
    # year15_urls = [url2.format(year) for year in lst]
    # # # print(year15_urls)
    # #
    # for item in year15_urls:
    #     year_and_name(item)

    # clean_name()
    # ubc_name(url)
    # check_ubc()
    # duplicate()
    clean_name()
