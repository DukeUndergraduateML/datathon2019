
import tensorly as tl
from tensorly.decomposition import parafac
import numpy as np
from sklearn.decomposition import randomized_svd

import pandas as pd
import ast
import matplotlib.pylab as plt
import scipy.sparse as sparse

def load(file):

    df = pd.read_csv(file)
    
    #convert the column values from literal string to dictionary
    df['ltiFeatures'] = df['ltiFeatures'].apply(ast.literal_eval)
    df['stiFeatures'] = df['stiFeatures'].apply(ast.literal_eval)
    
    return df

# load all the data
training = load("training.csv")
validation = load("validation.csv")
interest_topics = pd.read_csv("interest_topics.csv")

# inspect the data
interest_topics.head()
training.head()
validation.head()


# Turn training data into array
x_train = pd.DataFrame(list(training['ltiFeatures']))
x_train = x_train.sort_index(axis = 1)
x_train.insert(130, "113", np.zeros(96406), True) 
x_train.insert(641, "1670", np.zeros(96406), True) 
x_train.insert(1078, "525", np.zeros(96406), True) 
x_train_data = np.nan_to_num(x_train)
x_train_sti = pd.DataFrame(list(training['stiFeatures']))
x_train_sti = x_train_sti.sort_index(axis = 1)
x_train_sti_data = np.nan_to_num(x_train_sti)

y_train = training['inAudience']
y_train = np.nan_to_num(y_train)
y_train_data = y_train.astype(int)


# Turn valadation data into array
x_val = pd.DataFrame(list(validation['ltiFeatures']))
x_val = x_val.sort_index(axis = 1)
x_val.insert(130, "113", np.zeros(80008), True) 
x_val.insert(628, "1627", np.zeros(80008), True) 
x_val.insert(1079, "525", np.zeros(80008), True) 
x_val_data = np.nan_to_num(x_val)
x_val_sti = pd.DataFrame(list(validation['stiFeatures']))
x_val_sti = x_val_sti.sort_index(axis = 1)
x_val_sti_data = np.nan_to_num(x_val_sti)

y_val = validation['inAudience']
y_val = np.nan_to_num(y_val)
y_val_data = y_val.astype(int)


# Separating data by conversion
x_train_con = x_train_data[y_train,:]
x_train_sti_con = x_train_sti_data[y_train,:]
x_train_not_con = x_train_data[np.logical_not(y_train),:]
x_train_sti_not_con = x_train_sti_data[np.logical_not(y_train),:]

x_val_con = x_val_data[y_val,:]
x_val_sti_con = x_val_sti_data[y_val,:]
x_val_not_con = x_val_data[np.logical_not(y_val),:]
x_val_sti_not_con = x_val_sti_data[np.logical_not(y_val),:]

tensor_train_con = np.stack((x_train_con, x_train_sti_con), axis=2)

tensor = tl.tensor(tensor_train_con)

factors = parafac(tensor, rank=2)