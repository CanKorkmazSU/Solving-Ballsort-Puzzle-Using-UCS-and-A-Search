from typing import List
import copy
import time


class State:
    def __init__(self, state: List[List[int]], cost: int, heuristicCost: int, level: int, expandth_num: int):
        self.state = state #  a 2d list keeping track of ball positions, colors(integers) and empty spots(zeros) 
        self.cost = cost # 1 for every State
        self.heuristicCost = heuristicCost
        self.level = level
        self.expandth_num = expandth_num

# colors, 0 correspond for empty location, other positive integers correspond to distinct colors

class Move:
    def __init__(self, initposition, aftposition ): # initposition [tubeno, positintube]
        self.initposition = initposition
        self.aftposition = aftposition

# A* SEARCH METHODS
def astForSolver(startState: State, tubenum):
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
            if e.cost + e.heuristicCost < leastCost.cost+ leastCost.heuristicCost:
                leastCost = e

        currentState = leastCost
        frontier.remove(currentState)
        
         #goal test 
        if isSorted(currentState.state, tubenum):
            return currentState

        possibleMoves = allPossyMoves(currentState.state, tubenum)

        #possibleStates are the succStates, from the currentState, they are matrixes
        possibleStates = statesAftMove(currentState.state, possibleMoves)

        for state in possibleStates:
            expandthNum +=1
            heuCost = heuristic(state, tubenum)
            newState = State(state, currentState.cost +1 , heuCost, currentState.level +1, expandthNum)
            
            if newState.state not in (m.state for m in closed) and newState.state not in (m.state for m in frontier):
                frontier.append(newState)
            elif newState.state in (m.state for m in frontier):
                for k in frontier:
                    if k.state == newState.state and newState.cost + newState.heuristicCost < k.cost + k.heuristicCost:
                        frontier.remove(k)
                        frontier.append(newState)
            elif newState.state in (m.state for m in closed):
                for n in closed:
                    if n.state == newState.state and newState.cost + newState.heuristicCost < n.cost + n.heuristicCost:
                        closed.remove(n)
                        n = copy.deepcopy(newState)
                        frontier.append(n)

        closed.append(currentState)

# this should count the number of balls in a tube after the string of balls of the same color starting at bottom, add 1 for each blank slot in tube, 2 for differentColor
def heuristic(State: List[List[int]], tubenum: int):
    heuristicCost = 0
    for tube in range(tubenum):
        heuristicCost += tubeHeuristic(State, tube)
    return heuristicCost

# A* SEARCH METHODS
def tubeHeuristic(matrix, tno):
    bottomColor = matrix[tno][0]
    differentFound = False
    heuristicCost = 0
    if bottomColor == 0:
        return 4
    elif matrix[tno][1] == 0:
        return 3
    for i in range(3):
        if matrix[tno][i+1] == bottomColor and differentFound == False:
            continue
        elif differentFound == False and matrix[tno][i+1] != bottomColor and matrix[tno][i+1] != 0:
            heuristicCost += 2
            differentFound = True
        elif differentFound == False and matrix[tno][i+1] != 0:
            heuristicCost += 1
            differentFound = True
        elif differentFound and matrix[tno][i+1] == 0:
            heuristicCost+=1
    return heuristicCost

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

heuCost = heuristic(ball_matrix, f+e)
startState  = State(ball_matrix, 0, heuCost, 1, 1)

if isSorted(ball_matrix, f+e) != True:
    startTime = time.time()
    endState = astForSolver(startState, f+e)
    endTime = time.time()
    print("\n HERE IS THE OUTPUT OF THE UCS PROGRAM: SORTED\n")
    printMatrix(endState.state, f+e)
    print(f"Running Time: {endTime-startTime}")
else:
    print("Balls are already sorted\n")
    printMatrix(ball_matrix, f+e)
