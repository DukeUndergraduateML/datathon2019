# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import ast

# Load Data set 

def load(file):
    df = pd.read_csv(file)
    
    # convert the column values from literal string to dictionary
    df['ltiFeatures'] = df['ltiFeatures'].apply(ast.literal_eval)
    df['stiFeatures'] = df['stiFeatures'].apply(ast.literal_eval)

    return df

# load all the data
training = load("valassis_dataset/training.csv")
validation = load("valassis_dataset/validation.csv")
interest_topics = pd.read_csv("valassis_dataset/interest_topics.csv")

# Check that all columns from validation set are in training set 
# (can't predict on extra columns)

col1 = []
col2 = []
bad_col = []
for col in pd.DataFrame(list(training['ltiFeatures'])).columns: 
    col1.append(col)
for col in pd.DataFrame(list(validation['ltiFeatures'])).columns:
    col2.append(col)
for i in col2:
    t=0
    for j in col1: 
        if(i == j) : 
            t +=1
    if t < 1: 
        bad_col.append(i)

## Here we create a numpy array for the training data long and short term features. 

nfeatures,n = interest_topics.shape
x_train_lti = np.nan_to_num(pd.DataFrame(list(training['ltiFeatures'])))
x_train_sti = np.nan_to_num(pd.DataFrame(list(training['stiFeatures'])))
y_train = np.nan_to_num(training['inAudience'])

x_val_lti = np.nan_to_num(pd.DataFrame(list(validation['ltiFeatures'])).drop(bad_col, axis=1))
x_val_sti = np.nan_to_num(pd.DataFrame(list(validation['stiFeatures'])))
y_val = np.nan_to_num(validation['inAudience'])


dimensionality_reduction = False; 

if dimensionality_reduction: 
    from sklearn.decomposition import PCA
    pcaTest = PCA(0.99, svd_solver = 'full')
    pcaTest.fit(x_train_lti)
    x_train_lti = pcaTest.transform(x_train_lti)
    x_val_lti = pcaTest.transform(x_val_lti)


# Performance metric calculations
def perf_measure(y_actual, y_hat):
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_hat)): 
        if y_actual[i]==y_hat[i]==1:
           TP += 1
        if y_hat[i]==1 and y_actual[i]!=y_hat[i]:
           FP += 1
        if y_actual[i]==y_hat[i]==0:
           TN += 1
        if y_hat[i]==0 and y_actual[i]!=y_hat[i]:
           FN += 1

    return(TP, FP, TN, FN)
    
def f_Beta_measure(y_actual, y_hat,beta):
    (TP, FP, TN, FN) = perf_measure(y_actual,y_hat)
    
    return ((1+beta**2)*TP)/((1+beta**2)*TP + (beta**2)*FN+ FP)

# Set up ensemble voting classifier
import numpy as np
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

clf1 = LogisticRegression(solver='lbfgs', multi_class='multinomial', random_state=1)
clf2 = RandomForestClassifier(n_estimators=50, random_state=1)
clf3 = GaussianNB()

# Train classifier with hard voting
eclf1 = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='hard')
eclf1 = eclf1.fit(x_train_lti, y_train)
print(f"eclf1 f2 score is: {f_Beta_measure(y_val,eclf1.predict(x_val_lti))}")

# Train classifier with soft voting
eclf2 = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='soft')
eclf2 = eclf2.fit(x_train_lti, y_train)
print(f"eclf2 f2 score is: {f_Beta_measure(y_val,eclf2.predict(x_val_lti))}")

# Train classifier with soft voting
eclf3 = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], 
                                     voting='soft', weights=[2,1,1], flatten_transform=True)
eclf3 = eclf3.fit(x_train_lti, y_train)
print(f"eclf3 f2 score is: {f_Beta_measure(y_val,eclf3.predict(x_val_lti))}")


# Set up Logistic Regression model with roc_auc scoring
clf = LogisticRegressionCV(cv=3, random_state=0, solver='newton-cg', scoring='roc_auc').fit(x_train_lti, y_train)

y_pred = clf.predict(x_val_lti)
clf.score(x_val_lti, y_val)

temp = f_Beta_measure(y_val,y_pred,2)
print(f"Gradient boosting f2 score: {temp}")


# Set up DNN model using keras
from tf.keras.models import Sequential
from tf.keras.layers import Dense

N,nfeat = x_train_lti.shape

model = Sequential()
model.add(Dense(10000, input_dim=nfeat, activation='relu'))
model.add(Dense(1000, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x_train_lti, y_train, epochs=15, batch_size=1000,verbose=0,shuffle=True,validation_split=0.2)

scores = model.evaluate(x_train_lti, y_train)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

predictions = model.predict(x_val_lti[:,:-1])
rounded = [round(x[0]) for x in predictions]
temp = f_Beta_measure(y_val,rounded,2)
print(f"Gradient boosting f2 score: {temp}")

# Set up gradient boosting model 
from sklearn.ensemble import GradientBoostingClassifier 
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1)
clf.fit(x_train_lti, y_train)

pred = clf.predict(x_val_lti)
temp = f_Beta_measure(y_val,pred,2)
print(f"Gradient boosting f2 score: {temp}")















