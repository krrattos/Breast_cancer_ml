import math, sys, random
from time import time

temp=1000
heuristic = 'manhattan_dist'
class PuzzleState:
    def __init__(self, numbers):
        #initialize the data
        self.cells=[]
        self.blankLocation = 0, 0
        #[0,1,2,3,4,5,6,7,8]
        k= 0
        for i in range(3):
            row=[]
            for j in range(3):
                row.append(numbers[k])
                if numbers[k]==0:
                    self.blankLocation= i,j
                k +=1
            self.cells.append(row)

    def printState(self):
        #print the current state
        lines = []
        horizontalline = ("_" * (13))
        print(horizontalline)
        for row in self.cells:
            rowline ="|"
            for col in row:
                if col == 0:
                    col = "."
                rowline = rowline +" " + col.__str__() + "|"
            print(rowline)
            print(horizontalline)
    
    def isGoal(self):
        #check is the state is goal or not
        current = 0
        for i in range(3):
            for j in range(3):
                if current !=self.cells[i][j]:
                    return False
                current +=1
        return True
    
    def legalMoves(self):
        #return all the legal mover 
        row, col = self.blankLocation
        legalMoves=[]
        if row != 0:
            legalMoves.append("up")
        if row !=2:
            legalMoves.append("down")
        if col != 0:
            legalMoves.append("left")
        if col !=2:
            legalMoves.append("right")
        return legalMoves

    def resultState(self, move):
        #return the next state based the move
        row, col = self.blankLocation
        if move == "up":
            newrow = row-1
            newcol = col
        elif move == "down":
            newrow = row +1
            newcol = col
        elif move == "left":
            newrow = row
            newcol = col-1
        elif move =="right":
            newrow = row 
            newcol = col+1
        else:
            raise "ilegal move"

        newPuzzle = PuzzleState([0,0,0,0,0,0,0,0,0])
        newPuzzle.cells = [value[:] for value in self.cells]
        #new puzzle cells
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]

        newPuzzle.blankLocation = newrow, newcol
        return newPuzzle
    
    def __eq__(self, other):
        for row in range(3):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    
class SearchProblem:
    def __init__(self, state):
        # initialize the search problem
        self.puzzle = state

    def getStartState(self):
        # return the chile state
        return self.puzzle

    def getSuccessor(self,state):
        #retrun all the child state
        succs = []
        
        for move in state.legalMoves():
            cState = state.resultState(move)
            succs.append((cState, move))
        return succs

    def isGoalState(self, state):
        #return information that state is goal or not
        return state.isGoal()
  
#calculating distance by manhatan formula

def mdistatance(xy1, xy2):    
    return abs(xy1[0]-xy2[0]) + abs(xy1[1]-xy2[1])


goal = {0:(2, 2), 1:(0,0), 2:(0,1), 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2), 7:(2,0), 8:(2,1)}
# checking for the heightest point if start decreasing
#  then it we move and if again start increasing it should stop
def hvalue(state):
    hscore = 0
    for row in range(3):
        for col in range(3):
            if state.cells[row][col] == 0:
                continue
            goal1 = goal[state.cells[row][col]]
            xy1 = (row, col)
            hscore += mdistatance(xy1, goal1)
    return hscore

# new

def if_(test, result, alternative):
    if test:
        return result
    else:
        return alternative

schedule = lambda t: if_(t <1000, temp *math.exp(-0.005*t ), 0)

tempp=[]

def simulated_annealing(prob):
    current = prob.getStartState()
    num_of_states=0
    for t in range(sys.maxsize):
        T = schedule(t)
        num_of_states+=1
        if T ==0:
            return current,num_of_states
        #current.printState()
        # print("T value is ", T)
        tempp.append(T)
        succs = prob.getSuccessor(current)
        next = random.choice(succs)
        delta_e = hvalue(next[0])-hvalue(current)
        if delta_e < 0 or probability(math.exp(delta_e/T)):
            current = next[0]


def probability(p):
    return p > random.uniform(0.0, 1.0)

initState=[6, 7, 3, 8, 4, 2, 1, 0, 5]
state = PuzzleState(initState)
prob = SearchProblem(state)
start=time()
s,nos = simulated_annealing(prob)
end=time()
print('Initial Temp is: ',temp)
print('Heuristic is:',heuristic)

print('\nInitial State:\n')
print(initState[0:3])
print(initState[3:6])
print(initState[6:9])


print ("\nfinal State:")
s.printState()

if s.isGoal():
  print('Message: Algo Reached Final State Successfully')
else:
  print('Message: Failed to reach Final State')

print('\nNumber of States explored:',nos)
print('\nTime Taken is:',end-start)
rate=0.0
prev=temp
for it in tempp[1:]:
  rate=rate+ prev-it
  prev=it
rate=rate/len(tempp)
  # print(it)
print("cooling rate is" ,rate)