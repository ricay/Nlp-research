import pickle
import re
import os
import pandas as pd

def last():
    """newest dict with gender"""

    newest_d = {}
    my_dic = pd.read_excel('grad_gen.xlsx', index_col=0).to_dict()
    # new_d = pickle.load(open('new_d.pickle', "rb"))
    for item in my_dic:
        newest_d = my_dic[item]
    pickle.dump(newest_d, open('grad.pickle', 'wb'))
# last()

def last_dict():
    """newest dict with gender"""

    new_d = pickle.load(open('grad_g.pickle', "rb"))

    return new_d

def applied():
    applied_dict = {}
    all_l = []
    # save_path = 'ut/'
    # out_file = 'ut_17.txt'
    # complete = os.path.join(save_path, out_file)
    # save_path = 'mcgill-data/'
    string = '15Biology'
    complete = string + '.txt'
    # complete = os.path.join(save_path, out_file)

    # race_dict = ret_race()
    new_d = pickle.load(open('grad_g.pickle', "rb"))
    gender_dict = new_d
    race_dict = pickle.load(open('grad_race.pickle', "rb"))
    print(new_d)
    # gender_dict = last_dict()
    with open(complete) as file:
        for line in file:
            if ':' not in line:
                name = line
                if name in race_dict:

                    applied_dict[name] = [race_dict[name]]
        print(applied_dict)
        df_20 = pd.DataFrame.from_dict(applied_dict).T
        # string = '15_m'
        excel_name = string + '.xlsx'
        df_20.to_excel(excel_name)

applied()

def to_dict():
    new_d = pickle.load(open('grad_g.pickle', "rb"))
    gender_dict = new_d
    print(gender_dict)
    df_20 = pd.DataFrame.from_records(gender_dict, index = 'Ariya  Parisa A.').T
    df_20.to_excel('1all_g.xlsx')

# to_dict()

def to_txt():
    applied_dict = {}
    all_l = []
    save_path = 'mcgill/'
    out_file = '15_mcgill.txt'
    complete = os.path.join(save_path, out_file)

    # race_dict = ret_race()
    new_d = pickle.load(open('grad_g.pickle', "rb"))
    gender_dict = new_d
    race_dict = pickle.load(open('grad_race.pickle', "rb"))
    print(new_d)
    # gender_dict = last_dict()
    with open(complete) as file:
        for line in file:
            if ':' in line:
                year = re.findall(r"[0-9]+", out_file)
                line = re.sub(r"\W",'',line)
                subject = year[0] + line + '.txt'
                ou = open(subject, 'a')
            if ':' not in line:
                if line not in all_l:
                    name = line
                    all_l.append(line)
                    ou.write(name)

# to_txt()
