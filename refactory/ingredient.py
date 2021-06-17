# extract ingredients from recipes and count frequency

import pandas as pd
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import re
import requests
from bs4 import BeautifulSoup
import ast
import inflect
from help_functions import read_csv_files

# ----------------------------- parse recipes to get clean ingredient -----------------------------

def clean_recipe(ingred_list):
    cleanedtext = []
    p = inflect.engine()
    # change from string to list
    ingred_list = ast.literal_eval(ingred_list)
    
    for matchtext in ingred_list:
        # Obtain all before first comma
        if re.compile('^(.+?)(?=,)').search(matchtext) is not None:
            matchtext = re.compile('^(.+?)(?=,)').search(matchtext).group(1)
        
        # Tokenize ingredient list
        tokenized = word_tokenize(matchtext)
        
        # Remove words likely to be stop words or measurements
        removed_stop = [w for w in tokenized if not w in measure_corpus]
        removed_stop = [w for w in removed_stop if not w in stop_words]
        
        # Filter adjectives and nouns
        ingred_words = lambda pos: pos[:2] in ['JJ','NN','NNS']
        ingreds = [word.lower() for (word, pos) in pos_tag(removed_stop) if ingred_words(pos)]
        
        # Convert to singular
        ingreds = [p.singular_noun(word) if p.singular_noun(word) else word for word in ingreds]
        
        # remove special characters (including numbers!)怎么去除 ½, ¼, %等
        ingreds = [re.sub('[^ a-zA-Z]', '', i) for i in ingreds]
        #print(ingreds)
        
        # Remove common ingredients 
        common = []
        cleanedtext.append(ingreds)
        cleanedtext = [[ing for ing in ingreds if not any(word in common for word in ingreds)] for ingreds in cleanedtext]
        
        # Remove additional descriptors for long ingredient names
        cleanedtext = [ingreds[-2:] if len(ingreds) > 2 else ingreds for ingreds in cleanedtext]
        
    return [(' ').join(item) for item in cleanedtext if len(item)>0]


def get_stopwords():
    stop_words = set(stopwords.words('english'))

    page = requests.get('https://www.enchantedlearning.com/wordlist/measurement.shtml')
    soup = BeautifulSoup(page.content, "html.parser")
    measure_corpus = [tag.text for tag in soup.find_all('div',attrs={'class':'wordlist-item'})]
    # add plural form and additional words
    measure_corpus = measure_corpus + [text+'s' for text in measure_corpus] + \
                ['taste','strip', 'strips', 'package', 'packages', 'satchet', \
                 'satchets', 'sprigs', 'head', 'bunch', 'small', 'large', 'big', 'medium', 'tbsp', 'g']
    return stop_words, measure_corpus


def store_parsed_ingredients(data):

    df = data[['ingredients']]
    df['ingredients'] = df['ingredients'].apply(clean_recipe)
    df = df.rename(columns={"ingredients": "parsed_ingredients"})
    data = data.join(df)
    data.to_csv('./clean_data.csv')
    

# ----------------------------- count ingredient frequency and find top ingredients -----------------------------

def count_ingredient_frequency(data):
    # count the frequency of each ingredient
    dic = {}

    for ingredient in data['parsed_ingredients']:
        #if type(ingredient) != list:
            # if load from presaved csv file then type is str
            # convert from str to list
        ingredient = ast.literal_eval(ingredient)
        for item in ingredient:
            try:
                dic[str(item)] += 1
            except:
                dic[str(item)] = 1
    dic_sorted = sorted(dic.items(),key=lambda item:item[1], reverse=True)
    return dic_sorted
    

def get_top_ingredients(path, number):
    # find most common top 10 ingredients in training data
    data = pd.read_csv(path)
    dic_sorted = count_ingredient_frequency(data)
    top_ingredient = []
    for (i,j) in dic_sorted[:number]:
        top_ingredient.append(i)

    return top_ingredient


def ingredient_vector(data, top_ingredients):
    # turn ingredients of each recipe into vector
    ingre_vectors = []

    for parsed_ingre in data['parsed_ingredients']:
        if type(parsed_ingre) != list:
            ingres = ast.literal_eval(parsed_ingre)
        ingre_vector = len(top_ingredients) * [0]

        for ingre in ingres:
            if ingre in top_ingredients:
                ingre_vector[top_ingredients.index(ingre)] = 1

        ingre_vectors.append(ingre_vector)
    
    return np.asarray(ingre_vectors)


def clean_ingredient_vector(data, drop_index, top_ingredient):
    ingre_vectors = ingredient_vector(data, top_ingredient)
    
    # remove corresponding ingredients of recipes lacking complete nutrients
    ingre_vectors = [i for j, i in enumerate(ingre_vectors) if j not in drop_index]
    ingre_vectors = np.asarray(ingre_vectors)
    
    return ingre_vectors


stop_words, measure_corpus = get_stopwords()


