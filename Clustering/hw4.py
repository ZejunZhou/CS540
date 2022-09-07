import csv
import numpy
def load_data(filepath):
    list_data = []
    with open(filepath, mode = 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            list_data.append(row)
        return list_data
    
def calc_features(row):
    x_1 = row["Attack"]
    x_2 = row["Sp. Atk"]
    x_3 = row["Speed"]
    x_4 = row["Defense"]
    x_5 = row["Sp. Def"]
    x_6 = row["HP"]
    return numpy.array((x_1, x_2, x_3, x_4, x_5, x_6), dtype = numpy.int64)

def count_distance(cluster_1, cluster_2):
    result = -1
    for p1 in cluster_1:
        for p2 in cluster_2:
            dis = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2 + (p1[3]-p2[3])**2 + (p1[4]-p2[4])**2 + (p1[5]-p2[5])**2)**0.5
            if dis > result:
                result = dis
    return result

def count_distance(cluster_1, cluster_2):
    result = -9999
    for p1 in cluster_1:
        for p2 in cluster_2:
            distance = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2 + (p1[3]-p2[3])**2 + (p1[4]-p2[4])**2 + (p1[5]-p2[5])**2)**0.5
            if distance > result:
                result = distance
    return result

def hac(features):
    n = len(features)
    list_z = []
    cluster_list = []
    new_merge_index = len(features) - 1
    
    for trace_index in range(len(features)):
        cluster_list.append([[features[trace_index]], trace_index])
        
    while len(cluster_list) > 1:
        cluster_1 = []
        cluster_2 = []
        trace_index_1 = 0
        trace_index_2 = 0
        min_distance = 999999;
        for i in range(len(cluster_list)):
            for j in range(i+1,len(cluster_list)):  
                distance = count_distance(cluster_list[i][0], cluster_list[j][0])
                
                
                if distance < min_distance:
                    min_distance = distance
                    cluster_1 = cluster_list[i][0]
                    cluster_2 = cluster_list[j][0]
                    trace_index_1 = cluster_list[i][1]
                    trace_index_2 = cluster_list[j][1]
                        
        merge = []    
        for i in range(len(cluster_1)):
            merge.append(cluster_1[i])
        for i in range(len(cluster_2)):
            merge.append(cluster_2[i])
        new_merge_index = new_merge_index + 1
        cluster_list.append([merge, new_merge_index])
        list_z.append([trace_index_1,trace_index_2, min_distance, len(merge)])
        for i in range(len(cluster_list)):
            if cluster_list[i][1] == trace_index_1:
                cluster_list.pop(i)
                break
                
        for i in range(len(cluster_list)):
            if cluster_list[i][1] == trace_index_2:
                cluster_list.pop(i)
                break
    return numpy.array(list_z).reshape(n-1, 4)

from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
def imshow_hac(Z):
    dn = dendrogram(z)
    plt.show()