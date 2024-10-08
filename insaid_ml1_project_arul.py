# -*- coding: utf-8 -*-
"""INSAID-ML1-PROJECT-ARUL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ft8eSPhfCyPX80p0WsTxg_2BSoFlAFIk

<img src="https://github.com/insaid2018/Term-1/blob/master/Images/INSAID_Full%20Logo.png?raw=true" width="240" height="360" style="float:right"/>  
    
<h1> Machine Learning I: Project Avocado Price Prediction  </h1>
<img src="https://github.com/Ashwani-ML-AL/Images/blob/master/Avocado.JPG?raw=true" width="1050" height="20" style="float:left"/>

   <h1> By : Arul Pandita </h1>

### Table of Contents
- 1. [Problem Statement](#section1)</br>
    - 1.1 [Introduction](#section101)<br/>
    - 1.2 [Data source and data set](#section102)<br/>
- 2. [Load the packages and data](#section2)</br>
- 3. [Exploratory Data Analysis](#section3)</br>   

- 4. [Data Preparation](#section4)</br>
- 5. [Modeling and Evaluation](#section5)<br/>

<a id=section1></a>
## 1. Problem Statement !

Given the data make a model to predict the average price of the avocado.Evaluate the model using possible __model evaluation techniques__.

In this study, we will try to see if we can predict the Avocado’s Average Price based on different features. . The features are different (Total Bags,Date,Type,Year,Region..).

The variables of the dataset are the following:

Categorical: ‘region’,’type’ <br/>
Date: ‘Date’ <br/>
Numerical:‘Unamed: 0’,’Total Volume’, ‘4046’, ‘4225’, ‘4770’, ‘Total Bags’, ‘Small Bags’,’Large Bags’,’XLarge Bags’,’Year’
Target:‘AveragePrice’ <br/>


<a id=section101></a>
### 1.1. Introduction
This Project is to understand the fundamentals of the Machine Language I, I have taken avacado data set provided by Insaid and will try to predect the price , data would be used for test and train,so as to predect model evalution.

<a id=section102></a>
### 1.2. Data source and dataset

Date - The date of the observation <br/>
AveragePrice - the average price of a single avocado - target variable <br/>
type - conventional or organic <br/>
year - the year <br/>
Region - the city or region of the observation <br/>
Total Volume - Total number of avocados sold <br/>
4046 - Total number of avocados with PLU 4046 sold <br/>
4225 - Total number of avocados with PLU 4225 sold <br/>
4770 - Total number of avocados with PLU 4770 sold <br/>

Unamed: 0’ : Its just a useless index feature that will be removed later <br/>
,’Total Volume’ : Total sales volume of avocados<br/>
‘4046’ : Total sales volume of Small/Medium Hass Avocado<br/>
‘4225’ : Total sales volume of Large Hass Avocado<br/>
‘4770’ : Total sales volume of Extra Large Hass Avocado<br/>
‘Total Bags’: Total number of Bags sold<br/>
‘Small Bags’: Total number of Small Bags sold <br/>
Large Bags’: Total number of Large Bags sold <br/>
‘XLarge Bags’: Total number of XLarge Bags sold <br/>

Data: https://github.com/insaid2018/Term-2/blob/master/Term-I-II%20EDA%20Project%20Datasets.ipynb <br/>

<a id=section2></a>
### 2. Load the packages and data
"""

# Commented out IPython magic to ensure Python compatibility.
import sys                                                                      # Import packages
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import pie, axis, show
# %matplotlib inline
from sklearn import metrics
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)
from subprocess import check_output
import warnings                                                                 # Ignore warning related to pandas_profiling
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 100)                                       # Display all dataframe columns in outputs (it has 27 columns, which is wider than the notebook)
                                                                            # This sets it up to dispaly with a horizontal scroll instead of hiding the middle columns
print('done')

"""Read in the Avocado Prices csv file as a DataFrame called AD"""

AD = pd.read_csv("https://raw.githubusercontent.com/Ashwani-ML-AL/Data/main/avocado.csv")

"""<a id=section3></a>
### 3. Exploratory Data Analysis

Lets check our data head:
"""

AD.head(2)

AD.shape

AD.columns

AD.type.value_counts()  # Balanced Dataset

AD.region.value_counts() # Balanced DataSet

AD.year.value_counts() # Year for 2015,2016 and 2017 are balanced but 2018 would not be balanced data with other year

AD.describe()
#AD.describe(include = 'all')

AD.info()

AD.isnull().sum()  # No Null Values

"""###### Observation :

No Missing Values (18249 complete data) and 13 columns.

Feature Engineering on the Date Feature so we can be able to use the month columns in building our machine learning model later


"""

# Convert Date column from object to date
AD.Date = pd.to_datetime(AD.Date)

AD.info()  # Get General idea about our data:

AD.isnull().sum()  # Just to check again

"""### Preprocessing the data ###

1.  Create new column "Month" by splitting date column.
2.  Columns 4046, 4225, 4770 represent the PLU code of the small, large and extra large avacadoes.
3.  We can drop date column as we have Month and Year in the dataframe.
4.  Drop the unnamed column as well as this seems to be serial number.
5.  AveragePrice is the label that i am selecting and will try to predict the price.
6.  No need of scaling data using ( StandardScaler or RobustScaler)

"""

AD['Month'] = AD.Date.dt.month
#AD['Day'] = AD.Date.dt.day

"""The Feature "Unnamed:0" is just a representation of the indexes, so it's useless to keep it, lets remove it !"""

AD.head(2)

"""Now lets do some plots!! I'll start by plotting the Avocado's Average Price through the Date column"""

plt.figure(figsize=(12,5))                        # Distribution curve for AverageProce ( Traget Variable)
plt.title("Price Distribution Graph")
ax = sns.distplot(AD["AveragePrice"], color = 'blue')

"""We could notice that the price is slightly right skewed and most of the time the price is between 1 and 1.7"""

dategroup=AD.groupby('Month').mean()
plt.figure(figsize=(20,5))
dategroup['AveragePrice'].plot(x=AD.Month)
plt.title('Average Price')

dategroup=AD.groupby('Month').mean()
plt.figure(figsize=(20,5))
dategroup['Total Volume'].plot(x=AD.Month)
plt.title('Total Volume')

"""From the above chart we could infer that

*   We could observe from this graph that September and October are the months where the price seems to be at its highest
*   February is the month where the price seems to be the lowest.
*   Though the volume almost remained same, price seems to increase year on year

By comparing two charts above we could see that sometimes price and volume and inversely proportional(i.e. When volume increases price decreases)

This confirms our previous observation that Feb is the lowest price month and oct and Nov seems to be the highest priced months
"""

# Sales per year
'''plt.figure(figsize=(35,5))
sns.countplot('year',data = AD,palette="prism")
plt.title("Number of  Sales per Year",fontsize=18,fontweight="bold")
plt.xlabel('Year')
plt.ylabel('Sales Numbers')
plt.show()'''

# Check % of type for each year
'''f,ax = plt.subplots(1,4,figsize=(25,6))
AD['type'][AD['year'] == 2015].value_counts().plot.pie(explode=[0,0.2],autopct='%1.1f%%',ax=ax[0],shadow=True)
AD['type'][AD['year'] == 2016].value_counts().plot.pie(explode=[0,0.2],autopct='%1.1f%%',ax=ax[1],shadow=True)
AD['type'][AD['year'] == 2017].value_counts().plot.pie(explode=[0,0.2],autopct='%1.1f%%',ax=ax[2],shadow=True)
AD['type'][AD['year'] == 2018].value_counts().plot.pie(explode=[0,0.2],autopct='%1.1f%%',ax=ax[3],shadow=True)
ax[0].set_title('Year 2015')
ax[1].set_title('Year 2016')
ax[2].set_title('Year 2017')
ax[3].set_title('Year 2018')'''

AD.groupby(['region'])['AveragePrice'].mean().sort_values()[:100].plot(kind='barh', figsize=(40,15), fontsize=15, color='orange')
plt.ylabel('Price (in million INR)')

plt.figure(figsize=(17,10))
sns.jointplot('Total Volume','AveragePrice',data=AD,kind='reg')

#plt.figure(figsize=(17,10))
sns.jointplot('year','AveragePrice',data=AD,kind='reg')

# Using seaborn's regplot function to plot the scatter plot for the Year and Price columns with the regression line.
# done just for revision

'''plt.figure(figsize=(17,10))
sns.regplot(data=AD, x='year', y='AveragePrice', color='brown')

plt.title('Plot showing the variation of Price with Year')'''

# done just for revision
'''AD.plot(kind='scatter', x='year', y='AveragePrice', figsize=(7, 4), color='purple', grid=True)

plt.title('Scatter plot showing the variation per year  with price')'''

# First time i am using this shart, good chart showing price variance since 2015-2018
plt.figure(figsize=(20,20))
sns.pointplot(x='AveragePrice',y='region',data=AD, hue='year',join=False)
plt.xlabel('Region',{'fontsize' : 'large'})
plt.ylabel('Average Price',{'fontsize':'large'})
plt.title("Yearly Average Price in Each Region",{'fontsize':20})

"""Hartfordspringfield and San Fransisco seems to be the costliest states while southcentral and houston remains to be the cheapest."""

corr_matrix = AD.corr()
AD.tail(2)

"""We will be converting only the avacado type to two different columns"""

sns.pairplot(AD[["type", "region", "Total Volume", "year", "Month", "AveragePrice"]], diag_kind="kde")

"""***We are not doing an inplace replacement while dropping so as to find any relation between the dropped columns***"""

#We will be converting only the avacado type to two different columns
#AD.hist(bins=50, figsize=(20,15))
corr1 =  corr_matrix["AveragePrice"].sort_values(ascending=False)
n = pd.get_dummies(AD.type)
AD = pd.concat([AD, n], axis=1)
#m = pd.get_dummies(AD.region)
#AD= pd.concat([SD, m], axis=1)
drops = ['AveragePrice']
print(corr1)

#AD_subset = AD.drop(['Unnamed: 0', '4046','4225','4770','Small Bags', 'Large Bags', 'XLarge Bags','type','Date','Total Bags'], axis=1)
AD_subset = AD.drop(['Unnamed: 0', 'type','Date'], axis=1)
AD_subset.head(1)

"""###### Understanding the data using profile report and correlation matrix###
 not using profile report ...

Now lets have an idea about the relationship between our Features(Correlation)
"""

corr = AD_subset.corr()
plt.figure(figsize=(30,15))
sns.heatmap(corr,vmax=.8,linewidth=.01, square = True, annot = True,cmap='YlGnBu',linecolor ='black')
plt.title('Correlation between features')

"""As we can from the heatmap above, all the Features are not corroleted with the Average Price column, instead most of them are correlated with each other. So now I am bit worried because that will not help us get a good model. Lets try and see. First we have to do some Feature Engineering on the categorical Features : region and type

Tring to some features of correlation graph
"""

np.tril(np.ones(corr.shape)).astype(np.bool)[0:5,0:5]

'''array([[ True, False, False, False, False],
       [ True,  True, False, False, False],
       [ True,  True,  True, False, False],
       [ True,  True,  True,  True, False],
       [ True,  True,  True,  True,  True]])'''

df_lt = corr.where(np.tril(np.ones(corr.shape)).astype(np.bool))

df_lt.iloc[0:5,0:3]

hmap=sns.heatmap(df_lt,cmap="Spectral")
hmap.figure.savefig("Correlation_Heatmap_Lower_Triangle_with_Seaborn.png",
                    format='png',
                    dpi=250)

"""### Using Mask"""

#  create a numpy array to use it as our mask.
mask_ut=np.triu(np.ones(corr.shape)).astype(np.bool)

'''Here we create a boolean matrix with True on upper triangular matrix and False on lower
triangular correlation matrix with Numpy’s np.triu() function.'''
mask_ut[0:5,0:5]

# The mask argument will mask the upper triangular matrix and make us a heatmap with lower triangular matrix.
sns.heatmap(corr, mask=mask_ut, cmap="Spectral")
hmap.figure.savefig("Correlation_Heatmap_Lower_Triangle_with_Seaborn_using_mask.png",
                    format='png',
                    dpi=150)

"""as we can see we have 54 regions and 2 unique types, so it's going to be easy to to transform the type feature to dummies, but for the region its going to be a bit complexe so I decided to drop the entire column. I will drop the Date Feature as well because I already have 3 other columns for the Year, Month and Day."""

# Violen plot showing Price spread per year
'''import plotly.express as px

plt.figure(figsize=(15,8));
sns.violinplot(data=AD, x='year', y='AveragePrice',palette='magma');
plt.ylim(0,4,.3);
plt.title('Violen plot showing Price spread')'''

# Box plot showing Price spread per year
'''
plt.figure(figsize=(15, 9))
sns.boxplot(data=AD,x='year',y='AveragePrice',palette='viridis',width=0.2)
plt.ylim(0,4,.3);
plt.xticks(rotation=90)
plt.title('Box plot showing Price spread')'''

#pdpf.ProfileReport(AD_subset)

"""<a id=section4></a>
## 4. Data Preparation
Since now it is a clean dataset, Data Wrangling is not required. Hence here we will be mainly focussing on Feature Engineering and Scaling.

### Feature Extraction and Engineering:

We will extract the existing features and outcomes in separate variables.

###### Splitting the data into train and test after extracting the lable(AveragePrice) that we are going to predict ###

***Encoding columns region and type of avacadoes so that they can be fed as input to the model***

<a id=section5></a>
# Modeling and Evaluation

##### Logistic Regression
"""

#AD= AD.drop(['conventional', 'organic'], axis=1) # did not work well
AD.head(1)

AD_subset.head(1)

"""Now data is ready! lets apply our model which is going to be the __Linear Regression__ because our Target variable 'AveragePrice'is continuous.

Let's now begin to train out regression model!

We will need to first split up our data into an X array that contains the features to train on, and a y array with the target variable
"""

from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
label_encoder.fit(AD_subset.region)
label_encoder.classes_
AD_subset.region =  label_encoder.transform(AD_subset.region)
print('done ji')

AD_subset.head(1)

"""**Splitting the data into train and test**

Creating and Training the Model


"""

X = AD_subset.loc[:,AD_subset.columns != 'AveragePrice']
Y = AD_subset.AveragePrice
AD_subset.AveragePrice.sort_values(ascending= False)

#AD_subset.head(5)
#X.head(1) # check data
Y.head(1)  # check data

X.shape

Y.shape

# Came back and tried this .. did not work
# X = X.drop(['4046', '4225','4770','Small Bags','Large Bags','XLarge Bags'], axis=1)

X.head(1)

#!pip install scikit-learn
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=1)

"""**Evaluating different Models**"""

# First evaluating LinearRegression
from sklearn.linear_model import LinearRegression
LinearRegressionModel = LinearRegression(fit_intercept = False, normalize = False).fit(X_train, y_train)
print("Model Accuracy using Linear Regression is", LinearRegressionModel.score(X_test, y_test))

"""Accuracy Score is low, need to try other model evaluation"""

# regression coefficients , read this so was trying it
print('Coefficients: \n', LinearRegressionModel.coef_)

"""The sign of a regression coefficient tells you whether there is a positive or negative correlation between each independent variable the dependent variable. A positive coefficient indicates that as the value of the independent variable increases, the mean of the dependent variable also tends to increase. A negative coefficient suggests that as the independent variable increases, the dependent variable tends to decrease."""

# variance score: 1 means perfect prediction , read this result same as Accuracy score
print('Variance score: {}'.format(LinearRegressionModel.score(X_test, y_test)))

"""Predect the model using MAE,MSE and RMSE"""

predLR=LinearRegressionModel.predict(X_test)

from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, predLR))
print('MSE:', metrics.mean_squared_error(y_test, predLR))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predLR)))

"""The RMSE is low so we can say that we do have a good model, but lets check to be more sure."""

## Residual Error plot looks like this:
## plotting residual errors in training data
plt.scatter(LinearRegressionModel.predict(X_train), LinearRegressionModel.predict(X_train) - y_train,
            color = "green", s = 2, label = 'Train data')
## plotting residual errors in test data
plt.scatter(LinearRegressionModel.predict(X_test), LinearRegressionModel.predict(X_test) - y_test,
            color = "blue", s = 2, label = 'Test data')
## plotting line for zero residual error
plt.hlines(y = 0, xmin = 0, xmax = 1.5, linewidth = 2)
## plotting legend
plt.legend(loc = 'upper left')
## plot title
plt.title("Residual errors")

## function to show plot
plt.show()

"""Plotting the y_test vs the predictions."""

plt.scatter(x=y_test,y=predLR)

"""As we can see that we dont have a straigt line so I am not sure that this is the best model we can apply on our data

###### GridSearchCV Model

##### Use Hyper Parameter tuning
"""

numberlist = []
for x in range (2, 7):
    numberlist.append(x)
print(numberlist)

from sklearn import neighbors
from sklearn.model_selection import GridSearchCV

#using gridsearch to find the best parameter
params = {'n_neighbors':numberlist}
KNG = neighbors.KNeighborsRegressor()
KNG_model = GridSearchCV(KNG, params, cv=3)
KNG_model.fit(X_train, y_train)
score = KNG_model.score(X_test,y_test)
print("Model Accuracy using KNG regressor is:",score)

predCV=KNG_model.predict(X_test)

from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, predCV))
print('MSE:', metrics.mean_squared_error(y_test, predCV))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predCV)))

"""The RMSE is low so we can say that we do have a good model, but lets check to be more sure."""

plt.scatter(x=y_test,y=predCV)
plt.xlabel('Y Test')
plt.ylabel('Predicted Y')

"""As we can see we have a straigt line so model could be the best one

"""

print(X_train.shape)

print(y_train.shape)

"""#####  DecisionTree Regressor model


"""

from sklearn.tree import DecisionTreeRegressor
modelDT=DecisionTreeRegressor(max_features='auto', random_state=0)
modelDT.fit(X_train,y_train)
#pred=dtr.predict(X_test)


'''bootstrap=True, ccp_alpha=0.0, criterion='mse',
                      max_depth=None, max_features='auto', max_leaf_nodes=None,
                      max_samples=None, min_impurity_decrease=0.0,
                      min_impurity_split=None, min_samples_leaf=1,
                      min_samples_split=2, min_weight_fraction_leaf=0.0,
                      n_estimators=100, n_jobs=None, oob_score=False,
                      random_state=0, verbose=0, warm_start=False)'''

y_pred_trainDT = modelDT.predict(X_train)

y_pred_testDT = modelDT.predict(X_test)

predDT=modelDT.predict(X_test)

scoreDT=modelDT.score(X_test, y_test)
print("Model Accuracy using KNG regressor is:",scoreDT)

plt.scatter(x=y_test,y=predDT)
plt.xlabel('Y Test')
plt.ylabel('Predicted Y')

"""Nice, here we can see that we nearly have a straigt line, in other words its better than the Linear regression model, and to be more sure lets check the RMSE"""

from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, predDT))
print('MSE:', metrics.mean_squared_error(y_test, predDT))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predDT)))

"""RMSE is lower than the Linear Regression model and GridSearchCV.

Let's try RandomForestRegressor to see if it improve  predictions

###### RandomForestRegressor model

In this i will create two models using hyperparameters
"""

# Test Train for Randon Forest Regressor
from sklearn.model_selection import train_test_split
X_train_RFR, X_test_RFR, y_train_RFR, y_test_RFR = train_test_split(X, Y, test_size=0.25, random_state=1)

print(X_train_RFR.shape)
print(y_train_RFR.shape)

print(X_test_RFR.shape)
print(y_test_RFR.shape)

from sklearn.ensemble import RandomForestRegressor
model1RFR = RandomForestRegressor(random_state = 0)

from sklearn.ensemble import RandomForestRegressor

model2RFR = RandomForestRegressor(random_state=1, n_estimators=50,
                                   bootstrap=True,  min_samples_split=2,
                                   n_jobs=10, min_samples_leaf=1,
                                   max_features='auto',oob_score=True)

model1RFR.fit(X_train_RFR,y_train_RFR)

model2RFR.fit(X_train_RFR, y_train_RFR)

print('Random Forest Regressor score for model 1 is": ', model1RFR.score(X_test_RFR, y_test_RFR))

print('Random Forest Regressor score for model 2 is": ', model2RFR.score(X_test_RFR, y_test_RFR))

pred1RFR=model1RFR.predict(X_test_RFR)

"""The Mean Squared Error (MSE) or Mean Squared Deviation (MSD) of an estimator measures the average of error squares i.e. the average squared difference between the estimated values and true value. It is a risk function, corresponding to the expected value of the squared error loss. It is always non – negative and values close to zero are better."""

print('MAE:', metrics.mean_absolute_error(y_test_RFR, pred1RFR))
print('MSE:', metrics.mean_squared_error(y_test_RFR, pred1RFR))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test_RFR, pred1RFR)))

pred2RFR=model2RFR.predict(X_test_RFR)

print('MAE:', metrics.mean_absolute_error(y_test_RFR, pred2RFR))
print('MSE:', metrics.mean_squared_error(y_test_RFR, pred2RFR))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test_RFR, pred2RFR)))



"""Well as we can see the RMSE of RF model1 (model1RFR)is lower than the two previous models, so the RandomForest Regressor is the best model in this case.


"""

sns.distplot((y_test_RFR-pred1RFR),bins=50)

"""Notice here that our residuals looked to be normally distributed and that's really a good sign which means that our model was a correct choice for the data.

Below table is just a data frame representation of the first 5 y_test(the average price that exists in the data) and pred ( the predicted value of the average price by the model 'Random Forest Regressor), as you can see they are very close to each other.
"""

data = pd.DataFrame({'Y Test':y_test_RFR, 'Pred':pred1RFR},columns=['Y Test','Pred'])
sns.lmplot(x='Y Test',y='Pred',data=data,palette='rainbow')
data.head(6)

"""- __Model Evaluation__ using __R2 score ( Model1 of RF)"""

from sklearn.metrics import r2_score

pred3RFR=model1RFR.predict(X_train_RFR)
#pred3=model2RFR.predict(X_train_RFR)

### Assume y is the actual value and f is the predicted values
#y =[10, 20, 30]
#f =[10, 20, 30]
r2 = r2_score(y_test_RFR, pred1RFR)
print('r2 score for perfect test model is', r2)

r3 = r2_score(y_train_RFR, pred3RFR)
print('r2 score for train model is', r3)

# Gives summary of data model->gives value of r-square and adjusted r-square
import statsmodels.formula.api as sm
#X_opt = s.iloc[:, :-1]
#Y1 = s.iloc[:, -1]

#import statsmodels.api as sm
#import statsmodels.api as sm

import statsmodels.api as sm

regressor_OLS = sm.OLS(endog = pred3RFR, exog = y_train_RFR).fit()
regressor_OLS.summary()

