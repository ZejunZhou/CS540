import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file = sys.argv[1]
data = pd.read_csv(file)
datax = list(data["year"])
datay = data["days"].astype(int)

plt.plot(datax, datay)
plt.ylabel("Number of frozen days")
plt.xlabel("Year")
plt.xticks(np.arange(list(data["year"])[0], list(data["year"])[-1] + 1, step = 15))
plt.savefig("plot.png")


list_x = list(data["year"])
list_list_x = []
for i in list_x:
    item = [1, i]
    list_list_x.append(np.array(item).transpose())
array_x = np.array(list_list_x)
print("Q3a:")
print(array_x)


list_y = list(int(i) for i in data["days"])
an_array_y = np.array(list_y)
print("Q3b:")
print(an_array_y)

print("Q3c:")
print(np.dot(array_x.transpose(), array_x))

print("Q3d:")
print(np.linalg.inv(np.dot(array_x.transpose(), array_x)))

inverse_xt_x = np.linalg.inv(np.dot(array_x.transpose(), array_x))
print("Q3e:")
print(np.dot(inverse_xt_x, array_x.transpose()))


inverse_xt_x_xt = np.dot(inverse_xt_x, array_x.transpose())
print("Q3f:")
print(np.dot(inverse_xt_x_xt, an_array_y))

beta = np.dot(inverse_xt_x_xt, an_array_y)
x_test = 2021
beta0 = beta[0]
beta1 = beta[1]
y_test = beta0 + beta1 * 2021
print("Q4:" + str(y_test))

#q5 a
if beta1 == 0:
    print("Q5a: " + "=")
elif beta1 > 0:
    print("Q5a: " + ">")
else:
    print("Q5a: " + "<")
    
#q5 b
print("Q5b: " + "Because the beta1 is negative, the slope of the regression model is descending, it means that as the years increases, the number of frozen days of Mendota ice is decreasing")

#q6
x_star = (0 - beta0) / beta1
print("Q6a:" + str(x_star))

#q6
print("Q6b: " + "It makes sense because we have find our slope descending, which as year inceease, the number of ice days decrease. It should eventually reach to 0 days based on our regression model prediction around year 2456 based on the algebra computation")