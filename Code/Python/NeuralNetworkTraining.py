from NeuralNetwork import *
import matplotlib.pyplot as plt

Sensor0NeuralNetwork, trainLoss0, testLoss0 = train(11,1,100,1000,0)
#print ("Sensor0 Test Loss:", testLoss0, "Train Loss:", trainLoss0)
Sensor1NeuralNetwork, trainLoss1, testLoss1 = train(11,1,100,1000,1)
#print ("Sensor1 Test Loss:", testLoss1, "Train Loss:", trainLoss1)
Sensor2NeuralNetwork, trainLoss2, testLoss2 = train(11,1,100,1000,2)
#print ("Sensor2 Test Loss:", testLoss2, "Train Loss:", trainLoss2)

print("Weights:")
print("Sensor0 ", Sensor0NeuralNetwork[0].weights)
print("Sensor1 ", Sensor1NeuralNetwork[0].weights)
print("Sensor2 ", Sensor2NeuralNetwork[0].weights)

for i in range(0, len(trainLoss0)):
    trainLoss0[i] = trainLoss0[i]*100.0
for i in range(0, len(testLoss0)):
    testLoss0[i] = testLoss0[i]*100.0

for i in range(0, len(trainLoss1)):
    trainLoss1[i] = trainLoss1[i]*100.0
for i in range(0, len(testLoss1)):
    testLoss1[i] = testLoss1[i]*100.0

for i in range(0, len(trainLoss2)):
    trainLoss2[i] = trainLoss2[i]*100.0
for i in range(0, len(testLoss2)):
    testLoss2[i] = testLoss2[i]*100.0




plt.figure(0)
plt.title("Training Loss Over 500 Training Epochs for Sensor 1")
plt.ylabel("Loss as percentage")
plt.xlabel("Epochs")
plt.plot(trainLoss0)
plt.figure(1)
plt.title("Test Loss Over 500 Training Epochs for Sensor 1")
plt.ylabel("Loss as percentage")
plt.xlabel("Epochs")
plt.plot(testLoss0)

plt.figure(2)
plt.title("Training Loss Over 500 Training Epochs for Sensor 2")
plt.ylabel("Loss as percentage")
plt.xlabel("Epochs")
plt.plot(trainLoss1)
plt.figure(3)
plt.title("Test Loss Over 500 Training Epochs for Sensor 2")
plt.ylabel("Loss as percentage")
plt.xlabel("Epochs")
plt.plot(testLoss1)

plt.figure(4)
plt.title("Training Loss Over 500 Training Epochs for Sensor 3")
plt.ylabel("Loss as percentage")
plt.xlabel("Epochs")
plt.plot(trainLoss2)
plt.figure(5)
plt.title("Test Loss Over 500 Training Epochs for Sensor 3")
plt.ylabel("Loss as percentage")
plt.xlabel("Epochs")
plt.plot(testLoss2)
