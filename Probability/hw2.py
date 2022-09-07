import sys
import math
import string
import pandas as pd
def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    f = open(filename,'r')
    data = f.read()
    f.close()
    X = dict()
    X = dict.fromkeys(string.ascii_uppercase, 0)
    for i in data:
        each_char = i.upper()
        if each_char in X:
            X[each_char] = X[each_char] + 1
    return X

# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!
#Q1
count_result_dic = shred("letter.txt")
result_string = "Q1" + "\n"
for item in count_result_dic:
    result_string = result_string + item + " " + str(count_result_dic[item]) + "\n"
result_string = result_string.strip()
result_string
print(result_string)
#for item in count_result_dic 

#Q2
pY_English = 0.6
pY_Spanish = 0.4
x1 = count_result_dic["A"]
vector_english = get_parameter_vectors()[0]
vector_spanish =  get_parameter_vectors()[1]
print("Q2")
log_english = (round(math.log(vector_english[0]) * x1, 4))
print("{:.4f}".format(log_english,4))
log_spanish = (round(math.log(vector_spanish[0]) * x1, 4))
print("{:.4f}".format(log_spanish,4))

#Q3
#vector_English_and_Spanish = list(pd.Series(vector_english) + pd.Series(vector_spanish))
print("Q3")
english_result = 0
list_result = []
for i in count_result_dic:
    list_result.append(count_result_dic[i])
for i in range(26):
    english_result = english_result + math.log(vector_english[i]) * list_result[i]
F_English = round(english_result + math.log(pY_English), 4)
print("{:.4f}".format(F_English,4))
spanish_result = 0
for i in count_result_dic:
    list_result.append(count_result_dic[i])
for i in range(26):
    spanish_result = spanish_result + math.log(vector_spanish[i]) * list_result[i]
F_Spanish = round(spanish_result + math.log(pY_Spanish), 4)
print("{:.4f}".format(F_Spanish,4))

#Q4
print("Q4")
P_Y_English_X = 0
if (F_Spanish - F_English >= 100):
    P_Y_English_X = 0
if (F_Spanish - F_English <= -100):
    P_Y_English_X = 1
else:
    P_Y_English_X = 1 / (1 + math.e ** (F_Spanish - F_English))
P_Y_English_X = round(P_Y_English_X, 4)
print("{:.4f}".format(P_Y_English_X,4))