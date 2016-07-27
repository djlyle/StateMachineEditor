import tkinter
import tkSimpleDialog

class SMParamsDialog(tkSimpleDialog.Dialog):

    def __init__(self, parent, maxInputs = 10, maxOutputs = 10, title = None):
        tkSimpleDialog.Dialog.__init__(self, parent, title)
        self.maxInputs = maxInputs
        self.maxOutputs = maxOutputs
        return
        
    def body(self, master):
        tkinter.Label(master, text="Number Binary Inputs:").grid(row=0)
        tkinter.Label(master, text="Number Binary Outputs:").grid(row=1)

        self.numBinaryInputsSB = tkinter.Spinbox(master, from_=1, to=10)
        self.numBinaryOutputsSB = tkinter.Spinbox(master, from_=0, to=10)

        self.numBinaryInputsSB.grid(row=0,column=1)
        self.numBinaryOutputsSB.grid(row=1,column=1)
        #return the field with initial focus
        return self.numBinaryInputsSB

    def apply(self):
        numBinaryInputs = int(self.numBinaryInputsSB.get())
        numBinaryOutputs = int(self.numBinaryOutputsSB.get())
        self.result = numBinaryInputs, numBinaryOutputs
        return

              
