import argparse
import time

import numpy as np
import pandas as pd

# import xgboost as xgb
from sklearn import preprocessing
from sklearn.metrics import accuracy_score

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

parser = argparse.ArgumentParser()
# parser.add_argument("-n", "--num_passes", type=int)
parser.add_argument("-s", "--size", type=int)

args = parser.parse_args()
dataset_size = args.size
# num_passes = args.num_passes
# sample = args.sample

# Creating a linearly separable dataset using Gaussian Distributions.
# The first half of the number in Y is 0 and the other half 1.
# Therefore I made the first half of the 4 features quite different from
# the second half of the features (setting the value of the means quite
# similar) so that make quite simple the classification between the
# classes (the data is linearly separable).

print("\nGenerating dataset...")
dataset_prep_start_time = time.time()

dlen = int(dataset_size / 2)
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

TRAIN_SIZE = 0.80
X = df.drop(["Y"], axis=1).values
y = df["Y"]

# label_encoder object knows how to understand word labels.
label_encoder = preprocessing.LabelEncoder()

# Encode labels
y = label_encoder.fit_transform(y)

# identify shape and indices
num_rows, num_columns = df.shape
delim_index = int(num_rows * TRAIN_SIZE)

# Splitting the dataset in training and test sets
X_train, y_train = X[:delim_index, :], y[:delim_index]
X_test, y_test = X[delim_index:, :], y[delim_index:]


# Checking dimensions in percentages
total = X_train.shape[0] + X_test.shape[0]

dataset_prep_stop_time = time.time()


print("Fitting model...")
model_fit_starting_time = time.time()

for n in range(10):
    model = XGBClassifier(tree_method="hist")
    model.fit(X_train, y_train)

model_fit_stop_time = time.time()

print("Predicting with fitted model...")
pred_start_time = time.time()
sk_pred = model.predict(X_test)
sk_pred = np.round(sk_pred)
sk_acc = accuracy_score(y_test, sk_pred)
pred_stop_time = time.time()

print(f"XGB accuracy using Sklearn = {sk_acc * 100:.2f} %")
print(f"\nModel accuracy is {100*sk_acc:.1f} %.")

print(
    f"Data prep. took {(dataset_prep_stop_time - dataset_prep_start_time):.3f} seconds."
)
print(
    f"Fitting model took {(model_fit_stop_time - model_fit_starting_time):.3f} seconds!"
)
print(f"Predicting with model took {(pred_stop_time - pred_start_time):.3f} seconds!")

print(f"\nFinished!")
