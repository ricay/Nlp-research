from namsorclient import NamsorClient
from namsorclient.country_codes import CountryCodes
from namsorclient.request_objects import *
import pickle
import re
import os
import pandas as pd
from itertools import islice
import csv
import json
import simplejson

# Create an instance of NamsorClient and pass in your API key as an argument.
client = NamsorClient('61f8c3dc68d36e701dd558f668eb4fb9')
# CountryBatch(Batch)
# US_RaceEthnicityBatch()
def get_gender():
    save_path = 'mcgill/'
    # out_file = '20_aaai_output.txt'
    out_file = '15_mcgill.txt'
    complete = os.path.join(save_path, out_file)

    filename = 'grad_gender.pickle'

    name_dict = pickle.load(open(filename, "rb"))
    # Access the genderBatch (POST) endpoint
    gender_batch = GenderFullBatch()
    with open(complete) as file:
        while True:
            lines = list(islice(file, 100))
            if not lines:
                break
            worksheet = []
            for line in lines:
                print(line)
                if ':' not in line:
                    name = re.sub(r"\(.+\)*", "", line)
                    worksheet.append(name)
                    if name not in name_dict:
                        gender_batch.addItem(name)
            # response_list = gender_batch.classify('61f8c3dc68d36e701dd558f668eb4fb9')
            # for name in response_list:
            #     name_dict[name.name.strip()] = name.likely_gender
                    while len(worksheet) == 100:
                        # print(worksheet)
                        gender_batch = GenderFullBatch()
                        for name in worksheet:
                            if name not in name_dict:
                                gender_batch.addItem(name)
                        worksheet = []
    #                     response_list = gender_batch.classify('61f8c3dc68d36e701dd558f668eb4fb9')
    #                     for name in response_list:
    #                         name_dict[name.name.strip()] = name.likely_gender
                pickle.dump(name_dict, open(filename, "wb"))


def return_dic():
    filename = 'gender.pickle'
    name_dict = pickle.load(open(filename, "rb"))
    return name_dict


def last_dict():
    """newest dict with gender"""

    # my_dic = pd.read_excel('genderfile.xlsx', index_col=0).to_dict()
    # # new_d = pickle.load(open('new_d.pickle', "rb"))
    # for item in my_dic:
    #     new_d = my_dic[item]

    new_d = pickle.load(open('new_d.pickle', "rb"))
    # new_d.pop('Jeong')
    # new_d['Kristin P. Bennett'] = 'female'
    # new_d  = simplejson.loads(simplejson.dumps(new_d, ignore_nan=True))
    # pickle.dump(new_d, open('new_d.pickle', "wb"))
    return new_d

def gender_excel():

    new_dict={}
    for key, val in return_dic().items():
        new_dict[key] = [val]

    df = pd.DataFrame.from_dict(new_dict).T
    df.to_excel('genderfile.xlsx')


def parse():
    pfilename = 'race.pickle'
    #
    race_dict = pickle.load(open(pfilename, "rb"))
    # dict_ex = {'Seshu Yalamanchili': 'male', "Biao 'Bill' Chang": 'male', 'Tian Su': 'male', 'Prakash Mall': 'male', 'Julia Badger': 'female'}
    dict_ex = last_dict()

    for key in dict_ex:
        if key not in race_dict and key is not None:
            api_name = 'https://v2.namsor.com/NamSorAPIv2/api2/json/parseName/' + key
            fs_name = requests.get(api_name, headers={'X-API-KEY': '61f8c3dc68d36e701dd558f668eb4fb9'})
            fs_name = json.loads(fs_name.text)

            api_race = 'https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicity/'
            api_race += fs_name['firstLastName']['firstName']+ '/' + fs_name['firstLastName']['lastName']

            race = requests.get(api_race, headers={'X-API-KEY': '61f8c3dc68d36e701dd558f668eb4fb9'})
            race = json.loads(race.text)

            race_dict[key] = race['raceEthnicity']
            pickle.dump(race_dict, open(pfilename, "wb"))
            print(race_dict)

    return race_dict

def ret_race():
    """newest race dict"""
    pfilename = 'race.pickle'

    race_dict = pickle.load(open(pfilename, "rb"))
    return race_dict


def export_to_excel():
    new_dict={}
    for key, val in ret_race().items():
        new_dict[key] = [val]

    df = pd.DataFrame.from_dict(new_dict).T
    df.to_excel('racefile.xlsx')

# export_to_excel()

def applied():
    applied_dict = {}
    save_path = 'output/'
    # out_file = '20_aaai_output.txt'
    out_file = '2021_applied_ai_output.txt'
    complete = os.path.join(save_path, out_file)
    race_dict = ret_race()
    with open(complete) as file:
        for line in file:
            if ':' not in line:
                name = re.sub(r"\(.+\)*", "", line).strip()
                if name in race_dict:
                    applied_dict[name] = [race_dict[name]]
        print(applied_dict)
        df_20 = pd.DataFrame.from_dict(applied_dict).T
        df_20.to_excel('2021_race_file.xlsx')

# applied()

def get_country():
    country_dict = {}
    count_us = 0
    count_ca = 0
    europe = ['Germany', 'Greece', 'Italy', 'UK', 'Spain', 'Belgium','Netherlands','Sweden','Ireland','France','Portugal']
    asian = ['China', 'Japan', 'Korea', 'Taiwan', 'India']
    count_au = 0
    count_eu = 0
    count_asia = 0
    save_path = 'output/'
    # out_file = '20_aaai_output.txt'
    out_file = '17_aaai_output.txt'
    complete = os.path.join(save_path, out_file)
    with open(complete) as file:
        for line in file:
            if 'USA' in line:
                count_us += 1
            elif 'Canada' in line:
                count_ca += 1
            elif 'Australia' in line:
                count_au += 1
            else:
                for item in europe:
                    if item in line:
                        count_eu += 1
                for a in asian:
                    if a in line:
                        count_asia +=1

    country_dict['USA'] = count_us
    country_dict['Canada'] = count_ca
    country_dict['Europe'] = count_eu
    country_dict['Australia'] = count_au
    country_dict['Asia'] = count_asia
    return country_dict
print(get_country())
