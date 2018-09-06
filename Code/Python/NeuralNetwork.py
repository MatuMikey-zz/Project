import random as random
import csv
from datetime import datetime
random.seed(datetime.now())

def normalise(time, s1,s2,s3):
    smallest1 = 10000
    smallest2 = 10000
    smallest3 = 10000
    biggest1 = 0
    biggest2 = 0
    biggest3 = 0
    for i in range(0, len(time)):
        time[i] = time[i]/86400.0
        if (smallest1 > s1[i]):
            smallest1 = s1[i]
        if (biggest1 < s1[i]):
            biggest1 = s1[i]
        if (smallest2 > s2[i]):
            smallest2 = s2[i]
        if (biggest2 < s2[i]):
            biggest2 = s2[i]
        if (smallest3 > s3[i]):
            smallest3 = s3[i]
        if (biggest3 < s3[i]):
            biggest3 = s3[i]
    for i in range(0, len(s1)):
        s1[i] = (s1[i] - smallest1)/(biggest1-smallest1)
        s2[i] = (s2[i] - smallest2)/(biggest2-smallest2)
        s3[i] = (s3[i] - smallest3)/(biggest3-smallest3)

class NeuralNetwork:
    inputNodes = 3 #time, sensor 1, sensor 2
    hiddenLayers = 0 #hidden layer per neural network
    hiddenNodes = 0 #hidden nodes per layer
    outputNode = 1
    
    
    def __init__(self, hiddenNodes, hiddenLayers):
        self.weights = []
        self.hiddenNodes = hiddenNodes+1
        self.hiddenLayers = hiddenLayers
        #Connect the weights for the input layer to the hidden layer EXCEPT bias node
        for i in range(0, self.inputNodes):
            for j in range(0, self.hiddenNodes-1):
                self.weights.append(random.uniform(-1.0,1.0))
        #Connect weights for each hidden layer to the next hidden layer
        #If the hidden layer is the last layer before the output, only make 1 weight per output
        for i in range(0, self.hiddenLayers):
            if (self.hiddenLayers == 1 or i == self.hiddenLayers-1): #If only one hidden layer or the last hidden layer, connect only to the output
                for j in range (0, self.hiddenNodes):
                    self.weights.append(random.uniform(-1.0,1.0))
            else:
                for j in range(0, self.hiddenNodes): 
                    for k in range(0, self.hiddenNodes-1): #connect to all nodes except the bias node
                        self.weights.append(random.uniform(-1.0,1.0))
                        
    def printWeights(self): #print the weights for each node
        inputNodeWeights = []
        hiddenNodeWeights = []
        temp = []
        weightCounter = 0
        for i in range(0, self.inputNodes):
            temp = []
            for j in range(0, self.hiddenNodes-1):
                temp.append(self.weights[weightCounter])
                weightCounter = weightCounter+1
            inputNodeWeights.append(temp)
        print("Input Layer")
        for i in range(0, len(inputNodeWeights)):
            print("\tInput Node:", i+1, inputNodeWeights[i])
        if self.hiddenLayers == 1: #If only one hidden layer
            temp = []
            for i in range(0, self.hiddenNodes):
                temp.append(self.weights[weightCounter])
                hiddenNodeWeights.append(temp)
                weightCounter = weightCounter+1
                temp = []
            print("Hidden Layer")
            for i in range(0, len(hiddenNodeWeights)):
                if i == self.hiddenNodes-1:
                    print("Bias Node:", hiddenNodeWeights[i])
                else:
                    print("\tHidden Node:", i+1, hiddenNodeWeights[i])
        else:                       #If multiple hidden layers
            temp = []
            k = 0
            for i in range(0,self.hiddenLayers):
                if i == self.hiddenLayers-1: #Last hidden layer
                    temp = []
                    for j in range(0, self.hiddenNodes):
                        temp.append(self.weights[weightCounter])
                        hiddenNodeWeights.append(temp)
                        weightCounter = weightCounter+1
                        temp = []
                else:
                    for j in range(0, self.hiddenNodes): #for every node in the hidden layer
                        temp = []
                        for j in range(0, self.hiddenNodes-1): #only connect to the hidden nodes, not the bias nodes
                            temp.append(self.weights[weightCounter])
                            weightCounter = weightCounter+1
                        hiddenNodeWeights.append(temp)
            for i in range(0, self.hiddenLayers): #for every hidden layer
                print("Hidden Layer:", i+1)
                for j in range(0, self.hiddenNodes): #for every node in a layer
                    if j == self.hiddenNodes-1:
                        print("\tBias Node:", hiddenNodeWeights[k+j])
                    else:
                        print("\tHidden Node:", j+1, hiddenNodeWeights[k+j] )
                k = k+self.hiddenNodes

    def predict(self, inputs):
        output = 0
        outputs = []
        weightCounter = 0
        for i in range(0, self.hiddenNodes-1): #For every input node that needs to go to a hidden layer
            for j in range(0, self.inputNodes): #for every weight of an input node
                output = output + inputs[j]*self.weights[weightCounter]
                weightCounter = weightCounter+1
            outputs.append(output)
        for j in range(0, self.hiddenLayers): #for every hidden layer
            if self.hiddenLayers == 1: #If only 1 hidden layer
                inputs = []
                output = 0
                for i in range(0, len(outputs)):
                    inputs.append(outputs[i]/(1.0+abs(outputs[i]))) #use the optimised sigmoid function x/(1+|x|)
                outputs = []
                for i in range(0, self.hiddenNodes): #for every hidden node in the hidden layer to the output layer
                    if i == self.hiddenNodes-1: #If calculating the bias node
                        output = output + 1.0*self.weights[weightCounter]
                        weightCounter = weightCounter+1
                    else:
                        output = output + inputs[i]*self.weights[weightCounter]
                        weightCounter = weightCounter+1
                    outputs.append(output)
                    #calculate the output node
                output = 0
                for i in range(0, len(outputs)):
                    output = output + outputs[i]
                output = output/(1+abs(output))
            else:
                inputs = []
                output = 0
                for i in range (0, len(outputs)):
                    inputs.append(outputs[i]/(1.0+abs(outputs[i])))
                outputs = []
                for i in range(0, self.hiddenNodes): #For every hidden node layer to the next hidden layer
                    if i == self.hiddenNodes-1: #If calculating the bias node
                        output = output + 1.0*self.weights[weightCounter]
                        weightCounter = weightCounter+1
                    else:
                        output = output + inputs[i]*self.weights[weightCounter]
                        weightCounter = weightCounter + 1
                    outputs.append(output)
        output = 0
        for i in range(0, len(outputs)):
            output = output+outputs[i]
        return output/len(outputs)
                        
def train(nodes, layers, n_neuralnets, epochs, sensorNumber):
    #nodes = number of hidden nodes in hidden layer
    #layers = number of hidden layers
    #n_neuralnets = number neuralnets in the initial population
    #epochs = number of training runs
    #sensorNumber = which sensor to train
    time = []
    sensor1 = []
    sensor2 = []
    sensor3 = []
    with open('TemperatureData.csv', 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=';', quotechar='"')
        data = list(data)
    for i in range(1, len(data)):
        for j in range(0, len(data[i])):
            data[i][j] = float(data[i][j])
        time.append(data[i][1])
        sensor1.append(data[i][2])
        sensor2.append(data[i][3])
        sensor3.append(data[i][4])
    normalise(time, sensor1, sensor2, sensor3)
    
    trainingErrors = []
    testErrors = []
    neuralnets = []
    for i in range(0, n_neuralnets):
        neuralnets.append(NeuralNetwork(nodes, layers))   
        trainingErrors.append(0)
        testErrors.append(0)
    trainingSet= []
    testSet = []
    trainingTargets = []
    testTargets = []

    if sensorNumber == 0: #train a sensor for node 1
        for i in range(0, len(sensor1)):
            if random.randint(1,100) <= 60:
                trainingSet.append([sensor2[i], sensor3[i], time[i]])
                trainingTargets.append(sensor1[i])
            else:
                testSet.append([sensor2[i], sensor3[i], time[i]])
                testTargets.append(sensor1[i])
    elif sensorNumber == 1: #train a sensor for node 2
        for i in range(0, len(sensor1)):
            if random.randint(1,100) <= 60:
                trainingSet.append([sensor1[i], sensor3[i], time[i]])
                trainingTargets.append(sensor2[i])
            else: #train a sensor for node 3
                testSet.append([sensor1[i], sensor3[i], time[i]])
                testTargets.append(sensor2[i])
    elif sensorNumber == 2:
        for i in range(0, len(sensor1)):
            if random.randint(1,100) <= 60:
                trainingSet.append([sensor1[i], sensor2[i], time[i]])
                trainingTargets.append(sensor3[i])
            else:
                testSet.append([sensor1[i], sensor2[i], time[i]])
                testTargets.append(sensor3[i])
    
    for i in range(0, epochs):# for every epoch
        fitPopulation = []
        for j in range(0, len(neuralnets)): #for every neural net in the population
            for k in range(0, len(trainingSet)): #for every data point in the training set
                output = neuralnets[j].predict(trainingSet[k])
                trainingErrors[j] = trainingErrors[j] + abs(trainingTargets[k] - output)
            trainingErrors[j] = trainingErrors[j]/len(trainingTargets)
        
        for j in range(0, int(len(neuralnets)/10)): #for 10% of the population
            smallest = 1.01
            smallestPosition = 0
            for j in range(0, len(neuralnets)): #check every neural net
                if (smallest > trainingErrors[j]):
                    smallest = trainingErrors[j]
                    smallestPosition = j
            fitPopulation.append(neuralnets.pop(smallestPosition))
        print(fitPopulation)
nn = NeuralNetwork(3,1)
mm = NeuralNetwork(3,1)

train(3,2,20,1, 0)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
