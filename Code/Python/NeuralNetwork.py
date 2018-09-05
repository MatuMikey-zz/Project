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

    def predict(self, input1, input2, input3):
        output = 0
        outputs = []
        inputs = [input1, input2, input3]
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
                        print("Layer:", j+1, "Node:", i+1)
                    outputs.append(output)
        print(outputs)
        output = 0
        for i in range(0, len(outputs)):
            output = output+outputs[i]
        print(output/(1+abs(output)))
                        
nn = NeuralNetwork(19,3)
nn.predict(0.5,0.5,0.5)            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
