# extract nutrient information from recipes and record indexes of incomplete nutrients

import ast
import re
import numpy as np


# ----------------------------- parse recipes to get clean nutrients -----------------------------

def get_nutrient_information(data):
    nutrient_information = []

    for nutrients in data['nutrients']:
        # convert string to dictionary
        data_dict = ast.literal_eval(nutrients)
        # data_dict.values()
        # find numerical values of each nutrients
        nutrient = re.findall('[\d+\.\d+]+', str(data_dict.values()))
        nutrient = [float(num) for num in nutrient]
        nutrient_information.append(nutrient)
    
    return np.asarray(nutrient_information)


# ----------------------------- find indexes of incomplete nutrients -----------------------------

# {'calories', 'fatContent', 'saturatedFatContent', 'carbohydrateContent', 'sugarContent', 'fiberContent', 'proteinContent', 'sodiumContent'}

def find_incomplete_indexes(nutrient_information):
    # remove those with incomplete nutients
    index = 0
    drop_index = []

    for i in nutrient_information:
        if len(i) < 8:
            drop_index.append(index)
        index+=1
    
    # remove incomplete indexes
    clean_nutrient_information = [i for j, i in enumerate(nutrient_information) if j not in drop_index]
    clean_nutrient_information = np.asarray(clean_nutrient_information)
    return clean_nutrient_information, drop_index










