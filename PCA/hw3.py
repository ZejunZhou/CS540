from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

#5.1
def load_and_center_dataset(filename):
    data = np.load(filename)
    data = data.astype(float)
    data = data - np.mean(data, axis=0)
    return data
#5.2
def get_covariance(dataset):
    data_t = np.transpose(dataset)
    return np.dot(data_t, dataset / (len(dataset) - 1))
#5.3
def multi_return (S, m): 
    eigh_value, eigh_vector = eigh(S, subset_by_index = [len(S)- m, len(S)-1])
    return eigh_value, eigh_vector

def get_eig(S, m):
    eigh_value, eigh_vector = multi_return(S, m)
    reverse_order = np.flip(np.argsort(eigh_value))  
    return np.diag(eigh_value[reverse_order]), eigh_vector[:,reverse_order]
#5.4
def get_eig_prop(S, prop):
    eigh_value, eigh_vector = eigh(S)
    percent = np.sum(eigh_value) * prop
    percent_eigh_value, percent_eigh_vector = eigh(S, subset_by_value=[percent, np.inf])
    i = np.flip(np.argsort(percent_eigh_value))
    return np.diag(percent_eigh_value[i]), percent_eigh_vector[:, i]
#5.5
def project_image(image, U):
    aijs = np.dot(np.transpose(U), image)
    return np.dot(U, aijs)
#5.6
def display_image(orig, proj):
    orig = np.reshape(orig, (32,32))
    proj = np.reshape(proj, (32,32))
    orig = np.transpose(orig)
    proj = np.transpose(proj)
    figure, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2)
    ax1.set_title('Original')
    ax2.set_title('Projection')
    
    ax1Map = ax1.imshow(orig, aspect = 'equal')
    figure.colorbar(ax1Map, ax = ax1)
    ax2Map = ax2.imshow(proj, aspect = 'equal')
    figure.colorbar(ax2Map, ax = ax2)
