
# MSc final project
## Personalized diet for weight management in patients 
---
You can get eveything that's needed for the project from [here](https://drive.google.com/drive/folders/1LD69mz9t6QqwNIzH1GQru0nnM3NOfMqI?usp=sharing).

Note that github repository **does not** contain all the files due to size limits.


*All the python experiments of this project are carried out using jupyter notebook in local laptop or in the server. In order to keep folders neat and clean, codes are reorganized with necessary refactoryed functions.*


---
## Project Overview
---
To help people make better weight management and keep track of calorie intakes conveniently, a new dataset is collected from two recipe websites in this project, which is used to train a multi-task CNN model that predict calories (as well as category, ingredients, and nutrients) based on food images. Moreover, a iOS mobile application ”CalorieTracker“ is developed to help monitor diets easily where users can predict calories based on food images in real-time, track food intakes, have a clearer understanding of their health status, and make better dietary plans.


---
## Running Environment
---
The python codes are written in python 3.6.8 environment and experimented on Linux servers and Mac OS. 
The application is implemented using Swift in Xcode (version 12.5.1)

Some packetages needed for this task are given here long with its version. 
*tensorflow is not the newest version due to server constraints*

+ keras 2.3.1
+ numpy 1.19.5
+ Pillow 8.3.1
+ tensorflow 2.1.0
+ scikit-image 0.17.2
+ coremltools 4.1

The *coremltools* is used to convert the trained model from .h5 to .mlmodel to be deployed in the iOS application.



---
## Code file descriptions
---
 Most of the ipynb files are provided with complete in-line comments along with expected outputs and annotations.
 
### Data acquisition.ipynb

This file includes functions for creating the dataset, including scraping food images, calories, title, nutrients, ingredients, serving, etc. from two recipe websites: www.bbcgoodfood.com and www.thekitchn.com .

###  Data cleaning.ipynb

This file includes functions for cleaning the collected data, including merge from two sources, remove nan values, remove outliers, download images with wrong format manually, and train-test split.

### Data preparation.ipynb

This file includes functions for preparing targets for the proposed multi-task model, adding category vector, nutrient vector, and ingredient vector as auxiliary targets.

### Data exploration.ipynb

This file explores calorie distributions, and aggregates the calories by source and by category to see if there's any difference between annotations from different recipes sites, and whether categories can influence calorie values.

### Model training per recipe / per serving.ipynb

These two files show the process for training the multi-task models along with training details in the expected output cells.

There are 5 models trained in each file with different outputs: 
+ calorie, 
+ calorie+ingredient, 
+ calories+category, 
+ calorie+nutrients, 
+ calori+ingredient+category+nutrients

### Evaluation.ipynb

This file provides a Class and several help functions to compare trained models.



---
## Folder descriptions
---

### extracted_data
* bbc: includes sub-folders of 12 food categories that have food images collected from www.bbcgoodfood.com
* thekitchen: includes sub-folders of 12 food categories that have food images collected from www.thekitchn.com


### csv_files
* bbc: includes sub-folders of 12 food categories that have structured information collected from www.bbcgoodfood.com
* thekitchen: includes sub-folders of 12 food categories that have structured information collected from www.thekitchn.com


### data
some files are intermediate and below are brief introductions of important files.
* all_data: includes all the collected food images.
* all_data.csv: includes all the structured information of collected food images aggregated by calorie per serving.
* all_data_per_recipe.csv: includes all the structured information of collected food images aggregated by calorie per recipe
* all_data_clean.csv: the outcome of Data cleaning.ipynb
* per_recipe:
  - top_100_ingre_per_recipe.csv: the most common 100 ingredients in the training set.
  - train_per_recipe_complete.csv: add three vectors for the multi-task model.
  - test_per_recipe_complete.csv: add three vectors for the multi-task model.
* per_serving:
  - top_100_ingre_per_serving.csv: the most common 100 ingredients in the training set.
  - train_per_serving_complete.csv: add three vectors for the multi-task model.
  - test_per_serving_complete.csv: add three vectors for the multi-task model.


### server
* Convert_to_coreml.ipynb: convert the multi-task model from .h5 to .mlmodel to be deployed in the iOS application. 
* calorie.mlmodel: the .mlmodel version of the multi-task model with all the vectors as output, predicting calories per serving.
* models: include all the models trained in *Model training per recipe / per serving.ipynb*

### CalorieTracker
The Xcode project file for the iOS mobile application "CalorieTracker".

