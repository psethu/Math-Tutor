# basicTutor.py
# By: Sethu Prakasam
# April 15th, 2012
##############################################################################

########### NOTES: ###############

# People can use 5x and '^' symbol for exponents instead pf doing x**2 which python recognizes
# AT END OF THIS FILE: I call my "graphTutor" function 
############################################
import math
import string
from Tkinter import *

def mousePressed(event):  
    redrawAll()

def keyPressed(event):
    if (event.char == 's'):  ### Look at performSoperations() for note
        performSoperations()

    if (event.char == 'i'):   ### i
        performIoperations()
    if event.char == 'h':     ### h
        canvas.data.drawHelpScreenOverIntroWords = not canvas.data.drawHelpScreenOverIntroWords
    elif (event.char in 'is'):
        canvas.data.drawHelpScreenOverIntroWords = False
    
    if (canvas.data.isTutorScreen == True):
        typeInStartScreenTextBox(event)

    if (event.char == 'g'):   ## g
        pass

    if event.keysym == "BackSpace":  ### BackSpace
        backSpaceOperations()

    if event.keysym == "Return":   ## Return (Enter key)
        canvas.data.drawSolutionsOverCalcInterface = not canvas.data.drawSolutionsOverCalcInterface
    elif (event.char in 'isg'):   # if event.keysym == 'i', 's', or 'g'
        canvas.data.drawSolutionsOverCalcInterface = False
    if event.keysym == "space":
        canvas.data.displayTutorAnswer = not canvas.data.displayTutorAnswer
        
    redrawAll()

#####################################################################
###      HELPER FUNCTIONS for Controller    #########################
#####################################################################
def performIoperations():
    canvas.data.isTutorScreen = False
    canvas.data.isIntroPage = True

def performSoperations():
    canvas.data.isIntroPage = False  
    canvas.data.isTutorScreen = True
    
    
def typeInStartScreenTextBox(event):
    if (len(canvas.data.textInTextBox) < 15):
        if (event.char in 'x+/-*^.()=0123456789'): 
            canvas.data.drawTextInBox = True   
            canvas.data.textInTextBox += event.char
        
def backSpaceOperations():
    if canvas.data.isTutorScreen == True:
        canvas.data.textInTextBox = canvas.data.textInTextBox[0:len(
        canvas.data.textInTextBox)-1]
        
#########################################################################
################              timerFired()              #################    
#########################################################################

def timerFired():
    print 'canvas.data.textInTextBox:', canvas.data.textInTextBox    
    
    if len(canvas.data.textInTextBox) == 0:
        canvas.data.isAnimatedBlackTextBoxLine = not canvas.data.isAnimatedBlackTextBoxLine

        
    redrawAll()
    delay = 250
    canvas.after(delay, timerFired) # pause, then call timerFired again
    
#########################################################################
#########################################################################    
    
def almostEquals(d1, d2):
    epsilon = 0.000001
    return (abs(d2 - d1) < epsilon)
    
def solveEq(eq):
#####################################################
#  NEED to add below b/c equation may be erroneous 
#  Also below is just a pre-caution, the actual string
# displayed is found in "uniqueCases" function
#####################################################
    if len(eq)== 0:
        return 'No was equation entered'
    if eq.count('x') > 1:
        return "'x' variable used more than once."
    if eq.count('x') < 1:
        return "Please insert 'x' into expression"          
    if 'x/0' in eq:
        return "'x/0' is zero division error."
    if '=' in eq:    
        equalSignIndex = eq.find('=')
        leftSide = eq[0:equalSignIndex]
        if leftSide.count('x') != 1:
            return "Please insert single number \n  on right side of equation"
        print eq    
        print "len(eq):", len(eq), "equalSignIndex:", equalSignIndex 
        if len(eq) == (equalSignIndex+1): 
            # For situations like: '2x+5='  OR '3.23x-4.42='
            return "Please add a number to right hand side."
    else:
        return "Please enter '=' into expression."
#############################################
    print eq
    calcOperatons = "*/+-"
    leftSide = eq[0:eq.find('=')+1]
    print 'leftSide:', 'leftSide:', 'leftSide:', 'leftSide:', leftSide
    ###############################################################################
    ## Using eval below for rightSide b/c int can only convert string to integer,
    ## but eval can convert string to decimal
    ###############################################################################        
    rightSide = eval( eq[eq.find('=')+1:len(eq)] )    # the constant on right side of equation
    print 'rightSide:', rightSide
    print 'type(rightSide):', type(rightSide)
    numAndVariablesList = []  # contains strings of the 
    # sort: num, num+'x', ...(Look at my paper)
    tempConstant = ""
    indexOfAddOrSub = 0
    locationOfx = eq.find('x')
    rightPartOfLeftSide = leftSide[locationOfx+1:len(leftSide)-1]   #Substring from 1 character after 'x' - character before equal sign
    leftPartOfLeftSide = leftSide[0:locationOfx]
    print leftPartOfLeftSide, 'LEFT PART OF LEFT SIDE', "BEFORE THE 'x'"
    print rightPartOfLeftSide, 'RIGHT PART OF LEFT SIDE', 'yeahhhh'
    if '+' in rightPartOfLeftSide:
        print "rightPartOfLeftSide:", rightPartOfLeftSide
        indexOfAddOrSub = rightPartOfLeftSide.find('+')
        tempConstant +=  rightPartOfLeftSide[indexOfAddOrSub + 1: len(leftSide)-1]
        print 'type(tempConstant):', type(tempConstant)
        print 'rightSide:', rightSide, 'type(rightSide):', type(rightSide)
        print 'eval(tempConstant):', eval(tempConstant)
        ###############################################################################
        ## Using eval because int can only convert string to integer, NOT to decimal ##
        ###############################################################################
        rightSide = 1.0 * rightSide - eval(tempConstant)

    if '-' in rightPartOfLeftSide:
        print 'ACTUAL rightPartOfLeftSide:', leftSide[leftSide.find('x')+1:len(leftSide)-1] 
        indexOfAddOrSub = rightPartOfLeftSide.find('-')
        print "ACTUAl rightPartOfLeftSide", rightPartOfLeftSide[indexOfAddOrSub + 1: len(leftSide)-1]
        tempConstant +=  rightPartOfLeftSide[indexOfAddOrSub + 1: len(leftSide)-1]
        print tempConstant, 'TEMP CONSTANT', "COME ONNNNNNN"
        rightSide = 1.0 * rightSide + eval(tempConstant)
        print tempConstant, 'TEMP CONSTANT'
    tempConstant = ""
    print tempConstant, 'SHOULD BE EMPTY'
    if '*' in leftPartOfLeftSide:
        indexOfMultOrDiv = leftPartOfLeftSide.find('*')
        #print indexOfMultOrDiv
        tempConstant += leftPartOfLeftSide[0: indexOfMultOrDiv]
        print tempConstant, type(tempConstant), 'TEMP CONSTANT, DOS'
        print 'rightSide AND tempConstant:', rightSide, tempConstant
        if almostEquals(0, rightSide):
            return rightSide
        else:
            try:
                print 'eval(tempConstant):', eval(tempConstant)
                rightSide = rightSide / (eval(tempConstant))
            except ZeroDivisionError: # For '0x=5' situations  
                return 'Error in equation.'
            print tempConstant, 'TEMP CONSTANT'
        
    if '/' in leftPartOfLeftSide:
        indexOfMultOrDiv = leftPartOfLeftSide.find('/')
        tempConstant += leftPartOfLeftSide[0:indexOfMultOrDiv]
        print tempConstant, type(tempConstant), 'TEMP CONSTANT, DOS'
        rightSide = 1 / rightSide * (eval(tempConstant))
        print 'eval(tempConstant):', eval(tempConstant)
    return rightSide
    

#print solveEq('x+1=')
def testsolveEq():
    print '---------------------'
    print "testing solveEq()..."
    print '---------------------'
    assert(solveEq("-5*x+10=0") == 2.0)
    assert(solveEq('-4*x+10=0') == 2.5)
    assert(solveEq('-4*x+10=18') == -2.0)
    assert(solveEq('x+1=0') == -1.0)
    print '---------------------'
    print 'all tests passed!'
    print '---------------------'

testsolveEq()


#"""#####################################################################
# -- Drawing Functions -------------------------------------------------#
#########################################################################
        
def formatThenSolveEquation(equation):
    for charIndex in xrange(1, len(equation)):
        if equation[charIndex] == 'x' and (equation[charIndex-1] in string.digits):
            equation = equation.replace(equation[charIndex-1]+equation[charIndex], equation[charIndex-1] + '*' +equation[charIndex])
    return solveEq(equation)   # solveEq function from test2.py
    
def createGeneralText(cellSize, x, y):
    print cellSize, x, y
    generalText = " 1. On left side of equal sign, group all 'x' terms together \
     \n 2. Group all constants together \n 3. Do steps 1 and 2 for right side of equal sign \
     \n 4. Move the 'x' terms to the left side \
     \n 5. Move all constants to the right side \
     \n 6. Divide 'x' coefficient by number on right side"
    canvas.create_text((x)*cellSize, y*cellSize, text = "Solution", font = "Arial 16 bold underline", anchor=NW)
    canvas.create_text((x+1)*cellSize, (y+2) *cellSize, text = "%s" % generalText, font = "Arial 12", anchor=NW)
    canvas.create_text((x)*cellSize, canvas.data.cHeight - (y-1)*cellSize, text = "Answer", font = "Arial 16 bold underline", anchor=NW)
    canvas.create_text(125, 275, text = "('Spacebar' to display/hide answer.)", fill="#330066", font = "Arial 12 bold", anchor = NW)

def drawSolutionsToTextThatWasInBoxEquation():
    ### Below is GENERAL text to be displayed 
    cellSize = canvas.data.cellSize
    startRowGeneralText = 1 
    startColGeneralText = 4
    createGeneralText(cellSize, startRowGeneralText, startColGeneralText)
    #####################################################################
    
    canvas.data.solvedEquation = formatThenSolveEquation(canvas.data.textInTextBox)
        
    print 'canvas.data.solvedEquation:', canvas.data.solvedEquation  # prints when I press enter key
    if canvas.data.displayTutorAnswer == True:  ## displaying solved equation 
    #of form x=(...), where(...) is a number
        canvas.create_text((startRowGeneralText+1)*cellSize, canvas.data.cHeight-(startColGeneralText-2)*cellSize, text = "%s" % canvas.data.solvedEquation, anchor=NW, font = "Arial 12 bold") ### This is where I display the answer to my one variable equation
    print cellSize
    
def drawSolutionsInfo():
    xIntro = canvas.data.rows * canvas.data.cols
    margin = canvas.data.margin 
    canvas.create_text(xIntro - margin, 3 * margin + 5, text = "('Enter': Back)", anchor = W, fill="#330066", font = "Arial 12 bold")
    
def drawTextInBox():   
    canvas.create_text(81, 156, text = '%s' % canvas.data.textInTextBox, anchor = NW, font = "Arial 12 bold")

def drawTutorTextBoxLine():
    rows, cols, cellSize = (canvas.data.rows, canvas.data.cols, canvas.data.cellSize)
    # rows, cols, margin = 12, 16, 25
    canvas.create_line(canvas.data.textBoxLineX, 155, canvas.data.textBoxLineX, 171, fill="black", width=3)

def drawTutorTextBox():
    left = 3 * canvas.data.cellSize
    top = 6 * canvas.data.cellSize
    right = 15 * canvas.data.cellSize
    bottom = 7 * canvas.data.cellSize
    canvas.create_rectangle(left, top, right, bottom, fill = "#6699FF", width = 1.5)

def drawTutorCell(row, col, color):
    margin, cellSize = canvas.data.margin, canvas.data.cellSize
    left = margin + col*cellSize
    right = left + cellSize
    top = margin + row*cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill = "black")
    inM = 0.1 # inM == innerMargin for actual color
    canvas.create_rectangle(left + inM, top + inM, right - inM, bottom-inM, \
    fill = color) # creates the 'inner squares' for each cell
    
def drawTutorCalcBoxes():
    rows, cols, margin = (canvas.data.rows, canvas.data.cols, canvas.data.margin)
    # rows, cols, margin = 12, 16, 25
    buttonBG = canvas.data.buttonBG
    startRowOfTutorBox = canvas.data.startRowOfTutorBox # 10
    startColOfTutorBox = canvas.data.startColOfTutorBox # 2
    for row in xrange(startRowOfTutorBox, 9):
        for col in xrange(startColOfTutorBox, 14):
            drawTutorCell(row, col, buttonBG)    

def drawTheNumber(row, col, num):
    margin, cellSize = canvas.data.margin, canvas.data.cellSize
    left = margin + col*cellSize + 10.5
    right = left + cellSize
    top = margin + row*cellSize + 12.5
    bottom = top + cellSize
    canvas.create_text(left, top, text=num, fill="purple", \
    font="Helvetica 16 bold")

    
def drawTutorNumbers():
    rows, cols, margin=(canvas.data.rows, canvas.data.cols, canvas.data.margin)
    startRowOfTutorBox = canvas.data.startRowOfTutorBox
    startColOfTutorBox = canvas.data.startColOfTutorBox # 2
    highestNumXrange = 10
    num = 0
    for row in xrange(startRowOfTutorBox, startRowOfTutorBox + 1):
        for col in xrange(startColOfTutorBox, startColOfTutorBox + highestNumXrange):
            drawTheNumber(row, col, num)
            num += 1

def drawTutorVariableAndOperators():
    rows, cols, margin = (canvas.data.rows, canvas.data.cols, canvas.data.margin)
    xIntro = rows * cols # 12 * 16
    yIntro = rows * cols # 12 * 16
    canvas.create_text(155, 225, text="    +  -   *   .   =         \n    x", fill="purple", font="Helvetica 16 bold")
    # Start at 75, 200
    pass
            
def drawTutorWords():
    rows, cols, margin = (canvas.data.rows, canvas.data.cols, canvas.data.margin)
    xIntro = rows * cols # 12 * 16
    yIntro = rows * cols # 12 * 16
    newYintro = yIntro + 2*2*margin + 10 # 302
    if canvas.data.drawSolutionsOverCalcInterface == False:
        canvas.create_text(xIntro + margin - 30, 130, text="Press: 'Enter' to solve!", fill="#330066", font="Helvetica 16 bold")

def drawTutorScreen():
    rows = canvas.data.rows
    cols = canvas.data.cols
    margin = canvas.data.margin
    xIntro = rows * cols
    left = 0
    top = 0
    right = canvas.data.cWidth
    bottom = canvas.data.cHeight
    canvas.create_rectangle(left, top, right, bottom, fill= canvas.data.background)
    canvas.create_text(xIntro, margin*2, text="Mode: Solve", fill="#CCCCCC",
    font="Helvetica 26")  
    drawTutorWords()
                
    if canvas.data.drawSolutionsOverCalcInterface == False:
        canvas.create_text(right/2, bottom - 30, text="Press: 'i' to return to intro screen", fill="#330066", font="Helvetica 16")
        drawTutorCalcBoxes()
        drawTutorTextBox()
        drawTutorNumbers()
        drawTutorVariableAndOperators()
    else:
        drawSolutionsToTextThatWasInBoxEquation()
        drawSolutionsInfo()
        
def drawIntroHelp(rows, cols, margin):
    rows = rows+1
    print 'rows:', rows
    help = " - Tutor has two modes: \
    \n     1. Solving 'mx+b=c' equations  \
    \n     2. Graphing polynomials \n\
    \n - To access graph mode: \
    \n     Close current window THEN click on new window \
    \n - To navigate: \
    \n     Look for words highlighted in purple"
    canvas.create_text(3*rows, 6*rows, text= '%s' % help, fill = "#66FF66", font = 'Arial 12 bold', anchor = NW)
    
def drawIntroWords():
    rows = canvas.data.rows
    cols = canvas.data.cols
    margin = canvas.data.margin
    xIntro = rows * cols
    yIntro = rows * cols
    wordsX, wordsY = canvas.data.cWidth/2, margin
    canvas.create_text(wordsX, wordsY, text="Welcome to Math tutor!"
    , font="Arial 26")
    if canvas.data.drawHelpScreenOverIntroWords == False:
        canvas.create_text(xIntro, yIntro, text="Press: 'h' for help, \n           's' to start", 
        fill="#330066", font = "Helvetica 24 ")
    elif canvas.data.drawHelpScreenOverIntroWords == True:
        drawIntroHelp(rows, cols, margin)
        canvas.create_text(7 * (rows + 1), 20*(rows+1), text = "(Press 'h' to go back.)", font = "Arial 16 bold", anchor = W, fill="#330066")
  
def drawIntroPage():
    left = 0
    top = 0
    right = canvas.data.cWidth
    bottom = canvas.data.cHeight
    canvas.create_rectangle(left, top, right, bottom, fill= canvas.data.background)
    drawIntroWords()
    
#########################################################################
############################   reDRAW All() ############################
#########################################################################

def redrawAll():
    canvas.delete(ALL)
    drawIntroPage()

    if canvas.data.isTutorScreen == True:
        drawTutorScreen()
    elif canvas.data.isIntroPage == True:
        drawIntroPage()
    print canvas.data.drawTextInBox
    if canvas.data.drawSolutionsOverCalcInterface == False and canvas.data.isIntroPage == False and canvas.data.drawTextInBox == True:
        drawTextInBox()
        
    if canvas.data.isTutorScreen == True: 
        if canvas.data.drawSolutionsOverCalcInterface == False: 
            if canvas.data.isAnimatedBlackTextBoxLine == True:
                if len(canvas.data.textInTextBox) == 0:
                    drawTutorTextBoxLine()        
        
    
#################################################################################
#################################################################################
##########################       init           #################################
#################################################################################    
def init():
    canvas.data.isTutorScreen = False
    canvas.data.isIntroPage = True
    canvas.data.background = "#3399CC" # light blue color
    canvas.data.mouseCoord = (150, 150)
    canvas.data.buttonBG = "#CCFFFF"
    canvas.data.startRowOfTutorBox = 6
    canvas.data.startColOfTutorBox = 2
    canvas.data.isMouseCoordInBoxesFrom0to9 = False
    canvas.data.mouseInBoxCoords = (0, 0)
    canvas.data.delay = 250
    canvas.data.isAnimatedBlackTextBoxLine = False
    canvas.data.drawTextInBox = False
    init2()
    
def init2():
    canvas.data.textInTextBox = ""
    canvas.data.solvedEquation = ""
    canvas.data.textBoxLineX = 80
    
    canvas.data.drawSolutionsOverCalcInterface = False
    canvas.data.drawHelpScreenOverIntroWords = False
    canvas.data.displayTutorAnswer = False
    canvas.data.drawHelpScreenWords = False
    canvas.data.mouseCoord = (150, 150)
    
def run(rows, cols):
    # create the root and the canvas
    global canvas
    root = Tk()
    margin = 25
    cellSize = 25
    canvasWidth = cols * cellSize # 450, w/o margin: 400
    canvasHeight =  rows * cellSize # 350, w/o margin: 300
    print canvasWidth, canvasHeight
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.cWidth = canvasWidth
    canvas.data.cHeight = canvasHeight
    canvas.data.rows = rows
    canvas.data.cols = cols
    init()
    # set up events

    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run(14, 18)

from graphTutor import *
