import requests
from bs4 import BeautifulSoup
import re
import os.path
from tika import parser

def request(url):
    result = requests.get(url)

    src = result.content
    soup = BeautifulSoup(src, features="html.parser")
    return soup


def check_year(url):
    year = re.findall(r"[0-9]+",url) #year is a list
    if 'aaai' in url:
        file_name = year[0] + 'aaai_conference_name.txt'
    else:
        file_name = year[0] + 'applied_name.txt'
    return file_name


def get_all_links(soup): # all relevant links under organization
    all_links = soup.find_all("a")
    should = ['committee', 'chairs']
    year = re.findall(r"[0-9]+", url)  # year is a list

    links = []
    for link in all_links:
        href = link.get("href")
        if href is not None:
            if any(x in href for x in should):  #relevant hyperlink
                if ('pdf' not in href) and ('call' not in href) and ('iaai' not in href):
                    if 'php' in href and 'http' not in href and ('#' not in href):
                        href = 'https://www.aaai.org/Conferences/AAAI/20'+year[0]+'/' + href
                    if 'http' not in href:
                        href = 'https://aaai.org' + href  # complete the site
                    if (href not in links):
                        links.append(href)

    return links


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


def relevant_pages(url,  links):  # links must be a list #committee page
    all_page = ''
    length = len(links)

    if 'php' in url:
        for i in range(length): # add more relevant links in some known pages
            soup = request(links[i])
            attached = get_all_links(soup)
            for ele in attached:
                if ele not in links and '#' not in ele:
                    links.append(ele)

        for i in range(len(links)):
            all_name = ''
            soup = request(links[i])

            if soup.find('h2') != None:  # area chair
                header = soup.find('h2').text
                all_name = all_name + header + ':'+'\n'
                all_p = soup.findAll('p')
                for p in all_p:
                    if  "(" in p.text and not p.find('a'):
                        p_text = re.sub(r"\(.+@.+\)",'',p.text) # remove email
                        all_name = all_name + p_text
                        all_name = text_to_line(all_name)
                    else:
                        continue
            all_page = all_page + all_name + '\n'

    else:
        for i in range(len(links)):
            all_name = ''
            soup = request(links[i])
            if soup.find('h2') != None:  # area chair
                header = soup.find('h2').text
                all_name = all_name + header + ':'
                all_p = soup.findAll('p')
                all_page = all_page + all_name + combine_name(all_p) +'\n'
            if soup.find('h1') != None:
                header = soup.find('h1').text
                if 'Senior Program Committee' in str(header):
                    all_name = all_name + header + ':'+ '\n'
                    all_p = soup.findAll('div', class_='et_pb_text_inner')
                    for element in all_p:
                        if not bool(element.find('h1')):
                            item = str(element.text)
                            item = clean_format(item)
                            all_name = all_name + item
                            all_name = text_to_line(all_name)
                    all_page = all_page + all_name + '\n'
                    all_page.strip()

                else:
                    all_name = all_name + header +':'
                    all_p = soup.findAll('p')
                    all_page = all_page + all_name + combine_name(all_p) + '\n'

    file = check_year(url)

    file_name = open(file, "w")
    file_name.writelines(all_page)

    return all_page

def invited_speaker(url, soup):
    all_links = soup.find_all("a")
    should = ['speakers']

    links = []
    for link in all_links:
        href = link.get("href")
        if any(x in href for x in should):  # relevant hyperlink
            if ('pdf' not in href) and ('call' not in href) and ('iaai' not in href) and ('#' not in href):
                if 'applied' in href and 'http' not in href:
                    href = 'https://www.re-work.co/' + href
                elif 'http' not in href:
                    href = 'https://aaai.org' + href
                if href not in links:
                    links.append(href)

    soup = request(links[0])
    lst = []
    if 'php' in url:
        for i in soup.findAll('b'):
            if re.match(r".+\,\W\w+\W[0-9]",i.text): #ignore time
                continue
            else:
                if len(i.text.split()) > 2:
                    text = re.sub(r".+\:", '',i.get_text())
                    text = text.split('),')
                    for item in text:
                        lst.append(item)

    elif 'aaai'in url: #aaai
        lst = get_member(links[0])

    else:
        cell = soup.findAll('div', class_='cell speaker')  # applied ai
        for speaker in cell:
            name = speaker.find('h5')
            if speaker.find('h5') is not None:
                name = speaker.find('h5').text
            if speaker.find('p', class_='speaker__company') is not None:
                insti = speaker.find('p', class_='speaker__company').text
            sp = str(name) + ' (' + str(insti) + ')'
            lst.append(sp)

    file = check_year(url)
    file_name = open(file, "a")
    file_name.write('Invited Speakers: \n')
    file_name.write('\n'.join(lst))
    file_name.write('\n')


def get_tutorial_page(soup):
    all_links = soup.find_all("a")
    should = ['tutorials','panels']

    lst = []

    for link in all_links:
        href = link.get("href")

        if any(x in href for x in should):
            if 'php' in href and 'http' not in href and ('#' not in href) and '13' not in href:
                href = 'https://www.aaai.org/Conferences/AAAI/20' + year[0] + '/' + href
            if 'php' in href and 'http' not in href and '13' in href:
                href = 'http://www.aaai.org/Conferences/AAAI/' + href
            if 'http' not in href:
                href = 'https://aaai.org' + href  # complete the site
            if href not in lst:
                lst.append(href)

    return lst


def tutorial_name(url, links):

    file = check_year(url)
    file_name = open(file, "a")
    file_name.write('Tutorial Forum and Panelists:\n')

    lst = []
    if 'php' in url:
        for link in links:
            soup = request(link)
            for i in soup.findAll('b'):
                i_text = re.sub(r".+\:.+",'',i.text)
                if re.match(r".+\,\W\w+\W[0-9]", i_text):  # ignore time
                    continue
                else:
                    text = i_text.replace(' and ', ',')
                    text = text.split(',')
                    for item in text:
                        if len(item) >1 and 'NEW' not in item:
                            lst.append(item)
        file_name.write('\n'.join(lst))
        file_name.write('\n')
    else:
        for line in links:
            lst= get_member(line)
            file_name.write('\n'.join(lst))
            file_name.write('\n')


def get_member(link):
    soup = request(link)

    lst = []
    for i in soup.findAll('div', class_='et_pb_team_member_description'):
        name = i.find('h4').get_text()
        if len(i.find('h4').findNext('p').get_text().split(' ')) < 20:
            insti = i.find('h4').findNext('p').get_text()
        else:
            insti = ' '
        lst.append(name + ' (' + insti + ')')

    return lst


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

    save_path = 'example/'
    complete = os.path.join(save_path, out_file)

    with open(file) as infile, open(complete, 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            line = re.sub(r"^\,.+", '', line)
            outfile.write(line)  # non-empty line. Write it to output


def get_program_committee(soup):
    all_links = soup.find_all("a")
    should = ['Members.List_.']

    for link in all_links:
        href = link.get("href")
        if any(x in href for x in should):
            return href


def pdf_parser(file):
    # Parse data from file
    file_data = parser.from_file(file)
    # Get files text content
    text = file_data['content']
    # print(text)
    file_name = open('program_committee.txt','w')
    file_name.writelines(text)

    output_file = check_year(url)
    with open('program_committee.txt') as infile, open(output_file, 'a') as outfile:
        outfile.write('AAAI20 Program Committee members:\n')
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)


if __name__ == '__main__':

    aaai_urls = ['https://aaai.org/Conferences/AAAI-20/',
            'https://aaai.org/Conferences/AAAI-19/',
            'https://aaai.org/Conferences/AAAI-18/',
            'https://aaai.org/Conferences/AAAI/aaai17.php',
            'https://aaai.org/Conferences/AAAI/aaai16.php',
            'https://aaai.org/Conferences/AAAI/aaai15.php',
            'https://aaai.org/Conferences/AAAI/aaai14.php',
            'https://aaai.org/Conferences/AAAI/aaai13.php']

    for url in aaai_urls:

        year = re.findall(r"[0-9]+", url)

        soup = request(url)

        links = get_all_links(soup)

        organization_name = relevant_pages(url, links)

        invited_speaker(url, soup)  # invited speaker page

        tut_link = get_tutorial_page(soup)  # tutorial forum page

        tutorial_name(url, tut_link)

        if '20' in year[0]:
            program_committee = get_program_committee(soup)  # 2020 program committee page

            pdf_parser(program_committee)

        clean_txt(check_year(url))

    applied_ai_urls = ['https://www.re-work.co/events/applied-ai-summit-san-francisco-2021',
                       'https://www.re-work.co/events/applied-ai-summit-san-francisco-2020',
                       'https://www.re-work.co/events/applied-ai-summit-san-francisco-2019',
                       'https://www.re-work.co/events/applied-ai-summit-houston-2018']

    for link in applied_ai_urls:

            soup = request(link)

            invited_speaker(link, soup)  # invited speaker page

            clean_txt(check_year(link))
