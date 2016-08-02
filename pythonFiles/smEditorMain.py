import tkinter
import smParamsDialog
import smMachine

STICKY_ALL_SIDES=tkinter.W+tkinter.E+tkinter.N+tkinter.S

def find_in_grid(frame, row, column):
    for child in frame.grid_slaves():
        info = child.grid_info()
        if((int(info['row']) == int(row)) and (int(info['column']) == int(column))):
            return child
    return None
    
class Application(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tkinter.BOTH)
        self.create_widgets()
        #Note: the number of transitions won't necessarily match the current row index
        #That is if some rows have been removed the grid layout manager still needs to
        #use a row index greater than the last one used when adding a row below the last
        #visible one already on the screen
        self.numTransitions=0
        self.totalColumns=0
        self.maxNumStates=1
        self.startState=0
        self.numBinaryInputs=0
        self.maxNumStates=0
        self.numBinaryOutputs=0
        self.stateMachine = None
        self.gridVars = []
        self.gridVarsIndex = 0
        #Note: row index should only increment never decrement
        #Even if we remove one or more rows and then add a new one, the grid layout
        #manager should use a row index always greater than the last one used
        self.m_CurrentRowIndex = 0
        return
    
    def create_widgets(self):
        self.menubar = tkinter.Menu(self)
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.createNewStateMachine)
        self.filemenu.add_command(label="Open", command=self.openStateMachine)
        self.filemenu.add_command(label="Save", command=self.saveStateMachine)
        self.editmenu = tkinter.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Add State Transition", command=self.addStateTransition)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.master.config(menu=self.menubar)
        self.body = tkinter.Frame(self)
        self.body.pack(fill=tkinter.BOTH)
        lbl = tkinter.Label(self.body,text="Body")
        lbl.grid(row=0,column=0)
        return

    def addStateTransitionEx(self,sBinaryInput,iState,iNextState,sBinaryOutput):
        col=0
        iBinaryIndex=0
        self.numTransitions += 1
        self.m_CurrentRowIndex += 1
        for i in range(self.numBinaryInputs,0,-1):
            self.gridVars.append(tkinter.IntVar())
            sb = tkinter.Spinbox(self.body, textvariable=self.gridVars[self.gridVarsIndex], from_=0, to=1, width=3)
            self.gridVars[self.gridVarsIndex].set(int(sBinaryInput[iBinaryIndex]))
            sb.grid(row=self.m_CurrentRowIndex,column=col,sticky=STICKY_ALL_SIDES)
            col += 1
            self.gridVarsIndex += 1
            iBinaryIndex += 1
            
        #cell for state
        self.gridVars.append(tkinter.IntVar())
        sb = tkinter.Spinbox(self.body, textvariable=self.gridVars[self.gridVarsIndex], from_=0, to=self.maxNumStates, width=3)
        self.gridVars[self.gridVarsIndex].set(iState)            
        sb.grid(row=self.m_CurrentRowIndex,column=col,sticky=STICKY_ALL_SIDES)
        col += 1
        self.gridVarsIndex += 1
                      
        #cell for next state
        self.gridVars.append(tkinter.IntVar())
        sb = tkinter.Spinbox(self.body, textvariable=self.gridVars[self.gridVarsIndex], from_=0, to=self.maxNumStates, width=3)
        self.gridVars[self.gridVarsIndex].set(iNextState)            
        sb.grid(row=self.m_CurrentRowIndex,column=col,sticky=STICKY_ALL_SIDES)
        col += 1
        self.gridVarsIndex += 1
                      
        iBinaryIndex = 0
        for i in range(self.numBinaryOutputs,0,-1):
            self.gridVars.append(tkinter.IntVar())
            sb = tkinter.Spinbox(self.body, textvariable=self.gridVars[self.gridVarsIndex], from_=0, to=1, width=3, )
            self.gridVars[self.gridVarsIndex].set(int(sBinaryOutput[iBinaryIndex]))
            sb.grid(row=self.m_CurrentRowIndex,column=col,sticky=STICKY_ALL_SIDES)
            col += 1
            self.gridVarsIndex += 1
            iBinaryIndex += 1
        currRow = self.numTransitions
        btn = tkinter.Button(self.body, text="Delete Row", command=lambda:self.removeStateTransition(currRow))
        btn.grid(row=self.m_CurrentRowIndex,column=col,sticky=STICKY_ALL_SIDES)
        return
    
    def addStateTransition(self):
        col = 0
        self.numTransitions += 1
        self.m_CurrentRowIndex += 1
        for i in range(self.numBinaryInputs,0,-1):
            self.gridVars.append(tkinter.IntVar())
            sb = tkinter.Spinbox(self.body,
                                 textvariable=self.gridVars[self.gridVarsIndex],
                                 from_=0, to=1, width=3)
            self.gridVars[self.gridVarsIndex].set(0)
            sb.grid(row=self.m_CurrentRowIndex,column=col,sticky=STICKY_ALL_SIDES)
            col += 1
            self.gridVarsIndex += 1
        for i in range(0,2):
            self.gridVars.append(tkinter.IntVar())
            sb = tkinter.Spinbox(self.body,
                                 textvariable=self.gridVars[self.gridVarsIndex],
                                 from_=0, to=self.maxNumStates, width=3)
            self.gridVars[self.gridVarsIndex].set(0)
            sb.grid(row=self.m_CurrentRowIndex,column=col,sticky=STICKY_ALL_SIDES)
            col += 1
            self.gridVarsIndex += 1
        for i in range(self.numBinaryOutputs,0,-1):
            self.gridVars.append(tkinter.IntVar())
            sb = tkinter.Spinbox(self.body,
                                 textvariable=self.gridVars[self.gridVarsIndex],
                                 from_=0, to=1, width=3)
            self.gridVars[self.gridVarsIndex].set(0)
            sb.grid(row=self.m_CurrentRowIndex,column=col,sticky=STICKY_ALL_SIDES)
            col += 1
            self.gridVarsIndex += 1
        currRow = self.m_CurrentRowIndex
        btn = tkinter.Button(self.body, text="Delete Row", command=lambda:self.removeStateTransition(currRow))
        btn.grid(row=self.m_CurrentRowIndex,column=col,sticky=STICKY_ALL_SIDES)
        return

    def removeStateTransition(self,rowIndex):
        self.numTransitions -= 1
        l = list(self.body.grid_slaves(row=rowIndex))
        for w in l:
            w.grid_forget()
        return
    
    def saveStateMachine(self):
        self.stateMachine = smMachine.SMMachine(self.startState,self.numBinaryInputs,self.maxNumStates, self.numBinaryOutputs)
        rowIndex = 1
        colIndex = 0
        #row 0 is the header so start on row 1
        for rowIndex in range(1,self.m_CurrentRowIndex+1):
            iState = -1
            iNextState = -1
            sBinaryInput = ""
            sBinaryOutput = ""
            for colIndex in range(0,self.numBinaryInputs+2+self.numBinaryOutputs):
                sb = find_in_grid(self.body,rowIndex,colIndex)
                if(sb != None):
                    if(colIndex < self.numBinaryInputs):
                        sBinaryInput += sb.get()
                    elif(colIndex == self.numBinaryInputs):
                        iState = int(sb.get())
                    elif(colIndex == (self.numBinaryInputs + 1)):
                        iNextState = int(sb.get())
                    else:
                        sBinaryOutput += sb.get()
            self.stateMachine.addTransition(sBinaryInput,iState,iNextState,sBinaryOutput)
            sBinaryInput = ""
            sBinaryOutput = ""
            iState = -1
            iNextState = -1
            
        f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        sJSON = self.stateMachine.toJSON()
        print(sJSON)
        f.write(sJSON)
        f.close()
        return

    def openStateMachine(self):
        filename=tkinter.filedialog.askopenfilename()
        sJSON = ""
        with open(filename,'r') as f:
            sJSON = f.read()
        self.stateMachine = smMachine.SMMachine(self.startState,self.numBinaryInputs,self.maxNumStates, self.numBinaryOutputs)
        self.stateMachine.loadFromJSON(sJSON)
        self.startState = self.stateMachine.getStartState()
        self.numBinaryInputs = self.stateMachine.getMaxBinaryInputs()
        self.maxNumStates = self.stateMachine.getMaxStates()
        self.numBinaryOutputs = self.stateMachine.getMaxBinaryOutputs()
        self.numTransitions = 0
        self.totalColumns=0
        self.gridVars = []
        self.gridVarsIndex = 0
                      
        #clear out frame gui body's children
        for widget in self.body.winfo_children():
            widget.destroy()
            
        self.createHeaderRow()
        transitions = self.stateMachine.transitions
        for key in sorted(transitions.keys()):
            transition = transitions[key]
            self.addStateTransitionEx(transition["input"],transition["state"],transition["nextState"],transition["output"])
        return

    def createHeaderRow(self):
        #create a top row of labels as a header
        col = 0
        for i in range(self.numBinaryInputs,0,-1):
            txt = 'I{}'.format(i)
            lbl = tkinter.Label(self.body, text=txt, relief=tkinter.RAISED, width=1, wraplength=1)
            lbl.grid(row=0, column=col,sticky=STICKY_ALL_SIDES)
            col += 1
        lbl = tkinter.Label(self.body, text="State", relief=tkinter.RAISED, width=1, wraplength=1);
        lbl.grid(row=0, column=col, sticky=STICKY_ALL_SIDES)
        col += 1;
        lbl = tkinter.Label(self.body, text="Next State", relief=tkinter.RAISED, width=1, wraplength=1);
        lbl.grid(row=0, column=col, sticky=STICKY_ALL_SIDES)
        col += 1;
        for i in range(self.numBinaryOutputs,0,-1):
            txt = 'O{}'.format(i)
            lbl = tkinter.Label(self.body, text=txt, relief=tkinter.RAISED, width=1, wraplength=1)
            lbl.grid(row=0, column=col, sticky=STICKY_ALL_SIDES)
            col += 1
        return
    
    def createNewStateMachine(self):
        dlg = smParamsDialog.SMParamsDialog(self.master);
        if(dlg.result == None):
            return
        self.startState, self.numBinaryInputs, self.maxNumStates, self.numBinaryOutputs = dlg.result
        #Total Columns = num binary inputs + 1 (for "state" column) + 1 (for "next state" column) + num binary outputs
        self.totalColumns = self.numBinaryInputs + 2 + self.numBinaryOutputs;
        #print("numBinaryInputs: {}".format(numBinaryInputs))
        #print("numBinaryOutputs: {}".format(numBinaryOutputs))
              
        #clear frame gui and initialize it to a new blank state machine
        for widget in self.body.winfo_children():
            widget.destroy()

        self.createHeaderRow() 
        return

def main():
    root = tkinter.Tk()
    root.title("State Machine Editor")
    root.geometry("400x400")
    app = Application(root)
    root.mainloop()
    return

main()
