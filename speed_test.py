import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.metrics import accuracy_score
import time

# Creating a linearly separable dataset using Gaussian Distributions.
# The first half of the number in Y is 0 and the other half 1.
# Therefore I made the first half of the 4 features quite different from
# the second half of the features (setting the value of the means quite
# similar) so that make quite simple the classification between the
# classes (the data is linearly separable).
dataset_prep_start_time = time.time()

dataset_len = 30_000_000
dlen = int(dataset_len / 2)
X_11 = pd.Series(np.random.normal(2, 2, dlen))
X_12 = pd.Series(np.random.normal(9, 2, dlen))
X_1 = pd.concat([X_11, X_12]).reset_index(drop=True)
X_21 = pd.Series(np.random.normal(1, 3, dlen))
X_22 = pd.Series(np.random.normal(7, 3, dlen))
X_2 = pd.concat([X_21, X_22]).reset_index(drop=True)
X_31 = pd.Series(np.random.normal(3, 1, dlen))
X_32 = pd.Series(np.random.normal(3, 4, dlen))
X_3 = pd.concat([X_31, X_32]).reset_index(drop=True)
X_41 = pd.Series(np.random.normal(1, 1, dlen))
X_42 = pd.Series(np.random.normal(5, 2, dlen))
X_4 = pd.concat([X_41, X_42]).reset_index(drop=True)
Y = pd.Series(np.repeat([0, 1], dlen))
df = pd.concat([X_1, X_2, X_3, X_4, Y], axis=1)
df.columns = ["X1", "X2", "X3", "X_4", "Y"]
# df.head()

train_size = 0.80
X = df.drop(["Y"], axis=1).values
y = df["Y"]

# label_encoder object knows how to understand word labels.
label_encoder = preprocessing.LabelEncoder()

# Encode labels
y = label_encoder.fit_transform(y)

# identify shape and indices
num_rows, num_columns = df.shape
delim_index = int(num_rows * train_size)

# Splitting the dataset in training and test sets
X_train, y_train = X[:delim_index, :], y[:delim_index]
X_test, y_test = X[delim_index:, :], y[delim_index:]

# Checking sets dimensions
# print('X_train dimensions: ', X_train.shape, 'y_train: ', y_train.shape)
# print('X_test dimensions:', X_test.shape, 'y_validation: ', y_test.shape)

# Checking dimensions in percentages
total = X_train.shape[0] + X_test.shape[0]
# print('X_train Percentage:', (X_train.shape[0]/total)*100, '%')
# print('X_test Percentage:', (X_test.shape[0]/total)*100, '%')

dataset_prep_stop_time = time.time()
# %%time
print("\nFitting model...\n")
model_fit_starting_time = time.time()

for n in range(10):
    model = XGBClassifier(tree_method="hist")
    model.fit(X_train, y_train)

ending_time = time.time()

# sk_pred = model.predict(X_test)
# sk_pred = np.round(sk_pred)
# sk_acc = round(accuracy_score(y_test, sk_pred), 2)
# print("XGB accuracy using Sklearn:", sk_acc*100, '%')
print(f"It took {(ending_time-model_fit_starting_time):.3f} seconds!")
print(f"It took {(dataset_prep_stop_time - dataset_prep_stop_time):.3f} seconds!")