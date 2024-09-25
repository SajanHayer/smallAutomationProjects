# Example file showing a circle moving on screen
import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#width and height of screen
width = screen.get_width()
height = screen.get_height()

#inital code
playerPosition = pygame.Vector2(width / 2, height / 2)
dt = 0 
spacePressed = False
movementSpeed = 16

targetList = []
targetIndex = 0
finalPosition = 0 

postionDict={
  0:(width/2, height/2),
  1:(width/6, height/6),
  2:(width/2, height/6),
  3:(width*.83, height/6),
  4:(width*.83, height/2),
  5:(width*.83, height*.83),
  6:(width/2, height*.83),
  7:(width/6, height*.83),
  8:(width/6, height/2),
  }

# This function is to move nothing more so we need to constantyl add or remove
# distance to red postion to get to target point
# recursive function
def moveRedCircle():
  global playerPosition, targetList, targetIndex, finalPosition
  if targetIndex < len(targetList):
    target = targetList[targetIndex]
    dx = target[0] - playerPosition[0]
    dy = target[1] - playerPosition[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5    # x^2 + y^2
    if distance > movementSpeed:
        playerPosition = (
            playerPosition[0] + movementSpeed * dx / distance,
            playerPosition[1] + movementSpeed * dy / distance
        )
    else:
        targetIndex += 1
        print(targetIndex)
    
    if distance <= movementSpeed:
      playerPosition = (
          target[0],
          target[1]
      )

    finalPosition = list(postionDict.keys())[list(postionDict.values()).index(targetList[-1])]

def getTargetpoints():
  global targetList, targetIndex, finalPosition
  targetList.clear()
  targetVal = random.randint(1,8)
  targetIndex = 0
  print('---------')
  print(f'Target Index {finalPosition}')
  print(f'Target val {targetVal}')
  zeroCheck = targetVal - finalPosition
  firstLoop, secondLoop, thirdLoop = False, False, False 

  # first check (our first spin)
  if zeroCheck > 0 and finalPosition == 0:
    firstLoop = True
  
  # To move to the next point clockwise
  if zeroCheck > 0 and finalPosition != 0:
    secondLoop = True

  # if point is behind we move in a circle
  if zeroCheck <= 0 and finalPosition != 0:
    thirdLoop = True

  key = 0
  while key < len(list(postionDict.values())):
    # add keys normally
    if firstLoop:
      if key!=0 and key <= targetVal:
        targetList.append(postionDict[key])

    # move clock wise to next biggest point
    if secondLoop:
      if key != 0 and key<=targetVal and key > finalPosition:
        targetList.append(postionDict[key])
      
      if key == 8:
        finalPosition = 0
        
    # if target is behind current postion rotate til we get there
    if thirdLoop:
      if key != 0 and key >= finalPosition and finalPosition != 0:
        targetList.append(postionDict[key])
        if key == 8:
          finalPosition = 0 
          key = 1
      # append as normal
      if key <= targetVal and finalPosition == 0:
        targetList.append(postionDict[key])

    key +=1
  finalPosition = 0
  
  # og loop:
  # for key in postionDict:
  #   if key!=0 and key <= targetVal:
  #     targetList.append(postionDict[key])
  #     targetIndex = 0
  # print(targetList)


while running:
  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      getTargetpoints()

  # fill the screen with a color to wipe away anything from last frame
  screen.fill("purple")


  for key in postionDict:
    if key != 0:
      pygame.draw.circle(screen, 'white', postionDict[key], 45)

  pygame.draw.circle(screen, "red", playerPosition, 40)


  keys = pygame.key.get_pressed()
  # if keys[pygame.K_SPACE]:
      # TODO: To animate the circle moving from one position to another 
      #       we have to move it as if it was a player below by adding or 
      #       subtracting a certain amount of distance 
      # TODO: To get to where we want it to go, we have a target postion and
      #       then we can make the circle move using the best movement
      #       we can add algorithms, searchs and much more to efficently do this 

      # TODO: For what I need, we need to hit space bar to load up a random amount
      #       of target white circles, then continouly call a function to move our 
      #       red circl to each target postion 


  # flip() the display to put your work on screen
  spacePressed = False
  moveRedCircle()
  pygame.display.flip()

  # limits FPS to 60
  # dt is delta time in seconds since last frame, used for framerate-
  # independent physics.
  dt = clock.tick(60) / 1000

pygame.quit()