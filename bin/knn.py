# importing necessary libraries
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import sys
import numpy as np
from src.controller.IdentificationController import IdentificationController
import pickle

# loading the iris dataset
cont = IdentificationController()
data, label = cont.load_data_image()
iris = datasets.load_iris()

# X -> features, y -> label
X = iris.data
y = iris.target

n = 128

for i, row in enumerate(data):
    minus_length = n - len(row)

    new_array = np.full([minus_length, 32], -99)
    data[i] = np.concatenate((data[i], new_array), axis=0)
    data[i] = np.concatenate(data[i])

for i, row in enumerate(data):
    break
    print(len(row))


# dividing X, y into train and test data

imp = SimpleImputer(missing_values=-99, strategy='constant', copy=False)
imp = imp.fit(data)
X_train = imp.transform(data)
# training a KNN classifier

knn = KNeighborsClassifier(n_neighbors=9).fit(X_train, label)
filename = 'finalized_model.sav'
pickle.dump(knn, open(filename, 'wb'))
sys.exit()
# accuracy on X_test
accuracy = knn.score(X_test, y_test)


# creating a confusion matrix
knn_predictions = knn.predict(X_test)

for i, row in enumerate(y_test):
    print("{}\npredict: {}\n\n".format(row, knn_predictions[i]))
print(accuracy)
cm = confusion_matrix(y_test, knn_predictions)
