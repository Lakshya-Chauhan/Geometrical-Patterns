import time
from random import random
import pygame
from os import system
frameRate = 600
dt = 1/600
FoNt = 0
FoNtprint = 0
GREEN = (25, 187, 86)
lightGREEN = (25-10, 187-30, 86-20)
screen_res = (1920, 1080)
mcolor = [128, 128, 128]
mrad = (sum(screen_res))/30
class sphere:
    def __init__(self, position : list, radius : float, velocity, number : int, color : list):
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.radius = radius
        self.vel = pygame.math.Vector2(velocity[0], velocity[1])
        self.n = number
        self.color = color
    
    def update(self, dt):

        if self.vel.magnitude() > 50:
            self.vel = pygame.math.Vector2(50).rotate(pygame.math.Vector2(50).angle_to(self.vel))

        if self.pos[0] > screen_res[0]-10:
            self.pos[0] = screen_res[0]-11
            self.vel[0] = -self.vel[0]
        elif self.pos[0] < 10:
            self.pos[0] = 11
            self.vel[0] = -self.vel[0]
        
        if self.pos[1] > screen_res[1]-10:
            self.pos[1] = screen_res[1]-11
            self.vel[1] = -self.vel[1]
        elif self.pos[1] < 10:
            self.pos[1] = 11
            self.vel[1] = -self.vel[1]

        self.pos += self.vel*dt

    def is_colliding(obj1, obj2):
        return True if (sphere.distance(obj1.pos, obj2.pos) < obj1.radius + obj2.radius) else False

    def distance(point1 : list, point2 : list):
        if min([len(point1), len(point2)]) == 2:
            return ((((point1[0]-point2[0])**2) + ((point1[1] - point2[1])**2))**0.5)
        
        else:
            return ((((point1[0]-point2[0])**2) + ((point1[1] - point2[1])**2) + ((point1[2] - point2[2])**2))**0.5)

def cls():
    system("cls")
def font(a:str,b=18):
    global FoNt
    FoNt = pygame.font.SysFont(a,b)
def printpy(x:str,a=(100,400),y=(128,128,128)):
    global FoNt,FoNtprint
    FoNtprint = FoNt.render(x,True,y)
    screen.blit(FoNtprint,a)
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_res = [screen.get_width(), screen.get_height()]
pygame.display.set_caption("Random Geometrical Patterns")
cls()
OBJS = list()
for _ in range(50):
# for _ in range(30):
    OBJS.append( sphere([random()*screen_res[0], random()*screen_res[1]], random()*(sum(screen_res))/10, [(0.5-random())*8, (0.5-random())*8], _, [random()*256, random()*256, random()*256]) )
    # OBJS.append( sphere([random()*800, random()*800], random()*200, [(0.5-random())*2, (0.5-random())*2], _, [random()*256, random()*256, random()*256]) )
running = True
clock = pygame.time.Clock()
rectangle = pygame.Surface(screen_res)
rectangle.set_alpha(50)
rectangle.fill((0, 0, 0))
while running == True:
    clock.tick(frameRate)
    initTime = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(rectangle, (0, 0))
    surface1 = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    mpos = pygame.mouse.get_pos()
    mrad += (1 - random())
    mrad = ((sum(screen_res))/20) if mrad > ((sum(screen_res))/20) else ( ((sum(screen_res))/60) if mrad < ((sum(screen_res))/60) else mrad)
    mcolor = (mcolor[0]+(0.5-random()), mcolor[1]+(0.5-random()), mcolor[2]+(0.5-random()))
    mcolor = (255 if mcolor[0] > 255 else (0 if mcolor[0] < 0 else mcolor[0]), 255 if mcolor[1] > 255 else (0 if mcolor[1] < 0 else mcolor[1]), 255 if mcolor[2] > 255 else (0 if mcolor[2] < 0 else mcolor[2]))

    for circle in OBJS:
        if sphere.distance(circle.pos, mpos) < circle.radius + mrad:
            pygame.draw.line(surface1, [(circle.color[0]+mcolor[0])/2, (circle.color[1]+mcolor[1])/2, (circle.color[2]+mcolor[2])/2, (1-((sphere.distance(circle.pos, mpos))/(mrad + circle.radius)))*255], circle.pos[:2], mpos[:2])
            pygame.draw.circle(surface1, list(circle.color)+[(1-((sphere.distance(circle.pos, mpos))/(mrad + circle.radius)))*255], circle.pos[:2], 1)
            pygame.draw.circle(surface1, list(mcolor)+[(1-((sphere.distance(circle.pos, mpos))/(mrad + circle.radius)))*255], mpos[:2], 1)

        for circle2 in OBJS:
            if circle.n != circle2.n:
                if sphere.is_colliding(circle, circle2):
                    pygame.draw.line(surface1, [(circle.color[0]+circle2.color[0])/2, (circle.color[1]+circle2.color[1])/2, (circle.color[2]+circle2.color[2])/2, (1-((sphere.distance(circle.pos, circle2.pos))/(circle2.radius + circle.radius)))*255], circle.pos[:2], circle2.pos[:2])
                    pygame.draw.circle(surface1, list(circle.color)+[(1-((sphere.distance(circle.pos, circle2.pos))/(circle2.radius + circle.radius)))*255], circle.pos[:2], 1)
                    pygame.draw.circle(surface1, list(circle2.color)+[(1-((sphere.distance(circle.pos, circle2.pos))/(circle2.radius + circle.radius)))*255], circle2.pos[:2], 1)

        circle.vel[0] += (0.5-random())*120*dt*2
        circle.vel[1] += (0.5-random())*120*dt*2
    
        circle.update(dt)
    screen.blit(surface1, (0, 0))
    pygame.display.update()
    endTime = time.time()
    dt = endTime-initTime
    if dt != 0:
        frameRate = 1/dt
    else:
        frameRate = 1000
