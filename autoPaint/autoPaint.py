import pyautogui as pyag
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PIL import Image,ImageColor
import time

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, image):
    super().__init__()
    
    self.image = image
    
    #--Create Canvas---
    self.label = QtWidgets.QLabel()
    canvas = QtGui.QPixmap(100, 100)
    canvas.fill(Qt.white)
    self.label.setPixmap(canvas)
    self.setCentralWidget(self.label)
    #--------
    #intialize the master dict
    self.masterDict = {}
    self.create_masterDict()
    self.clickPencil()
    self.paintimage()
    # # Set up the timer
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.paintimage)
    self.timer.start(10) 
    # Update the window every 10 milliseconds
    
    # self.draw_something()



  def create_masterDict(self):
    print(f'Width: {image.width} Height: {image.height}')

    # Loop through each pixel in the image getting the colour Value and the 
    # cords of that value, MasterDict has format {colourValue: [(x,y), ]}
    for x in range(image.width):
      for y in range(image.height):
        colourVal = image.getpixel((x,y))
        if colourVal not in self.masterDict:
          self.masterDict[colourVal]=[(x,y)]
        else:
          self.masterDict[colourVal].append((x,y))

  def clickPencil(self):
    imageNotFound = False
    try: 
      pyag.click('pencil.png')
      pyag.click()
    except Exception as e:
      imageNotFound = True
      print('Image not found')

    if imageNotFound:
      try:
        pyag.click('pencilClicked.png')
        pyag.click()
      except Exception as e:
        print('Image not found')

  def changeColour(self, rgb):
    try:
      output = pyag.locateOnScreen('editcolours.png', confidence=0.7)
      point = pyag.center(output)
      pyag.doubleClick(point)
    except:
      pyag.doubleClick('editcoloursClicked.png')
      
    pyag.moveTo(1250, 645)
    i = 0
    while i < 3:
      pyag.doubleClick()
      pyag.typewrite(str(rgb[i]))
      pyag.moveRel(0,40)
      i+=1
    pyag.hotkey('enter')

  def paintimage(self):
    colourKeys = list(self.masterDict.keys())
    for colour in colourKeys:
      cordList = self.masterDict[colour]
      print(colour)
      self.changeColour(colour)
      for i in range(100):
        if not cordList:
          del self.masterDict[colour]
          break
        cord = cordList.pop(0)
        x = 24 + cord[0]
        y = 231 + cord[1]
        pyag.click(x,y)
        i+=1

  # def draw_something(self):
  #   # Create a QPainter to draw on the canvas
  #   painter = QtGui.QPainter(self.label.pixmap())
  #   # this draws the whole thing, we want to be able to keep track of where we are as well as make sure we dont copy the last 
  #   # we can use a counter/timer or something to create this, either when a colour ends or keep track of a count then cancel
  #   colourKeys = list(self.masterDict.keys())
  #   for colour in colourKeys:
  #     cordList = self.masterDict[colour]
  #     print(colour)
  #     for i in range(10):
  #       if not cordList:
  #         del self.masterDict[colour]
  #         break
  #       cord = cordList.pop(0)
  #       #get color based on rgb key in masterDict
  #       paintColour = QtGui.QColor(*colour)
  #       painter.setPen(paintColour)
  #       painter.drawPoint(*cord)
  #       i+=1

        
        
  #   # End the painting and update the label
  #   painter.end()
  #   self.label.setPixmap(self.label.pixmap())

# get the image we want to replicate
image = Image.open("dragon.jpg")
skipColour = None
# Start the timer
start_time = time.time()

# allows this to take command line arguments 
app = QtWidgets.QApplication(sys.argv)
window = MainWindow(image)
window.show()
app.exec_()


#  Calculate the elapsed time
elapsed_time = time.time() - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
 