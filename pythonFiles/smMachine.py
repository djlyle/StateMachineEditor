import json

class SMMachine:
    def __init__(self, startState, maxBinaryInputs, maxStates, maxBinaryOutputs):
        self.startState = startState
        self.maxBinaryInputs = maxBinaryInputs
        self.maxStates = maxStates
        self.maxBinaryOutputs = maxBinaryOutputs
        self.transitions = {}
        self.reset()
        return
    
    def reset(self):
        #set the current state to the start state
        self.state = self.startState
        
        #zero out the binary output string
        self.sBinaryOutput = "".rjust(self.maxBinaryOutputs,'0')
        return
        
    def nextState(self,sBinaryInput):
        key = '{}{}'.format(sBinaryInput,self.state)

        if(key not in self.transitions):
            return False

        transition = self.transitions[key]
        self.state = int(transition['nextState'])
            
        sBinaryOutput = transition['output']
        
        #copy the transition output to the binary output
        #converting any nonbinary values to zeroes
        self.sBinaryOutput = ""
        for i in range(0,min(self.maxBinaryOutputs,len(sBinaryOutput))):
            if(sBinaryOutput[i] == '1'):
                self.sBinaryOutput += '1'
            else:
                self.sBinaryOutput += '0'

        #zero pad if necessary for unspecified outputs
        self.sBinaryOutput.rjust(self.maxBinaryOutputs,'0')    
        return True

    def getState(self):
        return self.state
    
    def getOutput(self):
        return self.sBinaryOutput;

    def addTransition(self,sBinaryInput,iState,iNextState,sBinaryOutput):
            if((len(sBinaryInput) != self.maxBinaryInputs) or
               (len(sBinaryOutput) != self.maxBinaryOutputs)):
                return False
            key = "{}{}".format(sBinaryInput,iState)
            sState = "{}".format(iState)
            sNextState = "{}".format(iNextState)
            self.transitions[key] = {"input":sBinaryInput,
                                     "state":sState,
                                     "nextState":sNextState,
                                     "output":sBinaryOutput}
            return True

    def __str__(self):
        return self.toJSON()
        

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        
    
    def loadFromJSON(self,sJSON):
        obj = json.loads(sJSON)
        self.startState = int(obj["startState"])
        self.maxBinaryInputs = int(obj["maxBinaryInputs"])
        self.maxStates = int(obj["maxStates"])
        self.maxBinaryOutputs = int(obj["maxBinaryOutputs"])
        self.state = int(obj["state"])
        self.sBinaryOutput = obj["sBinaryOutput"]
        self.transitions = obj["transitions"]
        
        
