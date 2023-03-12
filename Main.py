import pygame
pygame.init()
import random
import math

class TreeTemplate:
    def __init__(self, widthIncrease, angleSpan, randomAngleOffset, randomWidthOffset, maxBaseBranches, maxBranches, branchDensity, buffed, width, leafSize, treeColor, leafColor):
        self.widthIn = widthIncrease
        self.angleSpan = angleSpan
        self.randomAngle = randomAngleOffset
        self.randomWidth = randomWidthOffset

        self.maxBaseBranches = maxBaseBranches
        self.maxBranches = maxBranches
        self.branchAmount = branchDensity

        self.buffed = buffed
        self.width = width
        self.leafSize = leafSize

        self.treeColor = treeColor
        self.leafColor = leafColor

treeTemp = TreeTemplate(widthIncrease=0.7, angleSpan=1.5, randomAngleOffset=0.3, randomWidthOffset=0.5,
                        maxBaseBranches=4, maxBranches=5, branchDensity=0.2, buffed=True, width=0.3, leafSize=6,
                        treeColor=(200, 64, 64), leafColor=(0, 225, 50))

class Tree:
    def __init__(self, template, width=None, startPos=pygame.Vector2(), endPos=None, generation=0):
        self.template = template
        self.startPos = startPos
        self.endPos = endPos or pygame.Vector2(y=-1)
        self.width = width or self.template.width
        self.generation = generation
        self.children = []

        # if you are creating a brand new tree
        if generation == 0:
            branchAmount = random.randint(1, self.template.maxBaseBranches)

            for i in range(branchAmount):
                self.generate_random_branch(branchAmount, i + 1)

    def draw(self, win, pos, size):
        color = self.template.treeColor if self.children else self.template.leafColor
        width = round(self.width * size) if self.children else round(self.width * size * self.template.leafSize)

        pygame.draw.line(win, color, pos + self.startPos * size, pos + self.endPos * size, width)
        for child in self.children:
            child.draw(win, pos, size)

    def get_branch_amount(self):
        gen = self.generation

        chance = random.random()
        exp = 1 / gen if self.template.buffed else gen
        chance = math.pow(chance, exp)

        return min(math.floor(chance / self.template.branchAmount), 3)

    def generate_random_branch(self, branchAmount, branch):
        startP = self.endPos
        newWidth = self.width * self.template.widthIn * random.uniform(1 - self.template.randomWidth, 1 + self.template.randomWidth)
        newLength = (self.startPos - startP).magnitude() * self.template.widthIn

        angle = (math.pi + self.template.angleSpan) / (branchAmount + 1)
        direction = angle * branch + math.pi / 2 - self.template.angleSpan / 2 + random.uniform(-self.template.randomAngle, self.template.randomAngle)

        endPos = pygame.Vector2(x=math.sin(direction), y=math.cos(direction)) * newLength

        newBranch = Tree(self.template, newWidth, startP, startP + endPos, self.generation+1)
        self.children.append(newBranch)

        branchAmount = newBranch.get_branch_amount()
        if newBranch.generation >= self.template.maxBranches:
            return

        for i in range(branchAmount):

            newBranch.generate_random_branch(branchAmount, i + 1)



class Main:
    def __init__(self):
        self.winSize = (1280, 720)
        self.win = pygame.display.set_mode(self.winSize)

    def loop(self):
        plant = Tree(treeTemp)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        plant = Tree(treeTemp)

                    if event.key == pygame.K_ESCAPE:
                        quit()

            self.win.fill((0, 0, 0))
            plant.draw(self.win, pos=pygame.Vector2(x=500, y=720), size=250)
            pygame.display.update()


Main().loop()
