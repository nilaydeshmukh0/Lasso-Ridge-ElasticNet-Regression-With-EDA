"""
Created on Tue Mar 24 11:48:10 2020
by - Deshmukh
LASSO AND RIDGE
"""
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pylab as plt
import pylab
import seaborn as sns

from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split

# ===================================================================================================
# Business Problem :- Perform the Lasso and Ridge Regression to Predict sales Price of the computer.
# ===================================================================================================

computerdata = pd.read_csv("Computer_Data.csv",index_col = 0) 
computerdata.shape
computerdata.isnull().sum()
computerdata.head()

############################### - Exploratory Data Analysis - ###################################### 

# Mesures of Central Tendancy / First moment business decision
computerdata.mean()
computerdata.median()
computerdata.mode()

# Measure of Dispersion / Second moment of business decision
computerdata.var()
computerdata.std()

# Skewness / Thired moment business decision
computerdata.skew()

# Kurtosis / Forth moment business decision
computerdata.kurt() 

# Graphical Representation
computerdata.hist(grid = False)

# Box plot
plt.boxplot(computerdata.price) # Outliers
plt.boxplot(computerdata.speed) # No Outliners
plt.boxplot(computerdata.hd) # Outliers
plt.boxplot(computerdata.ads) # No Outliers
plt.boxplot(computerdata.trend) # No Outliers
 
# Pair plot
sns.pairplot(computerdata,size = 1)

# Correlation coiffient 
computerdata.corr()

# Heat map
sns.heatmap(computerdata.corr(),annot = True,cmap = 'Blues')

############################### - Splitting data in X and Y - ######################################

X = computerdata.iloc[:,1:]
y = computerdata.iloc[:,1]

############################### - Converting Dummy Variable - ######################################

cd = pd.get_dummies(computerdata.cd,drop_first = True,prefix = 'cd')
multi = pd.get_dummies(computerdata.multi,drop_first = True,prefix = 'multi')
premium = pd.get_dummies(computerdata.premium,drop_first = True,prefix = 'premium')

# Droping nomial data columns
X = X.drop(['cd','multi','premium'],axis = 1) 

# Concating dummy variable state coulmns with X
X = pd.concat([X,cd,multi,premium],axis = 1)

############################ - Spliting Data in Train and Test - ###################################

X_train,X_test,y_train,y_test = train_test_split(X,y, test_size = 0.3 , random_state = 0)

##################################### - Losso Regression - ##########################################

### Running a LASSO Regressor of set of alpha values and observing how the R-Squared, train_rmse and test_rmse are changing with change in alpha values
train_rmse = []
test_rmse = []
R_sqrd = []
alphas = np.arange(0,10,0.1)
for i in alphas:
    LRM = Lasso(alpha = i,normalize=True,max_iter=500)
    LRM.fit(X_train,y_train)
    R_sqrd.append(LRM.score(X_train,y_train))
    train_rmse.append(np.sqrt(np.mean((LRM.predict(X_train) - y_train)**2)))
    test_rmse.append(np.sqrt(np.mean((LRM.predict(X_test) - y_test)**2)))
    
# Plotting Alpha vs Train and Test RMSE.
plt.scatter(x=alphas,y=R_sqrd);plt.xlabel("alpha");plt.ylabel("R_Squared")
plt.scatter(x=alphas,y=train_rmse);plt.xlabel("alpha");plt.ylabel("RMSE")
plt.scatter(x=alphas,y=test_rmse);plt.xlabel("alpha");plt.ylabel("RMSE")
plt.legend(("alpha Vs R_Squared","alpha Vs train_rmse","alpha Vs test_rmse"))


##Another Way of finding alpha value by using GV but above is best than this
#from sklearn.model_selection import GridSearchCV
#lasso=Lasso()
#params={'alpha':np.arange(0,500,10)}
#Regressor=GridSearchCV(lasso,params,scoring='neg_mean_squared_error',cv=10)
#Regressor.fit(X,y)
##Print best parameter and score
#print('best parameter: ', Regressor.best_params_)
#print('best score: ', -Regressor.best_score_)


# Preparing Lasso Regression by considering alpha = 0.01 from above
LassoM1 = Lasso(alpha = 0.01, normalize=True)
LassoM1.fit(X_train,y_train)

# Parameters of model
LassoM1.coef_
LassoM1.intercept_

# Adjusted R-Squared value 
LassoM1.score(X_train,y_train) # 0.9999

# Predication on Train and Test 
pred_train_lasso = LassoM1.predict(X_train)
pred_test_lasso = LassoM1.predict(X_test)

# Train and Test RMSE value
np.sqrt(np.mean((pred_train_lasso-y_train)**2)) # 0.66
np.sqrt(np.mean((pred_test_lasso-y_test)**2)) # 0.66

# Importanat Coefficient Plot
important_coff = pd.Series(LassoM1.coef_,index = X.columns)
important_coff.plot(kind = 'barh')

##################################### - Ridge Regression - ##########################################

### Running a Ridge Regressor of set of alpha values and observing how the R-Squared, train_rmse and test_rmse are changing with change in alpha values
train_rmse = []
test_rmse = []
R_sqrd = []
alphas = np.arange(0,10,0.1)
for i in alphas:
    RM = Ridge(alpha = i,normalize=True,max_iter=500)
    RM.fit(X_train,y_train)
    R_sqrd.append(RM.score(X_train,y_train))
    train_rmse.append(np.sqrt(np.mean((RM.predict(X_train) - y_train)**2)))
    test_rmse.append(np.sqrt(np.mean((RM.predict(X_test) - y_test)**2)))
    
# Plotting Alpha vs Train and Test RMSE.
plt.scatter(x=alphas,y=R_sqrd);plt.xlabel("alpha");plt.ylabel("R_Squared")
plt.scatter(x=alphas,y=train_rmse);plt.xlabel("alpha");plt.ylabel("RMSE")
plt.scatter(x=alphas,y=test_rmse);plt.xlabel("alpha");plt.ylabel("RMSE")
plt.legend(("alpha Vs R_Squared","alpha Vs train_rmse","alpha Vs test_rmse"))

# Preparing Ridge Regression by considering alpha = 0.01 from above
RidgeM1 = Ridge(alpha = 0.01, normalize=True)
RidgeM1.fit(X_train,y_train)

# Parameters of model
RidgeM1.coef_
RidgeM1.intercept_

# Adjusted R-Squared value 
RidgeM1.score(X_train,y_train) # 0.999

# Predication on Train and Test 
pred_train_ridge = RidgeM1.predict(X_train)
pred_test_ridge = RidgeM1.predict(X_test)

# Train and Test RMSE value
np.sqrt(np.mean((pred_train_ridge-y_train)**2)) # 0.23
np.sqrt(np.mean((pred_test_ridge-y_test)**2)) # 0.23

# Importanat Coefficient Plot
important_coff = pd.Series(RidgeM1.coef_,index = X.columns)
important_coff.plot(kind = 'barh',color = 'g')

##################################### - Elastic Net Regression - ##########################################

### Running a Elastic Net Regressor of set of alpha values and observing how the R-Squared, train_rmse and test_rmse are changing with change in alpha values
train_rmse = []
test_rmse = []
R_sqrd = []
alphas = np.arange(0,1,0.1)
for i in alphas:
    EN = ElasticNet(alpha = i,normalize=True,max_iter=500)
    EN.fit(X_train,y_train)
    R_sqrd.append(EN.score(X_train,y_train))
    train_rmse.append(np.sqrt(np.mean((EN.predict(X_train) - y_train)**2)))
    test_rmse.append(np.sqrt(np.mean((EN.predict(X_test) - y_test)**2)))
    
# Plotting Alpha vs Train and Test RMSE.
plt.scatter(x=alphas,y=R_sqrd);plt.xlabel("alpha");plt.ylabel("R_Squared")
plt.scatter(x=alphas,y=train_rmse);plt.xlabel("alpha");plt.ylabel("RMSE")
plt.scatter(x=alphas,y=test_rmse);plt.xlabel("alpha");plt.ylabel("RMSE")
plt.legend(("alpha Vs R_Squared","alpha Vs train_rmse","alpha Vs test_rmse"))

# Preparing Elastic Net Regression by considering alpha = 0.00001 from above
Elastic = ElasticNet(alpha = 0.00001, normalize=True)
Elastic.fit(X_train,y_train)

# Parameters of model
Elastic.coef_
Elastic.intercept_

# Adjusted R-Squared value 
Elastic.score(X_train,y_train) # 0.99

# Predication on Train and Test 
pred_train_elastic = Elastic.predict(X_train)
pred_test_elastic= Elastic.predict(X_test)

# Train and Test RMSE value
np.sqrt(np.mean((pred_train_elastic-y_train)**2)) # 0.5
np.sqrt(np.mean((pred_test_elastic-y_test)**2)) # 0.5

# Importanat Coefficient Plot
important_coff = pd.Series(Elastic.coef_,index = X.columns)
important_coff.plot(kind = 'barh',color = 'r')


# Form Above Three models Losso is giving us best result so we can be use it for future prediction.


                    # ---------------------------------------------------- #

