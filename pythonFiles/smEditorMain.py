import tkinter
import smParamsDialog

class Application(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tkinter.BOTH)
        self.create_widgets()
        return
    def create_widgets(self):
        self.menubar = tkinter.Menu(self)
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.createNewStateMachine)
        self.filemenu.add_command(label="Open", command=self.openStateMachine)
        self.filemenu.add_command(label="Save", command=self.saveStateMachine)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.master.config(menu=self.menubar)
        self.body = tkinter.Frame(self)
        self.body.pack(fill=tkinter.BOTH)
        lbl = tkinter.Label(self.body,text="Body")
        lbl.grid(row=0,column=0)
        return

    def saveStateMachine(self):
        #todo
        return

    def openStateMachine(self):
        filename=tkinter.filedialog.askopenfilename()
        #todo:
        #1)open file and read contents as a new state machine
        #2)clear frame gui and initialize it to match new state machine
        return

    def createNewStateMachine(self):
        dlg = smParamsDialog.SMParamsDialog(self.master);
        numBinaryInputs, numBinaryOutputs = dlg.result
        #print("numBinaryInputs: {}".format(numBinaryInputs))
        #print("numBinaryOutputs: {}".format(numBinaryOutputs))
              
        #clear frame gui and initialize it to a new blank state machine
        for widget in self.body.winfo_children():
            widget.destroy()
        col = 0
        for i in range(numBinaryInputs,0,-1):
            txt = 'I{}'.format(i)
            lbl = tkinter.Label(self.body, text=txt, relief=tkinter.RAISED)
            lbl.grid(row=0, column=col)
            col += 1
        lbl = tkinter.Label(self.body, text="S", relief=tkinter.RAISED);
        lbl.grid(row=0,column=col);
        col += 1;
        lbl = tkinter.Label(self.body, text="NS", relief=tkinter.RAISED);
        lbl.grid(row=0,column=col);
        col += 1;
        for i in range(numBinaryOutputs,0,-1):
            txt = 'O{}'.format(i)
            lbl = tkinter.Label(self.body, text=txt, relief=tkinter.RAISED)
            lbl.grid(row=0, column=col)
            col += 1
        #print("done")
        return

def main():
    root = tkinter.Tk()
    app = Application(root)
    root.mainloop()
    return

main()
