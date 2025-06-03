import pygame as pg
import sys, random,math
from pygame.locals import*
from math import *
from bird import bird

import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


        

largeur=1600#dimensions de la fenetre
hauteur=800

maxforce=.15
maxspeed=3  #10

Rsep=100
Rcoh=100
Rali=100

fsep=1
fcoh=1
fali=1
fsui=1


pg.init()
clock = pg.time.Clock()

nind=int(input("Nombre d'iindividus : "))
Flock=[]


Res_x=40
Res_y=40

noir=(0,0,0)
#definition de la grille pour la division spatial de bin-lattice

grid = [[] for _ in range(Res_x + 1)]
for i in range(Res_x + 1):
    grid[i] = [[] for _ in range(Res_y + 1)]



#Mise en place de la fenetre -------------------------------------------------------------

surface = pg.display.set_mode((largeur, hauteur))
pg.display.set_caption('Murmuration')
surface.fill((255,255,255))


#MIse en place des sliders ----------------------------------------------------------------

slider = Slider(surface, 1400, 100, 100, 10, min=0, max=5, step=0.1)
output = TextBox(surface, 1400, 115, 100, 15, fontSize=10)
slider.setValue(0.)

slider2 = Slider(surface, 1400, 150, 100, 10, min=0, max=5, step=0.1)
output2 = TextBox(surface, 1400, 165, 100, 15, fontSize=10)
slider2.setValue(0.)

slider3 = Slider(surface, 1400, 200, 100, 10, min=0, max=5, step=0.1)
output3 = TextBox(surface, 1400, 215, 100, 15, fontSize=10)
slider3.setValue(0.)

#chargement d'une police 
font = pg.font.SysFont(None, 15)


output.disable()  # Act as label instead of textbox

#debut du code
for i in range(nind):
    colonne=0
    ligne=0


    if i==1: 

        vx=random.randrange(1000)/1000*random.choice([-1,1])
        I=bird([vx,(1-vx**2)*random.choice([-1,1])],largeur,hauteur,maxforce,maxspeed,(255,0,0))

        colonne=int(I.position[0]/Res_x)
        ligne=int(I.position[1]/Res_y)

        grid[colonne][ligne].append(I)
    else :
        vx=random.randrange(1000)/1000*random.choice([-1,1])
        I=bird([vx,(1-vx**2)*random.choice([-1,1])],largeur,hauteur,maxforce,maxspeed,noir)

        colonne=int(I.position[0]/Res_x)
        ligne=int(I.position[1]/Res_y)

        grid[colonne][ligne].append(I)        


continuer = True #mise en place d'une boucle infini
while continuer:
    surface.fill((119, 181, 255))


    
    for k in range(0, len(grid) ):
        for j in range(0, len(grid[k])):
            for I in grid[k][j] :
                case=grid[k][j]


                #bird.apply_forces_s(I,case,Rcoh,Rsep,Rali,maxspeed,maxforce,fcoh,fsep,fali,fsui)
                bird.apply_forces(I,case,Rcoh,Rsep,Rali,maxspeed,maxforce,fcoh,fsep,fali)
                #bird.apply_forces_evite(I,case,Rcoh,Rsep,Rali,maxspeed,maxforce,fcoh,fsep,fali,fsui)

                bird.maj(I,largeur,hauteur)
                bird.affiche(I,surface,largeur,hauteur)

                grid[k][j].remove(I)

                # Calculer la nouvelle colonne et ligne pour l'oiseau
                colonne = int(I.position[0] / Res_x)
                ligne = int(I.position[1] / Res_y)

                # Ajouter l'oiseau à la nouvelle case
                grid[colonne][ligne].append(I)
    





    for event in pg.event.get():
        if event.type==QUIT:
            continuer = False

    clock.tick(60)
#recup des sliders-----------------------
    output.setText(slider.getValue())   
    output2.setText(slider2.getValue()) 
    output3.setText(slider3.getValue()) 
                                        
    fsep=slider.getValue()              
    fcoh=slider2.getValue()             
    fali=slider3.getValue()                         

    label1 = font.render("Cohesion", True, (0, 0, 0))
    surface.blit(label1, (1400, 90))

    label2 = font.render("Separation", True, (0, 0, 0))
    surface.blit(label2, (1400, 140))

    label3 = font.render("Alignment", True, (0, 0, 0))
    surface.blit(label3, (1400, 190))
  
                                        
    pygame_widgets.update(event)        
#----------------------------------------
    pg.display.update()
pg.quit()
