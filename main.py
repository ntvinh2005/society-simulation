import pygame
import random
import os
from math import *


from object import Nation, Map, player_addfood, player_addmonster

WIDTH, HEIGHT=1200, 600
WIN=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity")


WHITE=(0, 0, 0)
BLACK=(225, 255, 255)
RED=(255,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)


FPS=120


def draw_window(nation, map):
    WIN.fill(BLACK)
    for nation in map.nations:
        for nest in nation.nests:
            nest.draw()
            for ant in nest.swarm:
                ant.draw()
    for food in map.foods:
        food.draw()
    
    for monster in map.monsters:
        monster.draw()
    pygame.display.update()



def main():    
    clock=pygame.time.Clock()
    run=True
    count=0

    map=Map()
    map.add_nations(1)
    map.add_nations(2)
    map.add_nations(3)
    map.add_nations(4)
    for nation in map.nations:
        for enemy_nation in map.nations:
            if nation!=enemy_nation:
                nation.enemies.append(enemy_nation)
    for nation in map.nations:
        nation.build_nest(random.randrange(0, WIDTH),random.randrange(0, HEIGHT))

    while run:
        clock.tick(FPS)
  
    #event    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                (x,y)=pygame.mouse.get_pos()
                player_addfood(map)
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_a:
                    player_addmonster(map)

        for nation in map.nations:
            for nest in nation.nests:
                nest.find_attacker(nation)
                if len(nest.swarm)==0:
                    nest.add_ant()
                if nest.radius<=5:
                    nation.nests.remove(nest)
                for ant in nest.swarm:
                    ant.escape(map)
                    if ant.fear == False:
                        if ant.full==False:
                            ant.find_food(map)
                        ant.move()
                        ant.eat(map, nation)
                        ant.attack(nation)
                        if ant.full==True:
                            ant.return_home(nest)
                        if ant.size<=3:
                            nest.swarm.remove(ant)
                    else:
                        ant.move()
                    
        for monster in map.monsters:
            monster.hunt(map)
            monster.move()
            monster.eat(map)
            if monster.radius <= 5:
                map.monsters.remove(monster)

        count+=1
        if count%15==0:
            map.add_food()

        draw_window(nation, map)
        
    pygame.quit() 
    
    
if __name__=="__main__":
    main()