import pygame

class Button:
    def __init__(self, surface, text, color, highlightColor, width, height, x, y, function=None, params=None):
        pygame.init()
        self.surface = surface
        self.text = text
        self.color = color
        self.highlightColor = highlightColor
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.function = function
        self.params = params

    def drawButton(self):
        color = self.highlightColor if self.isMouseOverButton() else self.color

        pygame.draw.rect(self.surface, (0,0,0), (self.x-2, self.y-2, self.width+4, self.height+4))
        pygame.draw.rect(self.surface, color, (self.x, self.y, self.width, self.height))

        self.display(self.surface, self.text,20 , (0,0,0))

    def isMouseOverButton(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX >= self.x and mouseX <= self.x + self.width and mouseY >= self.y and mouseY <= self.y + self.height:
            return True

        return False

    def onClick(self):
        if self.function:
            if self.params:
                self.function(self.params)
            else:
                self.function()


    def display(self, screen, text, fontSize, color):
        font = pygame.font.SysFont("arial", fontSize)
        text = font.render(str(text), True, color)
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))



