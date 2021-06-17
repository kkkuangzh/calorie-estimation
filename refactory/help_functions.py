# read images, read extracted csv files

import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from PIL import Image
import re


def read_csv_files(path):
    # create a table that contains information of each category
    data = pd.DataFrame()
    for path, subpath, files in os.walk(path):
        # make sure that the label corresponds to images
        files.sort()
        for i in files:
            if i.endswith("csv"):
                temp = pd.read_csv(path + '/' + i)
                # integrate csv files of different categories into one table
                data = data.append(temp, ignore_index=True)
    return data


def sort_key(s):
    # sort image name by number
    try:
        c = re.findall('\d+', s)[0]
    except:
        c = -1
    return int(c)


def load_image_from_directory(path, img_height, img_width):
    # load images from directory and resize to tagert size for training network
    imgs = []
    # walk through base-folder and subfolders
    for path, subpath, files in os.walk(path):
        files.sort(key=sort_key)
        #print(path, files)
        for i in files:
            if i.endswith("jpg") or i.endswith("png"):
                # print(i)
                img = Image.open(path + "/" +i).resize((img_width, img_height))
                # convert images with 2 channels
                if np.asarray(img).shape != (img_width, img_height, 3):
                    img = Image.open(path + "/" +i).convert('RGB').resize((img_width, img_height))
                imgs.append(np.asarray(img))
    
    return np.asarray(imgs)


def get_image(path, img_height, img_width, drop_index):
    # get clean images with complete nutrients
    imgs = load_image_from_directory(path, img_height, img_width)
    print("Original number of images", imgs.shape[0])
    imgs = [i for j, i in enumerate(imgs) if j not in drop_index]
    imgs = np.asarray(imgs)
    
    return imgs


def normalize(imgs):
    return imgs / 255


def plot_nutrients_distribution(nutrient_information, pred_nutrients):
    # input is list
    
    nutrients = []
    predicted_nutrients = []

    for i in range(8):
        nutrients.append([x[i] for x in nutrient_information])
        predicted_nutrients.append([x[i] for x in pred_nutrients])
    
    plt.figure(figsize=(25,25))

    plt.subplot(3,3,1)
    plt.title('calories')
    plt.plot(nutrients[0], label='true')
    plt.plot(predicted_nutrients[0], label='pred')

    plt.subplot(3,3,2)
    plt.title('fat')
    plt.plot(nutrients[1], label='true')
    plt.plot(predicted_nutrients[1], label='pred')

    plt.subplot(3,3,3)
    plt.title('saturatedFat')
    plt.plot(nutrients[2], label='true')
    plt.plot(predicted_nutrients[2], label='pred')

    plt.subplot(3,3,4)
    plt.title('carbohydrate')
    plt.plot(nutrients[3], label='true')
    plt.plot(predicted_nutrients[3], label='pred')

    plt.subplot(3,3,5)
    plt.title('sugar')
    plt.plot(nutrients[4], label='true')
    plt.plot(predicted_nutrients[4], label='pred')

    plt.subplot(3,3,6)
    plt.title('fiber')
    plt.plot(nutrients[5], label='true')
    plt.plot(predicted_nutrients[5], label='pred')

    plt.subplot(3,3,7)
    plt.title('protein')
    plt.plot(nutrients[6], label='true')
    plt.plot(predicted_nutrients[6], label='pred')

    plt.subplot(3,3,8)
    plt.title('sodium')
    plt.plot(nutrients[7], label='true')
    plt.plot(predicted_nutrients[7], label='pred')

    plt.legend()
    
    

