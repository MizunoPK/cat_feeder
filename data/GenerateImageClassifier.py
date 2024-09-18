import os
import pickle
from skimage.io import imread
from skimage.transform import rescale
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Prepare data
print("Preparing Data...")
input_dir = "./data/CatPics"
categories = ["nori_orig", "bento_orig"]

data = []
labels = []
for category_idx, category in enumerate(categories):
    for file in os.listdir(os.path.join(input_dir, category)):
        img_path = os.path.join(input_dir, category, file)
        img = imread(img_path)
        img = rescale(img, (.25/.7))
        img_flat = img.flatten()
        try:
            np.asarray([img_flat])
        except:
            continue
        data.append(img_flat)
        labels.append(category_idx)

data = np.asarray(data)
labels = np.asarray(labels)


# train / test split
print("Splitting the train & test sets")
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# train classifier
print("Training...")
classifier = SVC()

parameters = [{'gamma': [0.01, 0.001, 0.0001], 'C': [1, 10, 100, 1000]}]

grid_search = GridSearchCV(classifier, parameters)

grid_search.fit(x_train, y_train)

# test performance
print("Testing Performance...")
best_estimator = grid_search.best_estimator_

y_prediction = best_estimator.predict(x_test)

score = accuracy_score(y_prediction, y_test)

print('{}% of samples were correctly classified'.format(str(score * 100)))

pickle.dump(best_estimator, open('./model.p', 'wb'))