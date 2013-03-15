# events-example0.py
# Barebones timer, mouse, and keyboard events

from Tkinter import *
from math import *
import string 

def mousePressed(event):
    print canvas.data.xyGraphCoords[0:61], 
    print "----------------------------------------"
    print "cWidth/2=", canvas.data.cWidth/2
    print "cHeight/2=", canvas.data.cHeight/2
    redrawAll()

def eventInfo(eventName, x, y, ctrl, shift): 
    # helper functions that creates a string with the event's information
    # Prints the string for debugging
    msg = ""
    if ctrl:
        msg = msg + "ctrl-"
    if shift:
        msg = msg + "shift-"
    msg = msg + eventName
    msg = msg + " at " + str((x, y))
    #print msg
    return msg
    
def rightTrace(event):
    if canvas.data.traceMode == True:
        if event.keysym == 'Right':
            canvas.data.rightTraceHold = True


def leftTrace(event):
    if canvas.data.traceMode == True:
        if event.keysym == 'Left':
            canvas.data.leftTraceHold = True


def isxAxisLeftIncomplete(scale, cWidth, cHeight):
    drawAxisLabels(cWidth, cHeight, scale) # Doing this to get 
    # the updated canvas.data.pixelCoordOfDomain0
    print '------------------------------------------------'
    print 'FROM: isxAxisLeftIncomplete'
    print 'canvas.data.pixelCoordOfDomain0:', canvas.data.pixelCoordOfDomain0
    print '------------------------------------------------'
    if canvas.data.pixelCoordOfDomain0 >= scale:
        return True
    else:
        return False        

        

def isxAxisRightIncomplete(scale, cWidth, cHeight):
    drawAxisLabels(cWidth, cHeight, scale) # Doing this to get 
    # the updated canvas.data.pixelCoordOfDomain1
    print '------------------------------------------------'
    print 'FROM: isxAxisRightIncomplete'
    print 'canvas.data.pixelCoordOfDomain1:', canvas.data.pixelCoordOfDomain1
    print '------------------------------------------------'
    if cWidth - canvas.data.pixelCoordOfDomain1 >= scale:
        return True
    else:
        return False

def isyAxisTopIncomplete(scale, cWidth, cHeight):
    drawAxisLabels(cWidth, cHeight, scale) #  Doing this to get 
    # the updated canvas.data.pixelCoordOfRange0
    if canvas.data.pixelCoordOfRange0 >= scale:
        return True
    else:
        return False
        
def isyAxisBottomIncomplete(scale, cWidth, cHeight):
    drawAxisLabels(cWidth, cHeight, scale) #  Doing this to get 
    # the updated canvas.data.pixelCoordOfRange1
    if cHeight - canvas.data.pixelCoordOfRange1 >= scale:
        return True
    else:
        return False

def editScale_OperationByDirection(cWidth, cHeight):            
    if isxAxisLeftIncomplete(canvas.data.scale, cWidth, cHeight):   
        canvas.data.domainForPanMode[0] += -1 # Assumes if xAxisIncompleteFromLeftBefore(scale):
        # is true and decreases domain by '1'   
        drawAxisLabels(cWidth, cHeight, canvas.data.scale) # DO this because:
        # The c.d.pixelCoordOfDomain0 needs to be calculated immediately
        # after an up or down arrow press. The c.d.pixelCoordOfDomain0
        # is calculated in drawAxisLabels funtion 
    
    if isxAxisRightIncomplete(canvas.data.scale, cWidth, cHeight):
        canvas.data.domainForPanMode[1] += 1
        drawAxisLabels(cWidth, cHeight, canvas.data.scale)
        
    if isyAxisTopIncomplete(canvas.data.scale, cWidth, cHeight):
        canvas.data.rangeForPanMode[0] += -1
        drawAxisLabels(cWidth, cHeight, canvas.data.scale)
        
    if isyAxisBottomIncomplete(canvas.data.scale, cWidth, cHeight):
        canvas.data.rangeForPanMode[1] += 1
        drawAxisLabels(cWidth, cHeight, canvas.data.scale)
        
def editScale(event):    
    cWidth = canvas.data.cWidth
    cHeight = canvas.data.cHeight
    
    if event.keysym == 'Up': 
        canvas.data.scale += 5        
        
    elif event.keysym =='Down':
        if canvas.data.scale >= 45:
            canvas.data.scale -= 5
  
    if event.keysym == 'Up' or event.keysym == 'Down':
        editScale_OperationByDirection(cWidth, cHeight)

def panRight():
    # Below moves: xAxis -> AND yAxis ->
    canvas.data.yAxisXPosition += canvas.data.panSpeed # moveXaxis: ->
    canvas.data.countForxAxisPan += canvas.data.panSpeed
    
    canvas.data.panDX += canvas.data.panSpeed
    canvas.data.panDY += 0
    
    
    if canvas.data.countForxAxisPan % canvas.data.scale == 0: 
    # Once countForPan becomes == scale value, add a negative number
    # to the left end of the x-axis
        canvas.data.addFromLeftEndToXaxis = True   

    if canvas.data.addFromLeftEndToXaxis == True:
        canvas.data.domainForPanMode[0] += -1            

def panLeft():
    # Below moves: xAxis <- AND yAxis <-
    canvas.data.yAxisXPosition -= canvas.data.panSpeed  
    canvas.data.countForxAxisPan -= canvas.data.panSpeed
    
    canvas.data.panDX -= canvas.data.panSpeed
    canvas.data.panDY -= 0
    
    if canvas.data.countForxAxisPan % canvas.data.scale == 0: 
        # Once countForPan becomes == scale value, add a negative number
        # to the left end of the x-axis            
        canvas.data.addFromRightEndToXaxis = True
        
    if canvas.data.addFromRightEndToXaxis == True:
        canvas.data.domainForPanMode[1] += 1

def panUp():
    # Below moves: xAxis Up AND yAxis Up
    canvas.data.xAxisYPosition -= canvas.data.panSpeed
    canvas.data.countForyAxisPan -= canvas.data.panSpeed
    
    canvas.data.panDX -= 0
    canvas.data.panDY -= canvas.data.panSpeed
    
    if canvas.data.countForyAxisPan % canvas.data.scale == 0:
    # Once countForPan becomes == scale value, add a positive number
    # to the top of the y-axis
        canvas.data.addFromBottomToYaxis = True
    
    if canvas.data.addFromBottomToYaxis == True:
        canvas.data.rangeForPanMode[1] += 1        

def panDown():
    # Below moves: xAxis Down AND yAxis Down
    canvas.data.xAxisYPosition += canvas.data.panSpeed
    canvas.data.countForyAxisPan += canvas.data.panSpeed
    
    canvas.data.panDX += 0
    canvas.data.panDY += canvas.data.panSpeed
    
    if canvas.data.countForyAxisPan % canvas.data.scale == 0:
    # Once countForPan becomes == scale value, add a positive number
    # to the top of the y-axis
        canvas.data.addFromTopToYaxis = True
    
    if canvas.data.addFromTopToYaxis == True:
        canvas.data.rangeForPanMode[0] += -1
        
        
def panMode(event):
    scale = canvas.data.scale
    cWidth = canvas.data.cWidth
    cHeight = canvas.data.cHeight
    
    if canvas.data.traceMode == False and canvas.data.editScale == False:
        if event.keysym == 'Right':
            panRight()
        
        if event.keysym == 'Left':
            panLeft()

        if event.keysym == 'Up':
            panUp()
                
        if event.keysym == 'Down':
            panDown()
    print '-------------------------------------------------------'
    print 'FROM: panMode(event)'
    print 'canvas.data.addFromLeftEndToXaxis:', canvas.data.addFromLeftEndToXaxis
    print
    print 'canvas.data.countForxAxisPan:', canvas.data.countForxAxisPan
    print 'canvas.data.scale:', canvas.data.scale
    print 'canvas.data.countForyAxisPan:', canvas.data.countForyAxisPan
    print '--------------------------------------------------'                 
            
    print 'CODE CAME TO panMode', canvas.data.panSpeed
        
def keyPressed(event):
    print '---------------------------------------------------------------------'
    print event.keysym, event.keysym, event.keysym, event.keysym, event.keysym
    print '---------------------------------------------------------------------'
    if event.keysym == 'Home':
        initWithBooleans()
    
    if event.keysym == 'F2':
        canvas.data.editScale = not canvas.data.editScale 
        canvas.data.traceMode = False 
        canvas.data.panMode = False
        
    if event.keysym == 'F3':
        canvas.data.panMode = not canvas.data.panMode
        canvas.data.traceMode = False 
        canvas.data.editScale = False
        
    if event.keysym == 'F4':
        canvas.data.traceMode = not canvas.data.traceMode
        canvas.data.editScale = False
        canvas.data.panMode = False
                
    if event.keysym == 'F5':
        canvas.data.help = not canvas.data.help
        canvas.data.drawInitialHelp = False
    
    if canvas.data.traceMode:
        if event.keysym == 'Control_R':
            if canvas.data.traceSpeed <= 49:
                canvas.data.traceSpeed += 1
        if event.keysym == 'Control_L':
            if canvas.data.traceSpeed >= 1:
                canvas.data.traceSpeed -= 1
    
    if event.keysym == 'F1':
        canvas.data.help = False
        canvas.data.drawInitialHelp = not canvas.data.drawInitialHelp
        
    if event.char == 'q':
        increment = 10
        canvas.data.domainToCreateGraph[0] += (-1 * increment)
        canvas.data.indexOfXYGraphCoordsForTrace += (increment * 10) ### Need to change
        # the index so the trace box does not move when graph is extended
        ### We multiply by 10 because increasing domain by one
        # means making 10 coordinate points
    
    if event.char == 'w':    
        increment = 10
        canvas.data.domainToCreateGraph[1] += increment

    if event.keysym == 'Return':
        canvas.data.drawGraph = not canvas.data.drawGraph  
            
    leftTrace(event)
    rightTrace(event)
    
    if canvas.data.panMode == True:
        panMode(event)
    
    changeEquation(event)

    if canvas.data.editScale == True:    
        editScale(event)
        
    redrawAll()

def changeEquation(event):
    if (canvas.data.drawGraph == False and 
    ((event.char in string.digits) or (event.char in 'x+-/*^()0.123456789e'))):
    # Took out: cositan so one cannot enter trig functions
        canvas.data.equation += event.char
    if event.keysym == 'BackSpace':
        canvas.data.equation = canvas.data.equation[0:len(canvas.data.equation)-1]
    if event.keysym == 'space':
        canvas.data.equation = ''

def keyReleased(event):
    if canvas.data.traceMode == True:
        if event.keysym == 'Right':
            canvas.data.rightTraceHold = False
        elif event.keysym == "Left":
            canvas.data.leftTraceHold = False
    redrawAll()
    
def mouseMotion(event):  # modified code from notes
    ctrl = ((event.state & 0x0004) != 0) # ? - ASK People especially ASA FRANK
    shift = ((event.state & 0X0001) != 0) # ? - ASK People especially ASA FRANK
    canvas.data.info = eventInfo("mouseMotion", event.x, event.y, ctrl, shift)
    canvas.data.mouseCoord = (event.x, event.y)

###############################################################################
#########################     Timer fired      ################################
###############################################################################

def timerFired():
    if canvas.data.traceMode == False:  ### This is where i reinitialize coords ###
        canvas.data.xyGraphCoords = []
    
    if canvas.data.traceMode == True:    
        print '------------------------------------------------------------'
        print canvas.data.traceSpeed
        print 'canvas.data.indexOfXYGraphCoordsForTrace:', canvas.data.indexOfXYGraphCoordsForTrace
        print '------------------------------------------------------------'
        if canvas.data.rightTraceHold:
            if (canvas.data.indexOfXYGraphCoordsForTrace <= 
                 ( (len(canvas.data.xyGraphCoords) - 1) - canvas.data.traceSpeed) ):
                canvas.data.count += 1  # for debugging        
                canvas.data.indexOfXYGraphCoordsForTrace += canvas.data.traceSpeed # Moving across list of points, one by one
        
        elif canvas.data.leftTraceHold:
            if canvas.data.indexOfXYGraphCoordsForTrace >= canvas.data.traceSpeed:
                canvas.data.count -= 1  # for debugging
                canvas.data.indexOfXYGraphCoordsForTrace -= canvas.data.traceSpeed  # 5 b/c skipps 5 indexes at a time, so 
                # goes from lets say 50th element: 0.0 to 55th element: 0.5 
    print 'FROM TIMER FIRED:', 'canvas.data.panMode:', canvas.data.panMode
    redrawAll()
    delay = 250 # milliseconds
    canvas.after(delay, timerFired) # pause, then call timerFired again
    
###############################################################################
#########################     Drawing Functions    ############################
###############################################################################
def drawWarning():
    cellSize = canvas.data.cellSize    
    canvas.create_text(cellSize*11, cellSize * 16, anchor = NW,
    text="Please enter proper equation, \n then HIT enter. 'Enter' to go back.", fill = 'blue', font = "Arial 12")

def drawTraceSpeed():
    cellSize = canvas.data.cellSize    
    canvas.create_text(cellSize, cellSize * 18, anchor = NW,
    text="speed: %d" % canvas.data.traceSpeed, fill = 'blue', font = "Arial 14")    
    
def drawTracing():   # The square that moves when left or right arrow is pressed
    #print canvas.data.xyGraphCoords
    ### canvas.data.indexOfXYGraphCoordsForTrace = 5
    cW = canvas.data.cWidth
    cH = canvas.data.cHeight
    squareSideLength = 5
    cellSize = canvas.data.cellSize
    
    drawTraceSpeed()
    
    if len(canvas.data.xyGraphCoords) == 0:
        drawWarning()
        ## Only happens for the first time you do not have a graph ##
         # First nothing is xyGraphCoords 
         # Then, xyGraphCoords stores the coordinates of the previous graph
         # once the user hits enter for the first graph.
    else:
        xCoord = canvas.data.xyGraphCoords[canvas.data.indexOfXYGraphCoordsForTrace][0]
        yCoord = canvas.data.xyGraphCoords[canvas.data.indexOfXYGraphCoordsForTrace][1]        
        xyGraphCoordTuple = canvas.data.xyGraphCoords[canvas.data.indexOfXYGraphCoordsForTrace]
        
        canvas.data.recLeft = ( (cW/2) + canvas.data.scale * xyGraphCoordTuple[0] - squareSideLength ) + canvas.data.panDX        
        canvas.data.recTop =  ( (cH/2) - canvas.data.scale * xyGraphCoordTuple[1] - squareSideLength ) + canvas.data.panDY
        canvas.data.recRight =  ( (cW/2) + canvas.data.scale * xyGraphCoordTuple[0] + squareSideLength ) + canvas.data.panDX
        canvas.data.recBottom = ( (cH/2) - canvas.data.scale * xyGraphCoordTuple[1] + squareSideLength ) + canvas.data.panDY
        
        canvas.create_rectangle(canvas.data.recLeft, canvas.data.recTop, canvas.data.recRight, canvas.data.recBottom, fill="", outline='blue') 
        canvas.create_text(cellSize, cellSize * 19, text = "x: %f    y: %f" % (xCoord, yCoord), anchor = NW, font = "Arial 12 bold", fill = '#333333')
        
def checkToAddNumberToAxis():
    ## These adding to axis functions belong here because as soon as
    ## I draw the axes, I would need to make changes to the Model 
    ## false again.    
    if canvas.data.addFromLeftEndToXaxis == True:
        canvas.data.addFromLeftEndToXaxis = False
        
    if canvas.data.addFromRightEndToXaxis == True:
        canvas.data.addFromRightEndToXaxis = False        

    if canvas.data.addFromTopToYaxis == True:
        canvas.data.addFromTopToYaxis = False
    
    if canvas.data.addFromBottomToYaxis == True:
        canvas.data.addFromBottomToYaxis = False
        
def drawXaxis(scale):
    for dashNum in xrange(canvas.data.domainForPanMode[0], canvas.data.domainForPanMode[1]):  
    # dashNum: -5 to 5 in this case when cWidth = 500 and scale = 50, NOTE: draws from LEFT to RIGHT
        #print dashNum
        # For each variable initialized: 'X' indicates x-axis
        (Xx1, Xy1, Xx2, Xy2) = ( ((canvas.data.yAxisXPosition) + (dashNum * scale)), (canvas.data.xAxisYPosition) - 10,
        ((canvas.data.yAxisXPosition) + (dashNum*scale)), (canvas.data.xAxisYPosition) + 10)
        canvas.create_line(Xx1, Xy1, Xx2, Xy2, fill = 'black', width=1.5)
        
        if dashNum != 0:
            canvas.create_text( ((canvas.data.yAxisXPosition) + (dashNum*scale)), (canvas.data.xAxisYPosition) + 10,
            text = '%d' % dashNum, anchor=NW, fill = '#666666', font = "Arial 12")
        
        if dashNum == canvas.data.domainForPanMode[0]:
            canvas.data.pixelCoordOfDomain0 = ((canvas.data.yAxisXPosition) + (dashNum * scale))
            
        if dashNum == (canvas.data.domainForPanMode[1] - 1):
            canvas.data.pixelCoordOfDomain1 = ((canvas.data.yAxisXPosition) + (dashNum * scale))        

def drawYaxis(scale):            
    for dashNum in xrange(canvas.data.rangeForPanMode [0], canvas.data.rangeForPanMode [1]):   # dashNum: -5 to 5 in this case when cHeight = 500 and scale = 50, NOTE: draws from UP to DOWN
        (Yx1, Yy2, Yx2, Yy2) = ( ((canvas.data.yAxisXPosition) - 10), (canvas.data.xAxisYPosition) + (dashNum*scale),
        ((canvas.data.yAxisXPosition) + 10), (canvas.data.xAxisYPosition) + (dashNum*scale))
        canvas.create_line(Yx1, Yy2, Yx2, Yy2, fill = 'black', width=1.5)
        
        if dashNum != 0:
            canvas.create_text( ((canvas.data.yAxisXPosition) + 10), (canvas.data.xAxisYPosition) + (dashNum*scale),
            text = '%d' % (-1*dashNum), anchor=NW, fill = '#666666', font = "Arial 12")
        
        if dashNum == canvas.data.rangeForPanMode[0]:
            canvas.data.pixelCoordOfRange0 = ( (canvas.data.xAxisYPosition) + (dashNum*scale) ) 
            
        if dashNum == (canvas.data.rangeForPanMode[1] - 1):
            canvas.data.pixelCoordOfRange1 = ( (canvas.data.xAxisYPosition) + (dashNum*scale) )
            
def drawAxisLabels(cWidth, cHeight, scale):    
    canvas.data.countTimesGoneToAxisLabel += 1

    xAxisLeft = 0
    xAxisRight = cWidth    
    yAxisTop = 0
    yAxisBottom = cHeight
    
    left = 0
    top = cHeight/2
    right = cWidth
    bottom = cHeight

    canvas.create_line(  (xAxisLeft), canvas.data.xAxisYPosition, 
    (xAxisRight), canvas.data.xAxisYPosition, fill = 'black')  # x-axis
    
    canvas.create_line( (canvas.data.yAxisXPosition) , yAxisTop,
    (canvas.data.yAxisXPosition), yAxisBottom, fill = 'black')   # y-axis
    
    drawXaxis(scale)
    drawYaxis(scale)    
    
    checkToAddNumberToAxis()

def createPoints(domain, equation):
    a = []
    print 'domain', domain
    for xCoord in xrange(domain[0] * 10, (domain[1] * 10) + 1, 1):  # multiply by 10 to get 100 b/c you want the step to be 0.1 and you want the decimalXcoord to be 10.0. You plus 1 to domain[1] * 10 b/c you want to include the last value of x    
        decimalXcoord = 1.0 * xCoord / 10
        ### print decimalXcoord
        
        try:
            y = eval(equation.replace('x',  ( '(' +('%0.2f' % decimalXcoord) + ')')    ))
            a += [(decimalXcoord, y)]
            a.sort()
        except SyntaxError:
            drawWarning()
            print "No equation to evaluate, so 'y = eval(equation.replace ...' FAILS"
            print '------------------------------------------------------------------'
            print '------------------------------------------------------------------'
        except IndexError:
            drawWarning()
            print "list index out of range"
        except NameError:
            drawWarning()
            print "Please insert parentheses"
        except TypeError:
            drawWarning()
            print "'float' object not callable"
        except ZeroDivisionError:
            drawWarning()
            print "DIVISION BY ZEROOOOOOO"
        except ValueError:
            drawWarning()
            print "Cant have a negative num in SquareRoot!"        
    return a


def adjustEquation():
    print 'excessive'
    equation = canvas.data.equation
    #equation = '5x'  # You can enter by just saying 0.5x and using carrot: x^2 instead of: x**2
    equation = equation.replace('^', '**')  ## Need to do equation = equation.replace... b/c strings are immutable
    for charIndex in xrange(1, len(equation)):
        if equation[charIndex] == 'x' and (equation[charIndex-1] in string.digits):
            equation = equation.replace( equation[charIndex - 1] + equation[charIndex],
            # replacing the number before 'x' and 'x' with: number before x, '*' sign, and 'x'
                                          equation[charIndex-1] + '*' + equation[charIndex])
    for charIndex in xrange(1, len(equation)):
        if (equation[charIndex] in 'tcs') and (equation[charIndex-1] in string.digits):
            equation = equation.replace( equation[charIndex - 1] + equation[charIndex],
                                          equation[charIndex - 1] + '*' + equation[charIndex])    
    return equation
    
def drawGraph(cWidth, cHeight): 
    equation = adjustEquation()
    print equation, 'dude'
    
    canvas.data.xyGraphCoords = createPoints(canvas.data.domainToCreateGraph, equation)
    
    for indexOfxyCoord in xrange(1, len(canvas.data.xyGraphCoords)):   # DO NOT confuse decimalXcoords with 
    # xCoord on x-axis
        #print len(canvas.data.xyGraphCoords), indexOfxyCoord
        decimalXcoord1 = canvas.data.xyGraphCoords[indexOfxyCoord-1][0]
        decimalYcoord1 = canvas.data.xyGraphCoords[indexOfxyCoord-1][1]
        
        decimalXcoord2 = canvas.data.xyGraphCoords[indexOfxyCoord][0]
        decimalYcoord2 = canvas.data.xyGraphCoords[indexOfxyCoord][1]
        
        x1 =             decimalXcoord1 * canvas.data.scale  + cWidth/2 + canvas.data.panDX
        ### cWidth/2 needs to be added since x is positive to right of origin
         # on x-axis and x has to be greater than 250 px to show this on Tkinter window.
        ### This works even if decimalXcoord1 is negative.
         # Ex: If decimalXcoord1 were -5.0, -5.0 * 50(scale) = -250.0; -250.0 + 250 = 0.0
         # This puts x1 all the way to left end (0, ?) coordinate
        y1 = cHeight/2 - decimalYcoord1 * canvas.data.scale  + canvas.data.panDY
        ### 'cHeight/2 -' 
         # because if decimalYcoord1 was negative it would need to be changed 
         # to a positive number by doing 'cHeight/2 -' so that the y1-pixel would be
         # displayed in a position below the origin.
        ### IF decimalXcoord1 was positive then y1 would be a y-pixel above the origin
        x2 =            decimalXcoord2  * canvas.data.scale + cWidth/2 + canvas.data.panDX
        y2 = cHeight/2 - decimalYcoord2 * canvas.data.scale + canvas.data.panDY
        
        canvas.create_line(x1, y1, x2, y2, fill = 'purple', width = '2')

        if 0 <= indexOfxyCoord <= 10:
            if indexOfxyCoord == 10:
                print 'len(canvas.data.xyGraphCoords):', len(canvas.data.xyGraphCoords)
                print 'len(canvas.data.xyGraphCoords)[indexOfxyCoord]:', canvas.data.xyGraphCoords[indexOfxyCoord]
    print '--------------------------------------------------'
    print 'FROM: drawGraph'
    print '--------------------------------------------------'    
    
def drawScale():
    cellSize = canvas.data.cellSize  # Should be 25
    tx = cellSize
    ty = cellSize * 18
    originalScale = 50
    level = ( canvas.data.scale - originalScale ) / 5
    canvas.create_text(tx, ty, 
    text = 'Zoom level: %d\n(%d px)' % (level, canvas.data.scale), 
    anchor = NW, fill = 'blue', font = "Arial 12 bold")
 
def editEquationHelp(cellSize):
    tx = cellSize * 12 - 10
    ty = cellSize * 12 - 15
    canvas.create_text(tx, ty, text = "Supports/allows: \
    \n - Operators: + - / * ^ ( ) \n - Variables/Constants: x/e \n - Numbers: 0.123456789 \
    \n - BACKSPACE: Delete prev. \n - SPACE: Clear equation" ,
    anchor = NW, fill = '#336633', font = 'Arial 11')
        #x+-/*^()0.123456789e
    
def drawInitialHelp(cellSize):
    cellSize = canvas.data.cellSize
    helpSpacing = 5
    tx = cellSize * 1 - 2*helpSpacing
    ty = cellSize * 12
    ty2 = cellSize * 14
    panHelpY = cellSize * 12
    panHelpX = cellSize * 12 - 2 * helpSpacing
    canvas.create_text(tx, ty, text = "READ ME: \n - Press 'Enter' whenever modifying\
    \n     equation. 'Enter' again to regraph", 
    anchor = NW, fill = '#336633', font = "Arial 10 bold")
    
    canvas.create_text(tx, ty2, text = " - Press 'Home' to restart \n - Press 'q' or 'w' to\
 extend graph \n     10 units to left/right \n - MODES: [F2]Zoom, [F3]Pan, \n    \
 [F4]Trace, [F5]Help" ,
    anchor = NW, fill = '#336633', font = "Arial 10")    
    
    editEquationHelp(cellSize) 

    
def drawHelp(cellSize):
    helpSpacing = 5
    tx = cellSize * 1 - helpSpacing
    ty = cellSize * 12 + 3 * helpSpacing
    if canvas.data.editScale:
        canvas.create_text(tx, ty, text = "HELP: \n -To zoom in/out PRESS 'Up' arrow \n or 'Down' arrow\
        \n-NOTE: Maximum level to zoom out: -2",
        anchor = NW, fill = '#336633', font = "Arial 10")
    if canvas.data.traceMode:
        canvas.create_text(tx, ty, text = "HELP: \n -To trace left/right, PRESS 'Left' \n or 'Right' arrows\
        \n- To increase/decrease speed,\n PRESS control keys, ('Left'/'Right')",
        anchor = NW, fill = '#336633', font = "Arial 10")            
    if canvas.data.panMode == True:
        canvas.create_text(tx, ty, text = "HELP: \n - Use arrow keys to move graph",
        anchor = NW, fill = '#336633', font = "Arial 10")    
        
def drawCurrentModeAndMenu(cellSize):
    tx = 14 * cellSize
    ty = 18 * cellSize
    if canvas.data.traceMode == True:
        canvas.create_text(tx, ty, text = "Mode: trace", anchor = NW, font = 'Arial 12 bold')
    elif canvas.data.editScale == True:
        canvas.create_text(tx, ty, text = "Mode: zoom", anchor = NW, font = 'Arial 12 bold')    
    elif canvas.data.panMode == True:
        canvas.create_text(tx, ty, text = "Mode: pan", anchor = NW, font = 'Arial 12 bold')

def drawReadMe():
    cellSize = canvas.data.cellSize
    tx = 15 * cellSize
    ty = 19 * cellSize
    canvas.create_text(tx, ty, text = "[F1] readMe", anchor = NW, 
    font = 'Arial 14 bold', fill = '#003300')
def redrawAll():
    canvas.delete(ALL)
    origin = (0, 0) # ORGIN for tkinter is top left at: 0, 0
    cWidth, cHeight = canvas.data.cWidth, canvas.data.cHeight
    info = canvas.data.info
    
    canvas.create_rectangle(origin[0], origin[1], cWidth, cHeight, fill = 'white')
    #canvas.create_text(canvas.data.cellSize * 12, canvas.data.cHeight-10, text=info, anchor = NW, 
    #font=("Helvetica", 12, "bold"))

    if canvas.data.drawGraph == True:
        drawGraph(cWidth, cHeight)
    
    canvas.create_text(25, 25, text = "Equation: %s " % (canvas.data.equation), anchor = W, fill = "#333333", font = "Arial 12 bold")
    
    drawAxisLabels(cWidth, cHeight, canvas.data.scale)
 
    if canvas.data.traceMode == True:
        drawTracing()

        
    if canvas.data.editScale == True:
        drawScale()
    
    if canvas.data.help == True:
        drawHelp(canvas.data.cellSize)

    if canvas.data.drawInitialHelp:
        drawInitialHelp(canvas.data.cellSize)
        
    drawCurrentModeAndMenu(canvas.data.cellSize)
    
    drawReadMe()
        
def initWithIntegers():    
    canvas.data.cellSize = 25
    canvas.data.mouseCoord = (150, 150)
    canvas.data.scale = 50
    canvas.data.domainToCreateGraph = [-10, 10] # Cannot change canvas.data.domain if I want blue square to be displayed
    canvas.data.domainForPanMode = [-1 * (canvas.data.cWidth/canvas.data.scale)/2, 
                                        (canvas.data.cWidth/canvas.data.scale)/2 + 1] ## [-5, -6]
    
    canvas.data.rangeForPanMode = [-1 * (canvas.data.cHeight/canvas.data.scale)/2, 
                                        (canvas.data.cHeight/canvas.data.scale)/2 + 1] ## [-5, -6]
    
    canvas.data.rectCenter = [250 , 250]
    canvas.data.recLeft = 0
    canvas.data.recRight = 0
    canvas.data.recTop = 0
    canvas.data.recBottom = 0
    canvas.data.xyGraphCoords = []
    canvas.data.indexOfXYGraphCoordsForTrace = 100  # Starting at 50 for now because for x^2, 50th index gives (0.0, 0.0) tuple
    canvas.data.panSpeed = 10
    canvas.data.count = 0
    canvas.data.countForxAxisPan = 0 # Once this equals the scale ADD a number to the x-axis or y-axis
    canvas.data.countForyAxisPan = 0
    canvas.data.yAxisXPosition = 250
    canvas.data.xAxisYPosition = 250  ## Do NOT take out otherwise tKinter will not show up and application will not run
                                      ## even though draw axis label for xAxis and yAxis uses only canvas.data.yAxisXPosition
    canvas.data.countTimesGoneToAxisLabel = 0
    canvas.data.pixelCoordOfDomain0 = 0
    canvas.data.pixelCoordOfDomain1 = 0
    canvas.data.pixelCoordOfRange0 = 0
    canvas.data.pixelCoordOfRange1 = 0
    canvas.data.panDX = 0
    canvas.data.panDY = 0
    canvas.data.traceSpeed = 1
    
def initWithBooleans():
    canvas.data.rightTraceHold = False
    canvas.data.leftTraceHold = False
    canvas.data.drawGraph = True
    canvas.data.displayEquation = True
    canvas.data.traceMode = False
    canvas.data.editScale = False
    canvas.data.help = False
    canvas.data.panMode = False
    canvas.data.addFromLeftEndToXaxis = False
    canvas.data.addFromRightEndToXaxis = False
    canvas.data.addFromTopToYaxis = False
    canvas.data.addFromBottomToYaxis = False
    canvas.data.drawInitialHelp = True
    
    canvas.data.equation = "x^2"
    canvas.data.info = "Mouse Motion Event :D"

    initWithIntegers()
    print "canvas.data.equation:", canvas.data.equation
    print 'canvas.data.domainToCreateGraph:', canvas.data.domainToCreateGraph
    #canvas.data.equation = adjustEquation()
    #points = createPoints(canvas.data.domainToCreateGraph , canvas.data.equation)
    #print points, 'sdfsdfsd'
    
def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    cWidth = 500
    cHeight = 500
    canvas = Canvas(root, width=cWidth, height=cHeight)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.cWidth = cWidth
    canvas.data.cHeight = cHeight
    initWithBooleans()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    root.bind("<Motion>", mouseMotion)
    root.bind("<KeyRelease>", keyReleased)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()
