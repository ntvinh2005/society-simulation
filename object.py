import pygame
import random
import os
from math import *

WIDTH, HEIGHT=1200, 600
WIN=pygame.display.set_mode((WIDTH, HEIGHT))

YELLOW=(255,255,0)
GREEN=(0,255,0)
RED=(255,0,0)
BLACK=(0,0,0)


def player_addfood(map):
    for i in range(5):
        (pos_x,pos_y)=pygame.mouse.get_pos()
        x=random.randrange(pos_x-100, pos_x+100)
        y=random.randrange(pos_y-100, pos_y+100)
        food=Food(x,y)
        map.foods.append(food)

def player_addmonster(map):
    (pos_x, pos_y) = pygame.mouse.get_pos()
    monster = Monster(pos_x, pos_y)
    map.monsters.append(monster)

class Map:
    def __init__(self):
        self.foods=[]
        self.nations=[]
        self.monsters = []

    def add_food(self):
        x=random.randrange(0, WIDTH)
        y=random.randrange(0, HEIGHT)
        food=Food(x,y)
        self.foods.append(food)
    
    def add_nations(self, order):
        nation=Nation(order)
        self.nations.append(nation)


class Nation:
    def __init__(self, order):
        self.nests=[]
        print(order)
        if order==1:
            self.color=RED
        elif order==2:
            self.color=YELLOW
        elif order==3:
            self.color=BLACK
        elif order==4:
            self.color=(0,0,255)
        self.enemies=[]

    def build_nest(self, x, y):
        nest=Nest(x , y, 20, self.color)
        self.nests.append(nest)
        nest.add_ant()

class Nest:
    def __init__(self, x, y, radius, color):
        self.x=x
        self.y=y
        self.radius=radius
        self.swarm=[]
        self.nationality=color
        (R,G,B)=color
        self.color=(abs(R-100), abs(G-100), abs(B-100))
        self.vision=self.radius+100
        self.enemies=[]
    
    def add_ant(self):
        ant=Ant(self.x, self.y, self.nationality)
        self.swarm.append(ant)

    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.radius)
    
    def find_attacker(self, nation):
        self.enemies=[]
        for enemy in nation.enemies:
            for nest in enemy.nests:
                for enemy_ant in nest.swarm:
                    if sqrt((enemy_ant.x-self.x)**2+(enemy_ant.y-self.y)**2)<=self.vision:
                        self.enemies.append(enemy_ant)
                        for ant in self.swarm:
                            ant.attack_mode=True
                            ant.defend(nest)
        if self.enemies==[]:
            for ant in self.swarm:
                ant.attack_mode=False

class Ant:
    def __init__(self,x,y, color):
        self.x=x
        self.y=y
        self.size=10
        self.size_limit=15
        self.color=color
        self.target_x=x
        self.target_y=y
        self.vision=self.size+200
        self.full=False
        self.attack_mode=False
        self.fear=False

    def find_food(self, map):
        min_distance=100000
        for food in map.foods:
            if sqrt((self.x-food.x)**2+(self.y-food.y)**2)<min_distance:
                min_distance=sqrt((self.x-food.x)**2+(self.y-food.y)**2)
                self.target_x=food.x
                self.target_y=food.y

    def move(self):
        angle=0
        if self.target_x-self.x !=0:
            angle=atan((self.target_y-self.y)/(self.target_x-self.x))*180/pi
            if self.fear == False:
                self.x+=2*cos(angle)
                self.y+=2*sin(angle)
            else:
                self.x-=2*cos(angle)
                self.y-=2*sin(angle)
        else:
            if self.target_y-self.y>0:
                if self.fear == False:
                    self.y+=2
                else:
                    self.y-=2
            elif self.target_y-self.y<0:
                if self.fear == False:
                    self.y-=2
                else:
                    self.y+=2
        if sqrt((self.target_x-self.x)**2+(self.target_y-self.y)**2)<40 and self.fear == False:
                self.x+=(self.target_x-self.x)/10
                self.y+=(self.target_y-self.y)/10

    def draw(self):
        if self.full==False:
            pygame.draw.circle(WIN, self.color, (self.x, self.y), self.size)
        else:
            pygame.draw.circle(WIN, self.color, (self.x, self.y), self.size)
            pygame.draw.circle(WIN, GREEN, (self.x, self.y), 5)

    def eat(self, map, nation):
        for food in map.foods:
            if sqrt((self.x-food.x)**2+(self.y-food.y)**2)<=self.size:
                map.foods.remove(food)
                if self.size<self.size_limit:
                    self.size+=0.5
                if self.size==self.size_limit:
                    nation.build_nest(self.x, self.y)
                    for nest in nation.nests:
                        for ant in nest.swarm:
                            if self==ant:
                                nest.swarm.remove(ant)          
                self.full=True
    
    def return_home(self, nest):
        self.target_x=nest.x
        self.target_y=nest.y
        if sqrt((self.x-nest.x)**2+(self.y-nest.y)**2)<=nest.radius:
            self.full=False
            if nest.radius<80:
                nest.radius+=0.2
                if len(nest.swarm)<int(nest.radius/5):
                    nest.add_ant()

    def defend(self, nest):
        self.attack_mode=True
        min_distance=100000
        self.return_home
                

    def attack(self, nation):
        for enemy in nation.enemies:
            for nest in enemy.nests:
                if sqrt((nest.x-self.x)**2+(nest.y-self.y)**2)<=self.vision+nest.radius:
                    self.attack_mode=True
                    self.target_x=nest.x
                    self.target_y=nest.y
                if sqrt((nest.x-self.x)**2+(nest.y-self.y)**2)<=self.size+nest.radius:   
                    nest.radius-=0.2
                    self.size-=0.5
                for ant in nest.swarm:
                    if sqrt((ant.x-self.x)**2+(ant.y-self.y)**2)<=ant.size+self.size:
                        ant.size-=0.2
                        self.size-=0.2

    def escape(self, map):
        self.fear = False
        for monster in map.monsters:
            if sqrt((self.x-monster.x)**2+(self.y-monster.y)**2)<self.vision:
                self.target_x=monster.x
                self.target_y=monster.y
                self.fear = True
        

class Food:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.radius=5

    def draw(self):
        pygame.draw.circle(WIN, GREEN, (self.x, self.y), self.radius)

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.radius = 15
        self.limit = 30
    
    def draw(self):
        pygame.draw.circle(WIN, (175, 132, 189), (self.x, self.y), self.radius)

    def hunt(self, map):
        min_distance=100000
        for nation in map.nations:
            for nest in nation.nests:
                for ant in nest.swarm:
                    if sqrt((self.x-ant.x)**2+(self.y-ant.y)**2)<min_distance:
                        min_distance=sqrt((self.x-ant.x)**2+(self.y-ant.y)**2)
                        self.target_x=ant.x
                        self.target_y=ant.y

    def move(self):
        angle=0
        self.radius -= 0.01
        if self.target_x-self.x !=0:
            angle=atan((self.target_y-self.y)/(self.target_x-self.x))*180/pi
            self.x+=2*cos(angle)
            self.y+=2*sin(angle)
        else:
            if self.target_y-self.y>0:
                self.y+=1
            elif self.target_y-self.y<0:
                self.y-=1
        if sqrt((self.target_x-self.x)**2+(self.target_y-self.y)**2)<40:
            self.x+=(self.target_x-self.x)/100
            self.y+=(self.target_y-self.y)/100
    
    def eat(self, map):
        for nation in map.nations:
            for nest in nation.nests:
                for ant in nest.swarm:
                    if sqrt((self.x - ant.x)**2 + (self.y - ant.y)**2) <= ant.size + self.radius and self.radius < self.limit:
                        nest.swarm.remove(ant)
                        if self.radius <= self.limit:
                            self.radius += 0.2
                if sqrt((self.x - nest.x)**2 + (self.y - nest.y)**2) <=nest.radius + self.radius:
                    nest.radius -= 1
                    self.radius += 0.2
                    

        