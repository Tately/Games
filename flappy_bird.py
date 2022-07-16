# extensions : background image, bird image, pipes image, infinite game
import pygame
import random

class Pips:
    pD = pygame.transform.scale(pygame.image.load("pD.png"), (100,500))
    pU = pygame.transform.scale(pygame.image.load("pU.png"), (100,500))

    def __init__(self):
        upperPipes = [pygame.Rect(300+i*300, random.randint(-300,-233), 100, 500) for i in range(3)]
        lowerPipes = [pygame.Rect(480 +i*310, random.randint(400,533), 100, 500) for i in range(2)]
        self.pipes = upperPipes + lowerPipes
        self.gameDone = False

    def update(self):
        if self.gameDone:
            upperPipes = [pygame.Rect(300+i*300, random.randint(-300,-233), 100, 500) for i in range(3)]
            lowerPipes = [pygame.Rect(480+i*310, random.randint(400,533), 100, 500) for i in range(2)]
            self.pipes = upperPipes + lowerPipes
            self.gameDone = False

    def render(self,screen):
        for i, pipe in enumerate(self.pipes):
            if i < 3:
                screen.blit(self.pU, pipe)
            else:
                screen.blit(self.pD, pipe)

class Bird:
    def __init__(self):
        self.bird = pygame.Rect(40, 350, 40, 40)
        self.speed = 0
        self.birdpic = pygame.image.load("bir.png")
        self.birdpic = pygame.transform.scale(self.birdpic, (40,40))

    def jump(self):
        self.speed = 14 

    def update(self):
        self.bird.move_ip(2,(4-(self.speed)))
        if self.speed >= 0 :
            self.speed -= 2
        else:
            self.speed -=1
    
    def render(self, screen):
        screen.blit(self.birdpic, self.bird)


class App:
    
    background = pygame.transform.scale(pygame.image.load("bg.png"), (1200,700))

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        pygame.init()
        self.fBird = None
        self.fPipes = None
        

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Flappy bird")
        self.fBird = Bird()
        self.fPipes = Pips()
        self.clock = pygame.time.Clock()
        self.running = True 
 
    def update(self):
        if self.fBird.bird.top < 0 or self.fBird.bird.top > 666 or any([self.fBird.bird.colliderect(rect) for rect in self.fPipes.pipes]):
            self.running = False
        if self.fBird.bird.left > 1180:
            self.fBird.bird.update(pygame.Rect(-20, self.fBird.bird.top, 40, 40)) 
            self.fPipes.gameDone = True
        self.events()
        self.fPipes.update()
        self.fBird.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE] or mouse[0]:  
            self.fBird.jump()


    def render(self):
        self.screen.blit(self.background, (0,0))
        self.fBird.render(self.screen)
        self.fPipes.render(self.screen)
        pygame.display.flip()
        self.clock.tick(60)


    def cleanUp(self):
        pass

if __name__ == "__main__":
    app = App()
    app.run()