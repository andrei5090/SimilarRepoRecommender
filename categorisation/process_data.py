import pandas as pd
import numpy as np
import pickle
from os.path import exists
import matplotlib.pyplot as plt

from sklearn.cluster import AgglomerativeClustering

df = pd.read_csv('data.csv')

print(df)
left_array_unique = df['lhs'].drop_duplicates().to_numpy()
right_array_unique = df['rhs'].drop_duplicates().to_numpy()
relationship_array_unique = df['relationship'].drop_duplicates().to_numpy()
print(df['lhs'].drop_duplicates().to_numpy())

# approach => construct a matrix where each row represents the vector representation of fields
X = None

try:
    with open("data.pickle", "rb") as infile:
        X = pickle.load(infile)
except Exception as e:
    print("serialized data cannot be loaded, create new representations")
    matrix = []
    for lhs in left_array_unique:
        matrix.append([])
        curr_idx = len(matrix) - 1
        for relationship in relationship_array_unique:
            matrix[curr_idx].append([0 for x in range(len(right_array_unique))])
            for data in df[(df.lhs == lhs) & (df.relationship == relationship)]['rhs'].to_numpy():
                matrix[curr_idx][np.where(relationship_array_unique == relationship)[0][0]][
                    np.where(right_array_unique == data)[0][0]] = 1
    data_set = np.array(matrix)
    nsamples, nx, ny = data_set.shape
    X = data_set.reshape((nsamples, nx * ny))
    with open("data.pickle", "wb") as outfile:
        pickle.dump(X, outfile)

clustering = AgglomerativeClustering(n_clusters=50) #affinity='cosine', linkage='complete')

clustering_fit_res = clustering.fit_predict(X)

clustering_result = dict()
for i in range(0, len(clustering_fit_res)):
    clustering_result[i] = []

id = 0
for label in clustering_fit_res:
    clustering_result[label].append(left_array_unique[id])
    id += 1

for i in np.unique(np.array(clustering_fit_res)):
    print(clustering_result[i])
