import matplotlib.pyplot as plt

xList = [ x for x in range(-5,6)]
yList = [y*y for y in range(-5,6)]
# plt.plot(xList, yList)

plt.scatter(xList,yList,color='g')