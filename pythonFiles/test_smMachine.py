import smMachine
import unittest

class TestSMMachine(unittest.TestCase):
    def test_sm_run(self):
        startState = 0
        maxBinaryInputs = 4
        maxStates = 6
        maxBinaryOutputs = 3
        machine = smMachine.SMMachine(startState,maxBinaryInputs,maxStates,maxBinaryOutputs)
        machine.addTransition("0000",0,0,"000")
        machine.addTransition("0001",0,1,"111")
        machine.addTransition("0000",1,0,"000")
        machine.addTransition("0011",1,1,"101")
        machine.nextState("0000")
        self.assertEqual(machine.getState(),0)
        state = machine.nextState("0001")
        self.assertEqual(machine.getState(),1)
        return
    def test_sm_serialize(self):
        startState = 0
        state = startState
        maxBinaryInputs = 4
        maxStates = 6
        maxBinaryOutputs = 3
        machine = smMachine.SMMachine(startState,maxBinaryInputs,maxStates,maxBinaryOutputs)
        machine.addTransition("0000",0,0,"000")
        machine.addTransition("0001",0,1,"111")
        machine.addTransition("0000",1,0,"000")
        machine.addTransition("0011",1,1,"101")
        sJSON = "{}".format(machine)
        machine2 = smMachine.SMMachine(0,0,0,0)
        machine2.loadFromJSON(sJSON)
        machine2.nextState("0001")
        self.assertEqual(machine2.getState(),1)
        machine2.nextState("0011")
        self.assertEqual(machine2.getOutput(),"101")
        return

if __name__ == '__main__':
    unittest.main()
    
