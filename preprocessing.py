import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import itertools
from sklearn.feature_selection import VarianceThreshold

application_data = pd.read_csv(r'application_data.csv')
previous_application = pd.read_csv(r'previous_application.csv')
columns_description = pd.read_csv(r'columns_description.csv',skiprows=1)

#clean the previous_application data

# 1.  Remove all the columns from the dataset which are having missing values more than 50%
#1a. get the names of columns from the dataset
column_list = []
column_list = previous_application.columns.values.tolist()

#1b.  traverse through the dataset and find the names of the columns having more than 50% missing values
missing_values_column_list = []

for i in column_list:
    missing_values = previous_application[i].isnull().sum()
    total_values = previous_application[i].shape[0]
    percentage = missing_values*100/total_values
    if percentage > 50:
        missing_values_column_list.append(i)

#1c.  remove the cloumns from the original dataset
previous_application = previous_application.drop(missing_values_column_list,axis=1)

#2.   Replace the missing values of the non-categorical columns by either mean, median or mode
#2a.  Find all the numerial as well as categorical columns
categorical_column_list = previous_application.select_dtypes(include=['object']).columns.tolist()
numerical_column_list = previous_application.select_dtypes(exclude=['object']).columns.tolist()

#2b.  Replace the missing values in numerical columns
#  Mean – When your numerical data has missing values given the values are normally distributed, 
#  we can replace the missing values with the mean of that numerical attribute
#Median – When you see your numerical data is skewed (left/right) . 
#Instead of imputing them with the mean values (that can imbalance your data further). 
#Impute them with the median value of the attribute

#How to detect whether the data is normally distributed?
# apply shapiro-wilk test. It gives two values as output - 1. statistics, 2. p-value
#i if p-value > 0.05, the data is nornally distributed
from scipy.stats import shapiro
skewed_distributed_column_list = []
normally_distributed_column_list = []

for i in numerical_column_list:
    result = shapiro(previous_application[i])
    if result[1]>0.05:
        print(i,result[0],result[1],"Noral")
        normally_distributed_column_list.append(i)
        mean_val = previous_application[i].mean()
        previous_application[i].fillna(mean_val,inplace=True)
    else:
        print(i,result[0],result[1],"Skewed")
        skewed_distributed_column_list.append(i)
        previous_application[i].fillna(previous_application[i].median(),inplace=True)

#2c.  Replace missing values in categorical data
# Replace the missing value with the most frequent value i.e. mode

for i in categorical_column_list:
    missing_count = previous_application[i].isnull().sum()
    mode_value = previous_application[i].mode().iloc[0]
    if(missing_count>0):
        previous_application.fillna(previous_application[i].mode().iloc[0],inplace=True)
        print(i,missing_count,mode_value)	


#3  Remove the outliars from the numeric data using interquartile range method

for i in numerical_column_list:
    iqr1 = previous_application[i].quantile(0.25)
    iqr3 = previous_application[i].quantile(0.75)
    iqr = iqr3-iqr1
    lower_limit = iqr1 - 1.5*iqr
    upper_limit = iqr3 + 1.5*iqr
    temp_data = previous_application[(previous_application[i] > lower_limit) & (previous_application[i] <upper_limit)]
    if temp_data[i].value_counts().shape[0] > 10:
        previous_application = previous_application[(previous_application[i] > lower_limit) & (previous_application[i] <upper_limit)]
        print(i,previous_application.shape)

#4 Remove unwanted columns from the dataset
#4a.  Remove the columns which are having very low variance among the data in the same column

#get only numeric data in other varibale
n_appdata = previous_application[numerical_column_list]

#apply the model to get the column names with 0.0 variance
var_thres = VarianceThreshold(threshold=0.001)
var_thres.fit(n_appdata)

low_var = var_thres.get_support()

#get the names of the columns with 0.0 variance and can be removed
const_cols = []
j=0
for i in low_var:
    if i != True:
        if n_appdata.columns[j] != 'TARGET' and n_appdata.columns[j] != 'SK_ID_CURR':
            print(n_appdata.columns[j])
            const_cols.append(n_appdata.columns[j])
            if numerical_column_list.count(n_appdata.columns[j]) > 0:
                numerical_column_list.remove(n_appdata.columns[j])
        j = j + 1

# OR
#const_cols = [column for column in n_appdata.columns if column not in n_appdata.columns[low_var]]

#drop the columns
previous_application.drop(const_cols, axis=1,inplace=True)

#Remove the elements from coll_corr from numerical_column_list
const_cols = list(set(const_cols))
for i in const_cols:
    if numerical_column_list.count(i):
        numerical_column_list.remove(i)

#4b   Remove the columns which are having high corelation with each other.  So these columns are redundant 
#     and we can remove these columns from our dataset.

n_appdata = previous_application[numerical_column_list]

#plt.figure(figsize=(12,10))
corr_matrix = n_appdata.corr()
#sns.heatmap(cor,annot=True,cmap=plt.cm.CMRmap_r)
#plt.show()

coll_corr = []
threshold = 0.9

for i in range(len(corr_matrix.columns)):
    for j in range(i):
        if abs(corr_matrix.iloc[i,j]) > threshold:
            colname = corr_matrix.columns[i]
            coll_corr.append(colname)
            print(colname)
            #numerical_column_list.remove(colname)

previous_application.drop(coll_corr,axis=1,inplace=True)

#Remove the elements from coll_corr from numerical_column_list
coll_corr = list(set(coll_corr))
for i in coll_corr:
    numerical_column_list.remove(i)

