# scrape recipe information from www.bbcgoodfood.com

import requests
import os
import pandas as pd
from recipe_scrapers import scrape_me
import sys
sys.setrecursionlimit(20000)



# ----------------------------- define categories and corresponding urls to be scraped -----------------------------

def input_category_information(name, pages, recipe_number):
    # input information
    dic = {}
    dic['name'] = name
    dic['pages'] = pages
    dic['number'] = recipe_number

    return dic

def define_required_data():
    
    raw_data = []
    # raw_data.append(input_category_information('burger', 18, 421))
    # raw_data.append(input_category_information('salad', 53, 1271))
    raw_data.append(input_category_information('cake', 36, 857))
    return raw_data


# ----------------------------- scrape recipes from www.bbcgoodfood.com -----------------------------

def scrape_from_web(categories):
    # deal with one category at a time
    for category in categories:
        name = category['name']
        recipe_links = []
        urls = get_urls(category)
        
        if not os.path.exists('./extracted_data/'):
            os.mkdir('./extracted_data/')
        
        # create directory for each sub-category
        path = './extracted_data/' +  name + '/'
        if not os.path.exists(path):
            os.mkdir(path)
        
        
        # loop through pages
        for url in urls:
            # scrape from table of contents
            scraper = scrape_me(url)
            # extract all the links in this page
            links = scraper.links()
            # get all the recipe links in the search query
            recipe_links = extract_recipe_links(recipe_links, links)
        
        # store recipe links?
        # recipe_links.to_csv(path + name + '_recipe_links.csv', index=False)
        
        # extract information from each recipe
        structured_information = extract_from_recipes(recipe_links)
        
        # download images from extracted image links
        download_images(path, structured_information)

        df = pd.DataFrame(structured_information)
        df.to_csv('./csv_files/' + name + '.csv', index=False)

        # return structured_information

    
def get_urls(dic):
    # get page urls for each category
    urls = []
    for i in range(1, dic['pages']+1):
        url = 'https://www.bbcgoodfood.com/search/recipes/page/' + str(i) + '/?q=' + dic['name'] + '&sort=-relevance'
        urls.append(url)
    
    return urls


def extract_recipe_links(recipe_links, links):
    # extract recipe links from all the links
    for link in links:
        try:
            if link['class'] == ['standard-card-new__article-title', 'qa-card-link']:
                recipe_links.append('https://www.bbcgoodfood.com'+link['href'])
        except:
            continue
    
    return recipe_links


def extract_from_recipes(recipe_links):
    # combine structured information of each recipe
    structured_information = []
    i = 1
    for recipe_link in recipe_links:
        print(i)
        i+=1
        temp = structured_information_in_recipe(recipe_link)
        # remove recipes that contain incomplete information
        if temp == {} or temp['nutrients'] == {} or temp['ingredients'] == {} or temp['image'] == {}:
            continue
        else:
            structured_information.append(temp)
    return structured_information


def structured_information_in_recipe(recipe_link):
    # extract name, image, ingredients, and nutrients from each recipe website
    recipe = {}
    scraper = scrape_me(recipe_link)
    recipe['title'] = scraper.title()
    recipe['image'] = scraper.image()
    recipe['ingredients'] = scraper.ingredients()
    recipe['nutrients'] = scraper.nutrients()
    
    return recipe

    
def download_images(path, structured_information):
    # download images from image links
    index = 0
    
    for recipe in structured_information:
        image = requests.get(recipe['image'])
        with open(path + str(index)+'.jpg', 'wb') as f:
            f.write(image.content)
        index += 1


#define categories to be extracted
#categories = define_required_data()
#scrape_from_web(categories)









