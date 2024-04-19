import numpy as np
from sklearn.linear_model import LinearRegression

x1 = np.array([])
x2 = np.array([])
y1 = np.array([])
y2 = np.array([])

file = open('data.txt', 'r')

for f in file:
    a,b,c,d = map(float, f.split(","))
    x1 = np.append(x1, a)
    x2 = np.append(x2, b)
    y1 = np.append(y1, c)
    y2 = np.append(y2, d)

file.close()

X = np.column_stack((x1, x2))

model_y1 = LinearRegression().fit(X, y1)
w11, w12 = model_y1.coef_
b1 = model_y1.intercept_

model_y2 = LinearRegression().fit(X, y2)
w21, w22 = model_y2.coef_
b2 = model_y2.intercept_

print(w11, w12, b1, w21, w22, b2)