from typing import List
import copy
import time

class State:
    def __init__(self, state: List[List[int]], cost: int, level: int, expandth_num: int):
        self.state = state #  a 2d list keeping track of ball positions, colors(integers) and empty spots(zeros) 
        self.cost = cost # 1 for every State
        self.level = level
        self.expandth_num = expandth_num   

# colors, 0 correspond for empty location, other positive integers correspond to distinct colors

class Move:
    def __init__(self, initposition, aftposition ): # initposition [tubeno, positintube]
        self.initposition = initposition
        self.aftposition = aftposition


# returns an instance of State class which passes the goal test
def ucsForSolver(startState: State, tubenum):
    
    closed, frontier = [], []
    frontier.append(startState)
    currentState = startState
    expandthNum = 1

    #goal test 
    if isSorted(currentState.state, tubenum):
        return currentState
    
    while frontier:
        leastCost= frontier[0]
        for e in frontier:
            if e.cost < leastCost.cost:
                leastCost = e

        currentState = leastCost
        frontier.remove(currentState)

        #goal test 
        if isSorted(currentState.state, tubenum):
            return currentState

        possibleMoves = allPossyMoves(currentState.state, tubenum)
        #possibleStates are the succStates, from the currentState
        possibleStates = statesAftMove(currentState.state, possibleMoves)
        
        for state in possibleStates:
            expandthNum +=1
            newState = State(state, currentState.cost +1 , currentState.level +1, expandthNum)

            # continue if newState.state in closed, continue current iteration of outer while loop
            if newState.state in (m.state for m in closed):
                continue

            inFrontier = False
            if inFrontier != True:
                for state in frontier: # check if state.state has correspondance with any of the closed states.state
                    if newState.state == state.state and state.cost > newState.cost:
                        state.cost = newState.cost
                        inFrontier = True
                        break

            if inFrontier == True:
                continue
            frontier.append(newState)

        closed.append(currentState)

# IMPLEMENTATION COMPLETE
# all possible moves, this should return a list of possible moves, return list of class Move instances
def allPossyMoves(matrix:List[List[int]], numtubes):
    possibleMoves =[]
    topBalls =[]
    for i in range(numtubes):
        tube, pos =topOfCol(matrix, i)
        if tube != -1 and pos != -1:
            topBalls.append([tube, pos])

    if len(topBalls) == 0:
        return possibleMoves
    elif len(topBalls) != 0:
        for ball in topBalls:
            possibleMoves += possyMovesForBall(matrix, ball[0], ball[1] ,numtubes)
    return possibleMoves
    
# IMPLEMENTATION COMPLETE
def possyMovesForBall(matrix, rownum, position, numtubes):# position is the position in a tube, 
    ballColor = matrix[rownum][position] 
    possibleMoves = []
    if(ballColor == 0):
        return possibleMoves

    for i in range(numtubes):
        if i == rownum:
            continue
        tno, tpos = topOfCol(matrix, i) # tno = tubeno, tpos = position in tube
        if matrix[tno][tpos] == ballColor and tpos != 3:
            possibleMoves.append(Move([rownum, position],[i, tpos+1]))
        elif isEmpty(matrix, i):
            possibleMoves.append(Move([rownum, position], [i, 0]))

    return possibleMoves
    
# IMPLEMENTATION COMPLETE
# do all the checks before calling this function
# return a state.state 
def implementMove(matrix, move: Move):
    oldBall = matrix[move.initposition[0]][move.initposition[1]]
    matrix[move.initposition[0]][move.initposition[1]] = 0
    matrix[move.aftposition[0]][move.aftposition[1]] = oldBall
    return matrix

# IMPLEMENTATION COMPLETE
# return a list of state.state
def statesAftMove(matrix, moves: List[Move]):
    aftStatesList =[]
    for move in moves:
        referenceMatrix = copy.deepcopy(matrix)
        aftStatesList.append(implementMove(referenceMatrix, move))
    return aftStatesList

# IMPLEMENTATION COMPLETE
# return true only if a tube is full and all same color
def isHomogenous(matrix, row):
    numBalls = 0
    for i in range(4):
        if(matrix[row][i] != 0):
            numBalls +=1

    if(numBalls != 4):
        return False

    lastcolor = matrix[row][0]
    for i in range(3):
        if(matrix[row][i+1] != lastcolor ):
            return False
    return True

# IMPLEMENTATION COMPLETE
def isEmpty(matrix, row):
    numempty =0
    for i in range(4):
        if(matrix[row][i] == 0):
            numempty +=1
    if(numempty == 4):
        return True
    else: return False

#IMPLEMENTATION COMPLETE
# returns true if every full column in the matrix is sorted
def isSorted(matrix, numtubes):
    for i in range(numtubes):
        if isHomogenous(matrix, i):
            continue
        elif isEmpty(matrix, i):
            continue
        else: return False
    return True

#IMPLEMENTATION COMPLETE
#returns tube no and ball's position in that tube, doesn't return color, do empty check before 
def topOfCol(matrix, col):
    for i in range(3, -1, -1):
        if matrix[col][i] != 0:
            return col, i 
    return -1, -1

    
def printMatrix(matrix, tubenum):
    for tube in range(tubenum):
        print(matrix[tube])


print(f"input f and e, filled bottle number and empty bottle numbers, respectively")
firstInput = input()
f, e = firstInput.split()
f = int(f)
e= int(e)
ball_matrix = [[0,0,0,0] for _ in range(f+e)]
print(ball_matrix)

numline =0
for line in range(f):
    print("input the start state matrix line by line")
    inputLine = input()
    numline +=1
    intline = inputLine.split()
    intline = [int(i) for i in intline]
    ball_matrix[numline-1] = intline

startState  = State(ball_matrix, 0, 1, 1)

if isSorted(ball_matrix, f+e) != True:
    startTime = time.time()
    endState = ucsForSolver(startState, f+e)
    endTime = time.time()
    print("\n HERE IS THE OUTPUT OF THE UCS PROGRAM: SORTED\n")
    printMatrix(endState.state, f+e)
    print(f"Running Time: {endTime-startTime}")
else:
    print("Balls are already sorted\n")
    printMatrix(ball_matrix, f+e)
