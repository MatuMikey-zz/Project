import random as random

class NeuralNetwork:
    inputNodes = 3 #time, sensor 1, sensor 2
    hiddenLayers = 0 #hidden layer per neural network
    hiddenNodes = 0 #hidden nodes per layer
    outputNode = 1
    weights = []
    
    def __init__(self, hiddenNodes, hiddenLayers):
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
        inputNodesCounter = 0
        inputNodeCounter = 0
        inputNodeWeight= []
        inputNodeWeights = []
        hiddenNodeCounter = 0
        hiddenNodeWeight = []
        hiddenNodeWeights = []
        hiddenLayerCounter = 0
        for i in range(0, len(self.weights)):
            if inputNodesCounter != 3:
                if inputNodeCounter != self.hiddenNodes-1:
                    inputNodeWeight.append(self.weights[i])
                    inputNodeCounter = inputNodeCounter + 1
                else:
                    inputNodeCounter = 0
                    inputNodeWeights.append(inputNodeWeight)
                    inputNodeWeight = []
                    inputNodesCounter = inputNodesCounter + 1
            else:
                hiddenNodeWeight.append(self.weights[i])
                hiddenNodeCounter = hiddenNodeCounter + 1
                if (hiddenNodeCounter == 4):
                    hiddenNodeWeights.append(hiddenNodeWeight)
                    hiddenLayerCounter = hiddenLayerCounter+1
                    hiddenNodeCounter = 0
                    hiddenNodeWeight = []
        print ("Input Weights")
        for i in range(0, len(inputNodeWeights)):
            print ("Input node: ", i+1, inputNodeWeights[i])
        print ("Hidden Weights")
        for i in range(0, len(hiddenNodeWeights)):
            print (hiddenNodeWeights[i])
    
    #def predict(input1, input2, input3):
     #   for i in range(0, len(weights)): #go over the WHOLE weights array
            
nn = NeuralNetwork(4,3)
nn.printWeights()

        