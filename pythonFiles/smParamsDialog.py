import tkinter
import tkSimpleDialog

class SMParamsDialog(tkSimpleDialog.Dialog):

    def __init__(self, parent, maxInputs = 10, maxOutputs = 10, maxStates=1000, title = None):
        self.maxInputs = maxInputs
        self.maxOutputs = maxOutputs
        self.maxStates = maxStates
        
        tkSimpleDialog.Dialog.__init__(self, parent, title)
        return
        
    def body(self, master):
        tkinter.Label(master, text="Start State:").grid(row=0)
        tkinter.Label(master, text="Number Binary Inputs:").grid(row=1)
        tkinter.Label(master, text="Number Binary Outputs:").grid(row=2)
        tkinter.Label(master, text="Max Number States:").grid(row=3)
        self.startStateSB = tkinter.Spinbox(master, from_=0, to=self.maxStates)
        self.startStateSB.grid(row=0,column=1)
        self.numBinaryInputsSB = tkinter.Spinbox(master, from_=1, to=self.maxInputs)
        self.numBinaryInputsSB.grid(row=1,column=1)
        self.numBinaryOutputsSB = tkinter.Spinbox(master, from_=0, to=self.maxOutputs)
        self.numBinaryOutputsSB.grid(row=2,column=1)
        self.maxNumStatesSB = tkinter.Spinbox(master, from_=0, to=self.maxStates);
        self.maxNumStatesSB.grid(row=3,column=1)
        
        #return the field with initial focus
        return self.startStateSB

    def apply(self):
        startState = int(self.startStateSB.get())
        numBinaryInputs = int(self.numBinaryInputsSB.get())
        numBinaryOutputs = int(self.numBinaryOutputsSB.get())
        maxNumStates = int(self.maxNumStatesSB.get())
        self.result = startState, numBinaryInputs, maxNumStates, numBinaryOutputs
        return

              
