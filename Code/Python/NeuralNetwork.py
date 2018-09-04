import random as random

class inputNode:
    input = 0
    weights = []
    def __init__(self, numberOfConnectedNodes):
        for i in range(0, numberOfConnectedNodes+1):
            self.weights.append(random.uniform(-1.0,1.0))
        
            
class HiddenNode:
    input = 0
    weights = []
    def __init__(self, numberOfConnectedNodes):
        for i in range(0, numberOfConnectedNodes+1):
            self.weights.append(random.uniform(-1.0,1.0))

class BiasNode:
    input = 1
    weights = []
    def __init__(self, numberOfConnectedNodes):
        for i in range(0, numberOfConnectedNodes+1):
            self.weights.append(random.uniform(-1.0,1.0))
        
class OutputNode:
    input = 0
    output = 0
    def __init__(self):
        self.input = 0
        self.output = 0
            
class NeuralNetwork:
    inputLayer = []
    hiddenLayers =[]
    outputLayer = 0
    def __init__(self, hiddenNodes, hiddenLayers):
        for i in range(0,3): #create 3 input nodes
            self.inputLayer.append(inputNode(hiddenNodes+1)) #hidden nodes + 1 bias node
        for i in range(0,hiddenLayers):
            hiddenLayer = []
            for j in range(0, hiddenNodes):
                hiddenLayer.append(HiddenNode(hiddenNodes))
            hiddenLayer.append(BiasNode(hiddenNodes))
            self.hiddenLayers.append(hiddenLayer)
        