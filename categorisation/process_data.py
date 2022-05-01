import pandas as pd
import numpy as np
import pickle
from os.path import exists
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import re

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

clustering = AgglomerativeClustering(n_clusters=50, compute_distances=True)  # , affinity='cosine', linkage='complete')

clustering_fit_res = clustering.fit(X)

print("clustering res", clustering_fit_res.labels_)

clustering_result = dict()
for i in range(0, len(clustering_fit_res.labels_)):
    clustering_result[i] = []

id = 0
for label in clustering_fit_res.labels_:
    clustering_result[label].append(left_array_unique[id])
    id += 1

id = 0
for i in np.unique(np.array(clustering_fit_res.labels_)):
    print(str(id) + " :" + str(clustering_result[i]))
    id += 1


def plot_dendrogram(model, **kwargs):
    count = np.zeros(model.children_.shape[0])
    nsamples = len(model.labels_)

    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < nsamples:
                current_count += 1
            else:
                current_count += count[child_idx - nsamples]
        count[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, count]
    ).astype(float)

    return dendrogram(linkage_matrix, **kwargs)


dend = plot_dendrogram(clustering_fit_res, truncate_mode="level", show_contracted=True, p=4)
labels = []

ivl = dend['ivl']

i = 0
labId = 0

clustering_labels = clustering_fit_res.labels_

# build labels
while i < len(ivl):
    try:
        a = str(int(ivl[i]))
        labels.append(str(clustering_labels[labId]))
        labId += 1
        i += 1
    except Exception as e:
        string = ""
        for j in range(int(re.search(r'\((.*?)\)', ivl[i]).group(1))):
            if labId < len(clustering_labels):
                string += str(clustering_labels[labId]) + " "
            labId += 1
        labels.append(string)
        i += 1

plt.figure(figsize=(30, 15), dpi=144)
plt.title("Hierarchical Clustering Dendrogram")
plot_dendrogram(clustering_fit_res, truncate_mode="level", show_contracted=True, p=4)

plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()

print("labels corresponding with the dendrogram plot: ", labels)

# 2d,is-a,field
# 2d,is-used-in-field,graphics
# 3d,is-a,field
# 3d,is-used-in-field,graphics

# 2d
# (is-a) 0 0 1 0 0 0 0 0 0
#
