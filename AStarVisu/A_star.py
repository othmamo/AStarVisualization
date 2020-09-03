import math
import pygame
import random
import time
from pygame.locals import *

pygame.init()

height=700
width=1000
size_of_cell=20
sizeX=int(width/size_of_cell)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
grid=[]
start=None
end=None
launch = False

class Node():
    def __init__(self, x=0, y=0, g=0, h=0):
        self.obstacle=False
        self.g=g
        self.x=x
        self.y=y
        self.h=h
        self.f=self.g+self.h
        self.parent=None


def init_grid(sizeX):
    L=[]
    for i in range(sizeX):
        L.append([])
        for j in range(sizeX):
            L[i].append(Node(i,j))
    return L

def lowest_cost(L):
    if(L==[]):
        return None
    res=L[0]
    index=0
    for i in range(len(L)):
        if(L[i].f<res.f):
            index=i
            res=L[i]
    L.pop(index)
    return res

def path(node):
    res=[]
    while(node):
        res.append((node.x,node.y))
        node=node.parent
    return res

def draw_grid():
    for i in range(sizeX):
        for j in range(sizeX):
            pygame.draw.rect(screen, (170,170,170), (size_of_cell*j,size_of_cell*i,size_of_cell, size_of_cell),1)

def draw_path(L):
    for i in L:
        draw_rect(i[0], i[1], (255,0,0))

def draw_rect(x,y,color):
    pygame.draw.rect(screen, color, (x*size_of_cell+1,y*size_of_cell+1,size_of_cell-2, size_of_cell-2))
    pygame.display.flip()

def draw_list(L,color):
    for i in L:
        draw_rect(i.x,i.y,color)

def a_star(L, start, end):
    toOpen=[]
    closed=[]
    toOpen.append(start)
    while(len(toOpen)!=0):
        current=lowest_cost(toOpen)
        closed.append(current)
        draw_rect(current.x, current.y, (227, 241, 63))
        if(current==end):
            return path(current)
        for i in range(-1,2):
            for j in range(-1,2):
                if ((i!=0 or j!=0) and 0<=i+current.x<len(L) and 0<=j+current.y<len(L[0])):
                    if(not close()):
                        return False
                    node=L[i+current.x][j+current.y]
                    if (node.obstacle==True or node in closed):
                        continue
                    h=int(10*math.sqrt(abs(node.x-end.x)**2+abs(node.y-end.y)**2))
                    g=current.g+(14 if abs(i)==abs(j) else 10)
                    f=h+g
                    if(node not in toOpen or node.g>g):
                        node.parent=current
                        node.h=h
                        node.g=g
                        node.f=h+g
                        if node not in toOpen:
                            draw_rect(node.x, node.y, (0,255,0))
                            toOpen.append(node)
def close():
    global launch, start, end
    for event in pygame.event.get():
        if event.type == KEYDOWN:
                if event.key == K_SPACE and start!=None and end!=None:
                    launch=True
                elif(event.key == K_BACKSPACE):
                    restart()
        elif event.type == QUIT:
            return False

    return True

def user_input():
    global start, end
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        x=int(pos[0]//size_of_cell)
        y=int(pos[1]//size_of_cell)
        if(start==None):
            start=(x,y)
            draw_rect(x,y,(0,0,255))
        elif(end==None and (x,y)!=start):
            end=(x,y)
            draw_rect(x,y,(0,0,255))
        elif((x,y)!=start and (x,y)!=end):
            grid[x][y].obstacle=True
            draw_rect(x,y,(0,0,0))

def restart():
    global grid, end, start
    screen.fill((255,255,255))
    start=None
    end=None
    grid.clear
    grid=init_grid(sizeX)
    draw_grid()

restart()
while(close()):
    if(launch):
        L=a_star(grid, grid[start[0]][start[1]], grid[end[0]][end[1]])
        if(L==False):
            break
        draw_path(L)
        launch=False
    user_input()
    pygame.display.flip()


pygame.quit()
