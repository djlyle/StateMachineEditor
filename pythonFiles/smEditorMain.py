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
        self.numTransitions=0
        self.totalColumns=0
        self.maxNumStates=1
        self.stateMachine = None
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
    
    def addStateTransition(self):
        col = 0
        self.numTransitions += 1
        for i in range(self.numBinaryInputs,0,-1):
            sb = tkinter.Spinbox(self.body, from_=0, to=1, width=3)
            sb.grid(row=self.numTransitions,column=col,sticky=STICKY_ALL_SIDES)
            col += 1
        for i in range(0,2):
            sb = tkinter.Spinbox(self.body, from_=0, to=self.maxNumStates, width=3)
            sb.grid(row=self.numTransitions,column=col,sticky=STICKY_ALL_SIDES)
            col += 1
        for i in range(self.numBinaryOutputs,0,-1):
            sb = tkinter.Spinbox(self.body, from_=0, to=1, width=3)
            sb.grid(row=self.numTransitions,column=col,sticky=STICKY_ALL_SIDES)
            col += 1
        currRow = self.numTransitions
        btn = tkinter.Button(self.body, text="Delete Row", command=lambda:self.removeStateTransition(currRow))
        btn.grid(row=self.numTransitions,column=col,sticky=STICKY_ALL_SIDES)
        return

    def removeStateTransition(self,rowIndex):
        self.numTransitions -= 1
        print("row:{}".format(rowIndex))
        for widget in self.body.grid_slaves():
            if(int(widget.grid_info()["row"]) == rowIndex):
                widget.grid_forget()
        return
    
    def saveStateMachine(self):
        self.stateMachine = smMachine.SMMachine(self.startState,self.numBinaryInputs,self.maxNumStates, self.numBinaryOutputs)
        rowIndex = 1
        colIndex = 0
        #row 0 is the header so start on row 1
        for rowIndex in range(1,self.numTransitions+1):
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
        #todo:
        #1)open file and read contents as a new state machine
        #2)clear frame gui and initialize it to match new state machine
        return

    def createNewStateMachine(self):
        dlg = smParamsDialog.SMParamsDialog(self.master);
        self.startState,self.numBinaryInputs, self.maxNumStates, self.numBinaryOutputs = dlg.result
        #Total Columns = num binary inputs + 1 (for "state" column) + 1 (for "next state" column) + num binary outputs
        self.totalColumns = self.numBinaryInputs + 2 + self.numBinaryOutputs;
        #print("numBinaryInputs: {}".format(numBinaryInputs))
        #print("numBinaryOutputs: {}".format(numBinaryOutputs))
              
        #clear frame gui and initialize it to a new blank state machine
        for widget in self.body.winfo_children():
            widget.destroy()
            
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

def main():
    root = tkinter.Tk()
    app = Application(root)
    root.mainloop()
    return

main()
