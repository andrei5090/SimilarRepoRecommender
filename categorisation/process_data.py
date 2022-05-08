import pandas as pd
import numpy as np
import pickle
from os.path import exists
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, cut_tree
from sklearn.decomposition import PCA
import re

from sklearn.cluster import AgglomerativeClustering, KMeans

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

# VARIABLES
NO_CLUSTERS = 50
DEND_LVL = 10

clustering = AgglomerativeClustering(n_clusters=NO_CLUSTERS,
                                     compute_distances=True)  # , affinity='cosine', linkage='complete')

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


dend = plot_dendrogram(clustering_fit_res, truncate_mode="level", show_contracted=True, p=DEND_LVL, count_sort=False,
                       get_leaves=True, no_plot=True)
labels = []

ivl = dend['ivl']

i = 0
labId = 0

clustering_labels = clustering_fit_res.labels_

# build labels
while i < len(ivl):
    try:
        a = str(int(ivl[i]))
        labels.append(a)
        labId += 1
        i += 1
    except Exception as e:
        # print("exception", e)
        string = ""
        for j in range(int(re.search(r'\((.*?)\)', ivl[i]).group(1))):
            if labId < len(clustering_labels):
                string += str(clustering_labels[labId]) + " "
            labId += 1
        labels.append(string)
        i += 1

# df_clst = pd.DataFrame()
# df_clst['index']  = range(0, len(clustering_labels))
# print("leaves ", dend['leaves'])
# df_clst['label']  = dend['leaves']
#
#
#
# for i in range(50):
#    elements = df_clst[df_clst['label']==i+1]['index'].tolist()
#    size = len(elements)
#    print('\n Cluster {}: N = {}  {}'.format(i+1, size, elements))

plt.figure(figsize=(120, 15), dpi=72)
plt.title("Hierarchical Clustering Dendrogram")
plot_dendrogram(clustering_fit_res, truncate_mode="level", show_contracted=True, p=DEND_LVL, count_sort=False,
                get_leaves=True, labels=left_array_unique)

plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()

print("labels corresponding with the dendrogram plot: ", labels)


def plot_clusters(n_clusters, data):
    reduced_data = PCA(n_components=2).fit_transform(data)
    kmeans = KMeans(init="k-means++", n_clusters=n_clusters, n_init=4)

    # kmeans = SpectralClustering(n_clusters = 50, affinity="precomputed")
    kmeans.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = 0.02  # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(
        Z,
        interpolation="nearest",
        extent=(xx.min(), xx.max(), yy.min(), yy.max()),
        cmap=plt.cm.Paired,
        aspect="auto",
        origin="lower",
    )

    plt.plot(reduced_data[:, 0], reduced_data[:, 1], "k.", markersize=2)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(
        centroids[:, 0],
        centroids[:, 1],
        marker="x",
        s=169,
        linewidths=3,
        color="w",
        zorder=10,
    )
    plt.title(
        "K-means clustering on the digits dataset (PCA-reduced data)\n"
        "Centroids are marked with white cross"
    )
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()


plot_clusters(50, X)

from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

# second version using just scipy
Z = linkage(X, method='ward')
label = fcluster(Z, NO_CLUSTERS, criterion='maxclust')
print("linkage ", Z)

df_clst = pd.DataFrame()
df_clst['index'] = left_array_unique
df_clst['label'] = label

dendogram_lvls = [len(left_array_unique), 500, 400, 300, 200, 100, 80, 70, 65, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10,
                  5, 4, 3, 2, 1]

# create result folder
import os

WRITE = False
res_dict = dict()

if WRITE:
    os.mkdir('results')
    os.path.join('results')

for lvl in dendogram_lvls:
    DEND_LVL = lvl

    currPath = ''
    if WRITE:
        currPath = 'cuts_at_level_' + str(lvl)
        os.mkdir('results/' + currPath)
        plt.figure(figsize=(120, 15), dpi=72)
        plt.title("Hierarchy Dendrogram level " + str(DEND_LVL))

    dend_res = dendrogram(
        Z,
        truncate_mode='lastp',  # show only the last p merged clusters
        p=DEND_LVL,
        show_leaf_counts=True,  # otherwise numbers in brackets are counts
        leaf_rotation=90.,
        leaf_font_size=12.,
        show_contracted=True,  # to get a distribution impression in truncated branches
        labels=left_array_unique,
        distance_sort=True,
        no_plot=not WRITE
    )
    if WRITE:
        plt.savefig('results/' + currPath + '/cuts_at_level_' + str(lvl) + '_dendrogram.png')
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()

    for i in range(NO_CLUSTERS):
        elements = df_clst[df_clst['label'] == i + 1]['index'].tolist()
        size = len(elements)
        print('\n Cluster {}: N = {}  {}'.format(i + 1, size, elements))

    print("NO Of Clusters in dendogram ", len(dend_res['leaves']))

    N_CLUSTERS_CUT = [DEND_LVL]
    clusters = cut_tree(Z, n_clusters=N_CLUSTERS_CUT)
    # print("clusters : cut", clusters)
    # insert column for the case, where every element is its own cluster
    # clusters = np.insert(clusters, clusters.shape[1], range(clusters.shape[0]), axis=1)
    # transpose matrix
    clusters = clusters.T
    # print(clusters)
    id = 0
    df_final = dict()
    for row in clusters[::-1]:
        groups = {}
        for i, g in enumerate(row):
            if g not in groups:
                groups[g] = set([])
            groups[g].add(i)
        res = []
        df_final['lvl' + str(DEND_LVL)] = list(groups.values())
        id += 1

    print(df_final)

    df_final_res = dict()

    for val in df_final.keys():
        res = []
        for i in df_final[val]:
            mat = []
            for p in i:
                mat.append(left_array_unique[p])
            res.append(mat)

        df_final_res[val] = res

    res_dict[DEND_LVL] = df_final_res

    cut_id = 0
    if WRITE:
        with open('results/' + currPath + "/clusters.txt", 'w') as f:
            for i in df_final_res.keys():
                f.write("Number of clusters at this level " + str(len(df_final_res[i])) + "\n")
                for j in df_final_res[i]:
                    f.write("SIZE = " + str(len(j)) + "  [")
                    p = 0
                    for el in j:
                        f.write(el)
                        if p < len(j) - 1:
                            f.write(", ")
                        p += 1
                    f.write("]")
                    f.write(" \n")
                f.write("\n")
                cut_id += 1


# print("DICT OUTPUT: ", res_dict)
# print("DICT KEYS: ", res_dict.keys())
# print("DICT VAL 3 ", res_dict[3])
# print("DICT VAL 3 VALUES ", res_dict[3]['lvl3'])


# check if two clusters are equal
def isEqual(a, b):
    lenght = 0
    for i in a:
        if i in b:
            lenght += 1
    return len(b) == lenght


def isPartOf(a, b, merged_into):
    curr_len = len(merged_into)
    if len(a) == 0 or len(b) == 0:
        return False

    for i in a:
        if i in b:
            merged_into.add(i)

    if curr_len < len(merged_into):
        return True
    else:
        return False


# display the merge
print("\n\n\n")


def getId(el):
    return np.where(left_array_unique == el)[0][0]


tree = dict()

with open("mergeInfo.txt", 'w') as f:
    for lvl in range(len(dendogram_lvls) - 1):
        merged_into = set()
        first_clusters = res_dict[dendogram_lvls[lvl]]['lvl' + str(dendogram_lvls[lvl])]
        second_clusters = res_dict[dendogram_lvls[lvl + 1]]['lvl' + str(dendogram_lvls[lvl + 1])]
        # print("LVL {0} MERGED IN {1}".format(str(dendogram_lvls[lvl]), str(dendogram_lvls[lvl + 1])))
        f.write("\n \n \n")
        f.write("LVL {0} MERGED IN {1}".format(str(dendogram_lvls[lvl]), str(dendogram_lvls[lvl + 1])))
        f.write("\n")

        for i in range(0, len(first_clusters)):
            for j in range(0, len(second_clusters)):
                merged_init_size = len(merged_into)
                if isEqual(first_clusters[i], second_clusters[j]):
                    # print("equal {} \n {}".format(first_clusters[i], second_clusters[j]))
                    continue
                elif isPartOf(first_clusters[i], second_clusters[j], merged_into):
                    # print("Cluster {0} with size {1} was merged in cluster {2} with size {3}".format(first_clusters[i], len(first_clusters[i]), second_clusters[j], len(second_clusters[j])))
                    if merged_init_size < len(merged_into):
                        f.write(
                            "Cluster (id: {0}) {1} with size {2} was merged in \nCluster (id :{3}) {4} with size {5}".format(
                                i, first_clusters[i], len(first_clusters[i]), j, second_clusters[j],
                                len(second_clusters[j])))
                    f.write("\n\n")
        f.write("\n \n \n")

import json


class Cluster:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.content = []

    def __hash__(self):
        return self.value

    class ComplexEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Cluster):
                return obj.__dict__
            return json.JSONEncoder.default(self, obj)

    def __str__(self):
        # return "\n NAME: {0} \n" \
        #        "CHILDREN (SIZE = {1}) = {2} \n" \
        #        "CONTENT (SIZE = {3}) = {4} \n".format(self.name, len(self.children), self.children, len(self.content),
        #                                               self.content)

        return json.dumps(self, cls=self.ComplexEncoder)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def getFatherId(el, cluster):
        id = 0
        for i in cluster:
            if el in i:
                return id
            id += 1
        return -1

    @staticmethod
    def getName(lvl, id, length):
        return "lvl " + str(dendogram_lvls[lvl]) + "  " + str(id) + " size: " + str(length)

    def containsTag(self, tag):
        for i in self.content:
            for j in i:
                if tag in j:
                    return True

        return False

    def isParent(self, subCluster):
        if subCluster[0] in self.content:
            return True
        return False


root = Cluster("root")

lvl = len(dendogram_lvls) - 1
big_clusters = res_dict[dendogram_lvls[lvl]]['lvl' + str(dendogram_lvls[lvl])]
root.content = big_clusters[0]

print(len(root.content))


def buildTree(root: Cluster, lvl):
    if lvl < 20:
        return

    small_clusters = res_dict[dendogram_lvls[lvl - 1]]['lvl' + str(dendogram_lvls[lvl - 1])]

    id = 0
    for i in small_clusters:
        currCluster = Cluster(Cluster.getName(lvl, id))
        currCluster.content = i
        currCluster.value = Cluster.getName(lvl, id, len(i))

        if root.isParent(i):
            root.children.append(currCluster)

    for ch in root.children:
        buildTree(ch, lvl - 1)


buildTree(root, lvl)

with open("clusters.json", 'w') as f:
    f.write(root.__str__())
    f.close()

# make json file


# 2d,is-a,field
# 2d,is-used-in-field,graphics
# 3d,is-a,field
# 3d,is-used-in-field,graphics

# 2d
# (is-a) 0 0 1 0 0 0 0 0 0
#
