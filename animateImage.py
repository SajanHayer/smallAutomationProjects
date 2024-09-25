import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PIL import Image,ImageColor
import time

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, image):
    super().__init__()
    
    self.image = image
    self.scale = 1
    # #--Create Canvas---
    self.label = QtWidgets.QLabel()
    self.canvas = QtGui.QPixmap(image.width, image.height)
    self.canvas.fill(Qt.white)
    # self.scene.addPixmap(self.canvas)
    self.label.setPixmap(self.canvas)
    # self.graphicsView.setScene(self.label)
    self.setCentralWidget(self.label)


    #--------
    #intialize the master dict
    self.masterDict = {}
    self.create_masterDict()

    # Set up the timer
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.draw_something)
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

  def draw_something(self):
    # Create a QPainter to draw on the canvas
    painter = QtGui.QPainter(self.label.pixmap())
    # this draws the whole thing, we want to be able to keep track of where we are as well as make sure we dont copy the last 
    # we can use a counter/timer or something to create this, either when a colour ends or keep track of a count then cancel
    colourKeys = list(self.masterDict.keys())
    for colour in colourKeys:
      cordList = self.masterDict[colour]
      for i in range(10):
        if not cordList:
          del self.masterDict[colour]
          break
        cord = cordList.pop(0)
        #get color based on rgb key in masterDict
        paintColour = QtGui.QColor(*colour)
        painter.setPen(paintColour)
        painter.drawPoint(*cord)
        i+=1

    # End the painting and update the label
    painter.end()
    self.label.setPixmap(self.label.pixmap())

  def resizeScreen(self):
    size = self.canvas.size()
    scaledCanvas = self.canvas.scaled(self.scale * size)
    # self.label.setPixmap(scaledCanvas)

  def wheelEvent(self, event):
    curserPosition = event.pos()
    print(curserPosition)
    # Zoom in/out based on mouse wheel movement
    if event.angleDelta().y() > 0:
        self.zoom_in()
    else:
        self.zoom_out()

  def zoom_in(self):
    self.scale *= 1.1
    self.resizeScreen()

  def zoom_out(self):
    self.scale *= 0.9
    self.resizeScreen()
# get the image we want to replicate
inputImage = input("""Input the filename of the image you want to replicate 
                   (this should be located in the same folder as the code):""")
image = Image.open(inputImage)

# Start the timer
start_time = time.time()

#

# allows this to take command line arguments 
app = QtWidgets.QApplication(sys.argv)
window = MainWindow(image)
window.show()
app.exec_()

#  Calculate the elapsed time
elapsed_time = time.time() - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
 