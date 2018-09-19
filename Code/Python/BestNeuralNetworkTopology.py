from NeuralNetwork import *
import csv
import matplotlib.pyplot as plt


best0 = 0
best1 = 0
best2 = 0
bestArray0 = []
bestArray1 = []
bestArray2 = []
nodes = []
for j in range(3, 12+1): #train for 3 to 15 hidden nodes
    print("Number of hidden nodes:", j)
    best0 = 0.0
    best1 = 0.0
    best2 = 0.0
    for i in range(0, 20): #train 100 times
        print("\nNumber of repetitions so far:", i)
        best, t1, t2 = train(j, 1, 100, 10, 0)
        best0 = best0 + best[1]
        best, t1, t2 = train(j,1,100,10,1)
        best1 = best1 + best[1]
        best, t1, t2 = train(j,1,100,10,2)
        best2 = best2 + best[1]
    bestArray0.append(best0/20)
    bestArray1.append(best1/20)
    bestArray2.append(best2/20)
    nodes.append(j)
plt.xlabel("Hidden nodes")
plt.ylabel("Loss")
plt.title("Loss against number of hidden nodes")
plt.figure(10)
plt.plot(nodes,bestArray0)
plt.figure(11)
plt.plot(nodes,bestArray1)
plt.figure(12)
plt.plot(bestArray2)