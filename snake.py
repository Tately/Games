# end screen, images for food, snake, background, Scoreboard
import random
import pygame

from random import randrange
import pygame

class GameObject:
    def __init__(self, screen, xPos = 0, yPos = 0, texture = None, rotation = 0):
        self._screen = screen

        self._xPos = xPos
        self._yPos = yPos
        self._rotation = rotation
        if (texture):
            self._texture = texture
        else:
            self._texture = pygame.image.load("default.png").convert()
            

        self.isRedrawNeeded = True
    
    def getPosition(self):
        return (self._xPos, self._yPos)
    
    def getXPosition(self):
        return self._xPos
    
    def getYPosition(self):
        return self._yPos
    
    def getRotation(self):
        return self._rotation

    def getTexture(self):
        return self._texture
    
    def setPosition(self, xPos, yPos):
        self._xPos = xPos
        self._yPos = yPos
        self.isRedrawNeeded = True
    
    def setXPosition(self, xPos):
        self._xPos = xPos
    
    def setYPosition(self, yPos):
        self._yPos = yPos
    
    def setRotation(self, rotation):
        self._rotation = rotation
        self._texture = pygame.transform.rotate(self._texture, self._rotation)
        self.isRedrawNeeded = True
    
    def update(self):
        pass
    
    def render(self):
        if (not self.isRedrawNeeded):
            return
        
        self._screen.blit(self._texture, (self._xPos, self._yPos))
        self.isRedrawNeeded = False

    def delete(self):
        self.isRedrawNeeded = True
        self._texture = pygame.image.load("default.png").convert()
        self._xPos = 0
        self._yPos = 0
        self.render()


class Snake(GameObject):
    def __init__(self, screen, startXPos, startYPos, snakeSpeed, snakeLength):
        super().__init__(screen, startXPos, startYPos)  
        
        self.__snakeLength = snakeLength

        x = startXPos
        y = startYPos
        self.__snakeSegments = [SnakeSegment(self._screen, x, y, texture="snakeHead.png")]
        for i in range(snakeLength):
            x -= 55
            self.__snakeSegments.append(SnakeSegment(self._screen, x, y, self.__snakeSegments[-1]))

        self.__snakeSpeed = snakeSpeed
        self.__snakeDirection = 1 # 0 = up, 1 = right, 2 = down, 3 = left
        
        self.__points = 0
        self.__isGameOver = False
        self.__gameOverScreen = None

        self.__pointsText = TextBox(self._screen, 0, 0, "Points: " + str(self.__points))


        self.__generateFruit()

        self.__isNewSegmentNeeded = False
    
    def getPoints(self):
        return self.__points

    def render(self):
        if (self.__isGameOver and self.__gameOverScreen != None):
            self.__gameOverScreen.render()
            return

        self.__fruit.render()
        for segment in self.__snakeSegments:
            segment.render()

        self.__pointsText.render()
    
    def update(self):
        self.__playerController()
        self.__checkCollision()
        self.__updatePlayground()
        
        return self.__isGameOver


    def __playerController(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (self.__snakeDirection != 0 and event.key == pygame.K_s or event.key == pygame.K_DOWN):
                    self.__snakeDirection = 2
                elif (self.__snakeDirection != 1 and event.key == pygame.K_a or event.key == pygame.K_LEFT):
                    self.__snakeDirection = 3
                elif (self.__snakeDirection != 2 and event.key == pygame.K_w or event.key == pygame.K_UP):
                    self.__snakeDirection = 0
                elif (self.__snakeDirection != 3 and event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                    self.__snakeDirection = 1
                elif(event.key == pygame.K_ESCAPE):
                    self.__isGameOver = True

        x = 0
        y = 0
        if (self.__snakeDirection == 0):
            y = -self.__snakeSpeed
        elif (self.__snakeDirection == 1):
            x = self.__snakeSpeed
        elif (self.__snakeDirection == 2):
            y = self.__snakeSpeed
        elif (self.__snakeDirection == 3):
            x = -self.__snakeSpeed
        
        self.__snakeSegments[0].rotate(self.__snakeDirection)
        for segment in self.__snakeSegments:
            segment.move(x, y)
    
    def __checkCollision(self):
        # Check if snake hit itself:
        if (len(self.__snakeSegments) > 3):
            for index in range(3, len(self.__snakeSegments)):
                if (self.__snakeSegments[0].getXPosition() == self.__snakeSegments[index].getXPosition() and self.__snakeSegments[0].getYPosition() == self.__snakeSegments[index].getYPosition()):
                    self.__isGameOver = True
                    return
        
        # Check if snake hit the wall:
        xMax = self._screen.get_width()
        yMax = self._screen.get_height()

        if (self.__snakeSegments[0].getXPosition() >= xMax or self.__snakeSegments[0].getXPosition() <= 0 or self.__snakeSegments[0].getYPosition() >= yMax or self.__snakeSegments[0].getYPosition() <= 0):
            self.__isGameOver = True
            return
        
        # Check if snake hit ate the fruit:
        if (abs(self.__fruit.getXPosition() - self.__snakeSegments[0].getXPosition()) <= Item.itemSizeRadius and abs(self.__fruit.getYPosition() - self.__snakeSegments[0].getYPosition()) <= Item.itemSizeRadius):
            self.__hasFruit = False
            self.__points += self.__fruit.getPoints()
            self.__pointsText.setText("Points: " + str(self.__points))
            self.__isNewSegmentNeeded = True

    def __updatePlayground(self):
        if (self.__isGameOver):
            self.__gameOverScreen = GameOverScreen(self._screen, self.__points)
            for segment in self.__snakeSegments:
                segment.delete()
            self.__fruit.delete()
            self.__snakeSegments = []
            self.__fruit = None


        if (not self.__hasFruit):
            self.__generateFruit()
        
        if (self.__isNewSegmentNeeded):
            xPos = self.__snakeSegments[-1].getXPosition()
            yPos = self.__snakeSegments[-1].getYPosition()

            if (self.__snakeDirection == 0):
                yPos -= 50
            elif (self.__snakeDirection == 1):
                xPos += 50
            elif (self.__snakeDirection == 2):
                yPos += 50
            elif (self.__snakeDirection == 3):
                xPos -= 50

            self.__snakeSegments.append(SnakeSegment(self._screen, xPos, yPos, self.__snakeSegments[-1]))
            self.__isNewSegmentNeeded = False
    
    def __checkItemPlacement(self, xPos, yPos):
        for segment in self.__snakeSegments:
            if (abs(segment.getXPosition() - xPos) <= Item.itemSize and abs(segment.getYPosition() - yPos) <= Item.itemSize):
                return False
        return True
    
    def __generateFruit(self):
        xMax = self._screen.get_width() - Item.itemSize
        yMax = self._screen.get_height() - Item.itemSize
        xPos = randrange(50, xMax, 15)
        yPos = randrange(50, yMax, 15)
            
        while (not self.__checkItemPlacement(xPos, yPos)):
             xPos = randrange(50, xMax, 15)
             yPos = randrange(50, yMax, 15)

        n = randrange(0, 30)
        if (n % 2 == 0):
            self.__fruit = Orange(self._screen, xPos, yPos)
        else:
            self.__fruit = Apple(self._screen, xPos, yPos)

        self.__hasFruit = True


class SnakeSegment(GameObject):
    segmentSize = 50
    segmentTexture = None

    def __init__(self, screen, xPos, yPos, nextSegment = None, texture = None, direction = 1):
        if (SnakeSegment.segmentTexture == None):
            SnakeSegment.segmentTexture = pygame.image.load("snake.png")
        
        if (texture == None):
            snakeTexture = SnakeSegment.segmentTexture
        else:
            snakeTexture = pygame.image.load(texture)

        super().__init__(screen, xPos, yPos, snakeTexture)

        self.__nextSegment = nextSegment
        self.__lastXPos = xPos
        self.__lastYPos = yPos
        self.__lastDirection = direction
        self.__lastRotation = 0
    
    def getNextSegment(self):
        return self.__nextSegment

    def getLastXPosition(self):
        return self.__lastXPos
    
    def getLastYPosition(self):
        return self.__lastYPos

    def getLastDirection(self):
        return self.__lastDirection
    
    def getLastRotation(self):
        return self.__lastRotation

    def move(self, x = 0, y = 0):
        self.__lastXPos = self.getXPosition()
        self.__lastYPos = self.getYPosition()

        if (x > 0):
            x += SnakeSegment.segmentSize
        elif (x < 0):
            x -= SnakeSegment.segmentSize

        if (y > 0):
            y += SnakeSegment.segmentSize
        elif (y < 0):
            y -= SnakeSegment.segmentSize

        if (self.__nextSegment != None):
            self.setPosition(self.__nextSegment.getLastXPosition(), self.__nextSegment.getLastYPosition())
            self.rotate(self.__nextSegment.getLastDirection())
        else:
            self.setPosition(self.getXPosition() + x, self.getYPosition() + y)
    
    def rotate(self, direction):
        if (direction == self.__lastDirection):
            return
        
        # Reset rotation to 0
        self.setRotation(-self.__lastRotation)

        if (direction == 0):
            rotation = 90
        elif (direction == 2):
            rotation = 270
        else:
            rotation = (direction - 1) * 90

        self.__lastDirection = direction
        self.__lastRotation = rotation
        self.setRotation(rotation)


class GameOverScreen(GameObject):
    def __init__(self, screen, points):
        texture = pygame.image.load("gameover.png")
        super().__init__(screen, 0, 0, texture)

        self.__gameOverText = TextBox(screen, screen.get_width() / 4.5, 100, "Game Over! Press esc to exit.", fontSize= 50)
        self.__pointsText = TextBox(screen, screen.get_width() / 4.5, 50, "Points: " + str(points), fontSize= 50)
    
    def render(self):
        self.isRedrawNeeded = True
        super().render()
        self.__gameOverText.render()
        self.__pointsText.render()

    def checkForInput(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    return True
            elif (event.type == pygame.QUIT):
                return True
        return False


class TextBox(GameObject):
    def __init__(self, screen, xPos, yPos, text, color = (0, 0, 0), font = "Arial", fontSize = 30, enableAA = True):
        texture = pygame.image.load("textbox.png")
        super().__init__(screen, xPos, yPos, texture)
        self.__color = color
        
        self.__enableAA = enableAA

        self.__font = pygame.font.SysFont(font, fontSize)
        self.__fontName = font
        self.__fontSize = fontSize

        self.__text = text
        self.__textBox = self.__font.render(text, enableAA, self.__color)

    def update(self):
        self.__textBox = self.__font.render(self.__text, self.__enableAA, self.__color)

    def render(self):
        self.isRedrawNeeded = True

        super().render()
        self._screen.blit(self.__textBox, (self.getXPosition(), self.getYPosition()))

    def setText(self, text):
        self.__text = text
        self.update()
        self.isRedrawNeeded = True
    
    def setColor(self, r, g, b):
        self.__color = (r, g, b)
        self.update()
        self.isRedrawNeeded = True

class Item(GameObject):
    itemSize = 50
    itemSizeRadius = itemSize / 2

    def __init__(self, screen, texture = None, xPos = 0, yPos = 0):
        self._points = 0
        super().__init__(screen, xPos, yPos, texture)

    def getPoints(self):
        return self._points

    def render(self):
        self.isRedrawNeeded = True
        super().render()

class Apple(Item): 
    def __init__(self, screen, xPos = 0, yPos = 0):
        texture = pygame.image.load("apple.png").convert()
        super().__init__(screen, texture, xPos, yPos)
        self._points = 2

class Orange(Item):
    def __init__(self, screen, xPos = 0, yPos = 0):
        texture = pygame.image.load("orange.png").convert()
        super().__init__(screen, texture, xPos, yPos)
        self._points = 4

class App:
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
    
    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 720))
        pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()
        self.running = True

        pygame.font.init()

        self.background = pygame.image.load("background.png")
        self.__snake = Snake(self.screen, 600, 600, 10, 5)
        self.__isGameOver = False

        self.__gameOverScreen = None

    def update(self):
        if (not self.__isGameOver):
            self.__isGameOver = self.__snake.update()
        
        if (self.__isGameOver):
            if (self.__gameOverScreen == None):
                self.__gameOverScreen = GameOverScreen(self.screen, self.__snake.getPoints())
            self.running = not self.__gameOverScreen.checkForInput()
        
        self.events()
    
    def events(self):
        pass

    def render(self):
        self.screen.blit(self.background, (0,0))
        
        if (not self.__isGameOver):
            self.__snake.render()
        else:
            self.__gameOverScreen.render()
        
        pygame.display.flip()
        self.clock.tick(9)

    def cleanUp(self):
        pass

if __name__ == "__main__":
    app = App()
    app.run()
