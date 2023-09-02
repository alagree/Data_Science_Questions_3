import pandas as pd
data = pd.read_csv('...cereal.csv')

'''
Create a new 'Type of Cereal' column in your dataframe by copying the 'name' column. Write a function to replace the names of the 
cereal in your new column with one of these categories Bran, Wheat, Fiber, Protein, Crunch, Corn, Nut, Rice and Other. 
Hint: the function should look through the text in the cereal name and determine, based on its contents, how to categorize the cereal type.
'''
import re

def determine_cereal_category(df,list_of_cereal_categories=None):
    '''

    Parameters
    ----------
    df : DataFrame
        Takes as input a DataFrame, which contains at minimum two columns named 'name' and 'Type of Cereal'.
    list_of_cereal_categories : List
        A list of all cereal categories

    Raises
    ------
    Exception
        Raises exception if input variable is not TYPE pandas.DataFrame.

    Returns
    -------
    df : DataFrame
        Returns a DataFrame, where the cereal has been categorized into one of the following categorizes:
            'Bran', 'Wheat', 'Fiber', 'Protein', 'Crunch', 'Corn', 'Nut', 'Rice', based on the cereal name.

    '''
    #Throw exception if input variable is not a DataFrame
    if isinstance(df, pd.DataFrame) == False:
        raise Exception(f"Input variable must be type Pandas DataFrame. Input variable is identified as {type(df)}")
        
    #Create a list of all cereal categories 
    if not list_of_cereal_categories:
        list_of_cereal_categories = ['Bran', 'Wheat', 'Fiber', 'Protein', 'Crunch', 'Corn', 'Nut', 'Rice']
    else:
        list_of_cereal_categories = list_of_cereal_categories
    
    #Iterate over all cereals
    for index, row in df.iterrows():
        #Identify the cereal name
        cereal_name = row['name']
        #As there are multiple delimiters across all cereal names we implement regular expressions. Here
        #we can specify a set of rules to seperate the cereal names.
        cereal_name = re.split("[-:;\*\n\s.''&]", cereal_name)
        #There is one instance where 'Fiber' is spelt 'Fibre'. Identify if it is in the list and change the spelling
        if 'Fibre' in cereal_name:
            cereal_name[cereal_name.index('Fibre')] = 'Fiber'
        #Implement list comprehension to compare the seperated cereal names to the cereal categories
        potential_cereal_category = [word for word in cereal_name if word in list_of_cereal_categories]
        
        if not potential_cereal_category:
            #If there were no matches between the cereal name and categories, then the cereal is labelled as 'other'
            df.loc[index,'Type of Cereal'] = 'Other'
        else:
            #As there can be multiple matches to the cereal category per cereal name (i.e. All-Bran with Extra Fibre)
            #we chose the last identified match as the cereal category. My assumption was that the first few words 
            #in the cereal name identify either the cereal or company name. If the cereal had a longer name such as
            #All-Bran with Extra Fibre the ending of the cereal name identifies the additive or describes the cereal, 
            #in this case Fibre. Therefore, we should categorize this cereal as Fibre not Bran. 
            df.loc[index,'Type of Cereal'] = potential_cereal_category[-1]
    
    return df 
    
data['Type of Cereal'] = data['name'].values

data = determine_cereal_category(data)

data.head()

'''
Identify the negative values in the data set and replace them with the median value for that column.
'''
from pandas.api.types import is_numeric_dtype
import numpy as np

#Iterate over eah column of the DataFrame
for column in data:
    #Identify if the data stored within the column is numeric
    if is_numeric_dtype(data[column]):
        #Identify if there are any values less than 0 (negative)
        if any(data[column].values[data[column].values < 0]):
            #Convert column type to float64 to allow for np.NaN
            data[column] = data[column].astype('float64')
            #Replace negative values with NaN
            data[column].values[data[column].values < 0] = np.NaN
            #Replace NaN's with median value
            data[column] = data[column].replace(np.NaN, data[column].median(skipna=True))
        else:
            continue
    
    else:
        continue

data.head()

'''
Standardize the 'weight' column to 1. For this question, you will need to write a function to divide the 
remaining columns which contain nutritional information by the corresponding value in the weight column, 
and you will need to divide the value in the weight column by itself in order to get 1. For example, 
if an observation has a weight value of 1.33 and a calories value of 250, if you divide 250/1.33 you 
should get a calories value of 188 and a weight value of 1.
'''
def standardize_columns(df,list_of_columns=None):
    '''

    Parameters
    ----------
    df : DataFrame
        Takes as input a DataFrame, which contains nutritional information about the cereals.
    list_of_columns : list
        List of all the nutitional information column names
    
    Raises
    ------
    Exception
        Raises exception if input variable is not TYPE pandas.DataFrame.

    Returns
    -------
    df : DataFrame
        Returns a DataFrame that has standardized the values of: 'calories', 'protein', 'fat', 'sodium', 
        'fiber', 'carbo', 'sugars', 'potass', 'vitamins' in regards to weight.

    '''
    #Throw exception if input variable is not a DataFrame
    if isinstance(df, pd.DataFrame) == False:
        raise Exception(f"Input variable must be type Pandas DataFrame. Input variable is identified as {type(df)}")
    
    #Create a list of all nutritional information
    if not list_of_columns:
        list_of_columns = ['calories', 'protein', 'fat', 'sodium', 'fiber', 'carbo', 'sugars', 'potass', 'vitamins']
    else:
        list_of_columns = list_of_columns
    
    #Iterate over each cereal
    for index, row in df.iterrows():
        #If weight does not equal 1, create a dictionary where the keys are the nutritional information names and values are divided
        #by the weight
        if row['weight'] != 1:
            weight = row['weight']
            standardized = {column_name: value/weight for column_name, value in row.iteritems() if column_name in list_of_columns}
            #Replace the nutritional information values with the standardized ones
            for key, value in standardized.items():
                df.loc[index,key] = value
            #Standardize the weight    
            df.loc[index,'weight'] = weight / weight
                
        else:
            continue
    
    return df

data = standardize_columns(data)

data.head()


'''
Create a new column to categorize cereals as 'healthy' vs. 'unhealthy'. You can define your own version of healthy 
vs. unhealthy, or you can use the following: healthy cereals can be defined as those which have low calories (<100), 
low sodium (<150), low sugar (<9) high fiber (>3), and high protein (>2). All other cereals are unhealthy.
'''
def conditional_tests(nutritional_variables, nutritional_values=None):
    '''

    Parameters
    ----------
    nutritional_variables : str
        String, which identifies the nutritional values name.
    nutritional_values : int64
        Nutritional value.

    Returns
    -------
    result : Bool
        Bool expression of whether the nutritional value falls within the healthy criteria.

    '''
    #Create a dictionary with multiple conditional expressions 
    cond_tests = {'calories': lambda: nutritional_values < 120,
                  'sodium': lambda: nutritional_values < 150,
                  'sugars': lambda: nutritional_values < 8,
                  'fiber': lambda: nutritional_values > 3,
                  'protein': lambda: nutritional_values > 2
                  }
    #Evaluate the nutritional value against the respective conditional expression
    result = cond_tests.get(nutritional_variables)()
    return result 

def determine_healthy_cereal(df,list_of_columns=None):
    '''

    Parameters
    ----------
    df : DataFrame
        Takes as input a DataFrame, which contains nutritional information about the cereals.
    list_of_columns : list
        List of the nutitional information column names to evaluate

    Raises
    ------
    Exception
         Raises exception if input variable is not TYPE pandas.DataFrame.

    Returns
    -------
    df : DataFrame
        Returns a DataFrame, which categorizes each cereal as healthy or unhealthy.

    '''
    #Throw exception if input variable is not a DataFrame
    if isinstance(df, pd.DataFrame) == False:
        raise Exception(f"Input variable must be type Pandas DataFrame. Input variable is identified as {type(df)}")

    #Create a list of nutritional information to evaluate
    if not list_of_columns:
        list_of_columns = ['calories', 'sodium', 'sugars', 'fiber', 'protein']
    else:
        list_of_columns = list_of_columns
    
    #Iterate across all cereals
    for index, row in df.iterrows():
        #Create a dictionary of the cereals nutritional information to evaluate
        nutritional_info = {column_name: value for column_name, value in row.iteritems() if column_name in list_of_columns}    
        #Using the conditional_tests function determine if all the nutiritional values fall within the healthy criteria.
        if all([conditional_tests(column_name, value) for column_name, value in nutritional_info.items()]):
            df.loc[index,'Cereal Category'] = 'healthy'
        else:
            df.loc[index,'Cereal Category'] = 'unhealthy'
            
    return df

data = determine_healthy_cereal(data)
data.head()


'''
Based on your newly prepared data set, identify what % of cereals that each manufacturer produces are healthy.
'''
#My assumption was that the mfr column represented the manufacturer's name
from collections import defaultdict

#Create a default dictionary
dct = defaultdict(list)
#Iterate over all the cereals, creating a key for each manufacturer and appending appending the cereal category to
#the respective manufacturer  
for mfr, value in zip(data['mfr'].values, data['Cereal Category'].values):
    dct[mfr].append(value)

#Iterate across all manufacturers ti determine the percentage of cereals considered healthy
for key, value in dct.items():
    mfr_percentage = (value.count('healthy') / len(value)) * 100

    print(f"{mfr_percentage:.0f}% of the cereals manufacturer {key} produce are considered healthy.")    


'''
Calculate the average, minimum and maximum ratings for healthy vs. unhealthy cereals.
'''
dct = defaultdict(list)
#Iterate over all the cereals, creating a key for each cereal category and appending appending the rating to
#the respective cereal category  
for category, value in zip(data['Cereal Category'].values, data['rating'].values):
    dct[category].append(value)

#Calculate the average value, min, and max per cereal category
for key, value in dct.items():
    avg_value = sum(value) / len(value)
    min_value = min(value)
    max_value = max(value)

    print(f"The following are the descriptive statistics for ratings of {key} cereals: average {avg_value:.2f}, minimum {min_value:.2f}, and maximum {max_value:.2f}.")    

'''
Calculate the average, minimum and maximum ratings for each type of cereal: Bran, Wheat, Fiber, Protein, Crunch, Corn, Nut, Rice and Other.
'''
dct = defaultdict(list)
#Iterate over all the cereals, creating a key for each type of cereal and appending appending the rating to
#the respective type of cereal 
for cereal_type, value in zip(data['Type of Cereal'].values, data['rating'].values):
    dct[cereal_type].append(value)

#Calculate the average value, min, and max per type of cereal
for key, value in dct.items():
    avg_value = sum(value) / len(value)
    min_value = min(value)
    max_value = max(value)

    print(f"The following are the descriptive statistics for ratings of {key} cereals: average {avg_value:.2f}, minimum {min_value:.2f}, and maximum {max_value:.2f}.")    


'''
Create a stacked bar chart which shows how many of each type of cereal each manufacturer produces.
'''
#My assumption was the type of cereal referred to either Bran, Wheat, Fiber, Protein, Crunch, Corn, Nut, Rice and Other. 

import matplotlib.pyplot as plt

dct = defaultdict(list)
#Iterate over all the cereals, creating a key for each manufacturer and appending appending the type of cereal to
#the respective manufacturer
for cereal_type, value in zip(data['mfr'].values, data['Type of Cereal'].values):
    dct[cereal_type].append(value)

#Create an empty DataFrame
df = pd.DataFrame(columns=['mfr','type_of_cereal','count'])
#Iterate over each manufacturer
for key, value in dct.items():
    #Create an empty dictionary
    dct_throwaway = {}
    #Identify all the unique type of cereal produced by the manufacturer
    unique_names = list(dict.fromkeys(value))
    #Count the number of occurences of each type of cereal, per manufacturer
    unique_info = {name: value.count(name) for name in unique_names}    
    dct_throwaway.update(unique_info)
    #Iterate across across all types of cereal per manufacturer and append the results to the master DataFrame 
    for type_key, count_value in dct_throwaway.items():
        df_throwaway = pd.DataFrame([[key,type_key,count_value]], columns=['mfr','type_of_cereal','count'])
        df = df.append(df_throwaway)

#Create a pivot table to reshape the DataFrame per manufacturer
pivot_df = df.pivot(index='mfr', columns='type_of_cereal',values='count')

#Plot a staked bar chart
ax = pivot_df.loc[:,list(pivot_df.columns)].plot.bar(stacked=True, figsize=(10,7))
ax.set_xlabel('Manufacturer')
ax.set_ylabel('Count')
plt.show(ax)
   
'''
Create a 3-dimensional scatterplot which shows the relationship between rating and calories; the 3-rd dimension 
should be reflected in the color of the dots and should highlight whether the cereal is categorized as healthy or unhealthy.
'''
import seaborn as sns

#Create a DataFrame, which contains the rating, calories, and category of each cereal
df = pd.DataFrame(dict({'rating':list(data['rating'].values), 
                        'calories':list(data['calories'].values),  
                        #Coverted the categorical data to numeric (1:healthy,0:unhealthy) so that the data could be plotted
                        'Cereal_Category_numeric':[1 if value=='healthy' else 0 for value in list(data['Cereal Category'].values)],
                        'Cereal_Category':list(data['Cereal Category'].values)}))

sns.scatterplot(x=df['rating'], y=df['calories'], hue=df['Cereal_Category'])

'''
Which shelf has the most healthy cereals?
'''
dct = defaultdict(list)
#Iterate over all the cereals, creating a key for each shelf and appending appending the type of cereal to
#the respective shelf
for cereal_category, value in zip(data['shelf'].values, data['Cereal Category'].values):
    dct[cereal_category].append(value)

#Count the number of healthy cereals per shelf
shelf_count = {column_name: value.count('healthy') for column_name, value in dct.items() if column_name} 

print(f'Shelf 1 holds {shelf_count[1]} healthy cereals, shelf 2 holds {shelf_count[2]} healthy cereals,' 
      f'and shelf 3 holds {shelf_count[3]} healthy cereals. Therefore, shelf {max(shelf_count, key=shelf_count.get)} holds the most healthy cereals.')    






























