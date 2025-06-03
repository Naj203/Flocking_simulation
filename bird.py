import pygame as pg
import sys, random,math
from pygame.locals import*
from math import *


class bird:
    position=[0,0]
    vitesse=[0,0]
    acceleration=[0,0]

    
    maxforce=0.1
    maxspeed=2

    col=(0,0,0)

    def __init__(self,vitesse,largeur,hauteur,maxforce,maxspeed,col):
        self.position=[random.randrange(largeur),random.randrange(hauteur)]
        self.vitesse=vitesse
        self.acceleration=[0,0]
        self.maxforce=maxforce
        self.maxspeed=maxspeed
        self.col=col#(random.randrange(255),random.randrange(255),random.randrange(255))


#Met à jours les positions et vitesse du boid
    def maj(I,largeur,hauteur):
        I.vitesse[0]=I.vitesse[0]+I.acceleration[0]
        I.vitesse[1]=I.vitesse[1]+I.acceleration[1]
        #limitation en vitesse
        vn=sqrt((I.vitesse[0]**2)+(I.vitesse[1]**2))
        if vn>I.maxspeed:
            I.vitesse[0]=I.maxspeed*I.vitesse[0]/vn
            I.vitesse[1]=I.maxspeed*I.vitesse[1]/vn

        I.position[0]=I.position[0]+I.vitesse[0]
        I.position[1]=I.position[1]+I.vitesse[1]

        I.acceleration[0]=I.acceleration[0]*0
        I.acceleration[1]=I.acceleration[1]*0


        if I.position[0] > largeur:
            I.position[0] =0
            
        if I.position[0]< 0:
            I.position[0] =largeur
            
        if I.position[1] >= hauteur:
            I.position[1] =0
            
        if I.position[1] < 0:
            I.position[1] =hauteur
        return(I)

#Met à jours les positions et vitesse du boid en les faisant rebondir aux bordures
    def maj_rebond(I,largeur,hauteur):
        I.vitesse[0]=I.vitesse[0]+I.acceleration[0]
        I.vitesse[1]=I.vitesse[1]+I.acceleration[1]
        #limitation en vitesse
        vn=sqrt(I.vitesse[0]**2+I.vitesse[1]**2)
        if vn>I.maxspeed:
            I.vitesse[0]=I.maxspeed*I.vitesse[0]/vn
            I.vitesse[1]=I.maxspeed*I.vitesse[1]/vn

        I.position[0]=I.position[0]+I.vitesse[0]
        I.position[1]=I.position[1]+I.vitesse[1]

        I.acceleration[0]=I.acceleration[0]*0
        I.acceleration[1]=I.acceleration[1]*0


        if I.position[0] > largeur or I.position[0]< 0 :
            I.vitesse[0] =-I.vitesse[0]

        if I.position[1] > hauteur or I.position[1]< 0 :
            I.vitesse[1] =-I.vitesse[1]  
 
        return(I)
#applique une force sur le boid I 
    def appliquer_force(I,force):
        I.acceleration[0]=I.acceleration[0]+force[0]
        I.acceleration[1]=I.acceleration[1]+force[1]
        return(I)
#Fait suivre la cible [x,y] par le boid I :
    def suivre(I,cible):

        Vvoulue=[0,0]

        
        Vvoulue[0]=cible[0]-I.position[0]
        Vvoulue[1]=cible[1]-I.position[1]
        if Vvoulue!=[0,0]:
            Vvoulue[0]=Vvoulue[0]/(sqrt(Vvoulue[0]**2+Vvoulue[1]**2))
            Vvoulue[1]=Vvoulue[1]/(sqrt(Vvoulue[0]**2+Vvoulue[1]**2))
        
            Vvoulue[0]=Vvoulue[0]*I.maxspeed
            Vvoulue[1]=Vvoulue[1]*I.maxspeed

            
            

        Steer=[0,0]
        Steer[0]=Vvoulue[0]-I.vitesse[0]
        Steer[1]=Vvoulue[1]-I.vitesse[1]

        
        sm=sqrt(Steer[0]**2+Steer[1]**2)
        if sm>I.maxforce:
            Steer[0]=Steer[0]*I.maxforce/sm
            Steer[1]=Steer[1]*I.maxforce/sm

            
            
        #I=bird.appliquer_force(I,Steer)
        return(Steer)


    def eviter(I,cible):

        Vvoulue=[0,0]

        
        Vvoulue[0]=cible[0]-I.position[0]
        Vvoulue[1]=cible[0]-I.position[1]
        if Vvoulue!=[0,0]:
            Vvoulue[0]=Vvoulue[0]/(sqrt(Vvoulue[0]**2+Vvoulue[1]**2))
            Vvoulue[1]=Vvoulue[1]/(sqrt(Vvoulue[0]**2+Vvoulue[1]**2))
        
            Vvoulue[0]=Vvoulue[0]*I.maxspeed
            Vvoulue[1]=Vvoulue[1]*I.maxspeed

            
            

        Steer=[0,0]
        Steer[0]=Vvoulue[0]-I.vitesse[0]
        Steer[1]=Vvoulue[1]-I.vitesse[1]

        
        sm=sqrt(Steer[0]**2+Steer[1]**2)
        if sm>I.maxforce:
            Steer[0]=-Steer[0]*I.maxforce/sm
            Steer[1]=-Steer[1]*I.maxforce/sm
            
        #I=bird.appliquer_force(I,Steer)
        return(Steer)

#affiche le boid I

    def affiche(I,surface,largeur,hauteur):
        pg.draw.rect(surface,I.col,(I.position[0],I.position[1],2,2))
        



#calcul la disatnce entre A et B :
    def dist(A,B):
        ab=[abs(A.position[0]-B.position[0]),abs(A.position[1]-B.position[1])]
        dist=sqrt(ab[0]**2+ab[1]**2)
        return(dist)
#Gerer la condition de séparation :
    def separer(I,groupe,Rsep,maxspeed,maxforce):
        d=0
        diff=[0,0]
        c=0
        somme=[0,0]
        Steer=[0,0]
        sm=0
        for J in groupe:
            
            d=bird.dist(I,J)
            if d<Rsep and d>0:
                c+=1
                diff=[I.position[0]-J.position[0],I.position[1]-J.position[1]]
                ndiff=sqrt(diff[0]**2+diff[1]**2)
                diff=[diff[0]/ndiff,diff[1]/ndiff]
                somme=[somme[0]+diff[0],somme[1]+diff[1]]
                
        if c>0:
            somme=[somme[0]/c,somme[1]/c]
            somme=[somme[0]*maxspeed,somme[1]*maxspeed]    
            Steer=[somme[0]-I.vitesse[0],somme[1]-I.vitesse[1]]


        sm=sqrt(Steer[0]**2+Steer[1]**2)
        if sm>I.maxforce:
            Steer[0]=-Steer[0]*I.maxforce/sm
            Steer[1]=-Steer[1]*I.maxforce/sm
            
        #I=bird.appliquer_force(I,Steer)
        return(Steer)

#S'occupe de la cohesion des boids
    def cohesion(I,groupe,Rcoh,maxspeed,maxforce):
        d=0
        diff=[0,0]
        c=0
        somme=[0,0]
        Steer=[0,0]
        sm=0
        for J in groupe:
            
            d=bird.dist(I,J)
            if d<Rcoh and d>0:
                c+=1
                diff=[I.position[0]-J.position[0],I.position[1]-J.position[1]]
                ndiff=sqrt(diff[0]**2+diff[1]**2)
                diff=[diff[0]/ndiff,diff[1]/ndiff]
                somme=[somme[0]+diff[0],somme[1]+diff[1]]
                
        if c>0:
            somme=[somme[0]/c,somme[1]/c]
            somme=[somme[0]*maxspeed,somme[1]*maxspeed]    
            Steer=[somme[0]-I.vitesse[0],somme[1]-I.vitesse[1]]


        sm=sqrt(Steer[0]**2+Steer[1]**2)
        if sm>I.maxforce:
            Steer[0]=Steer[0]*I.maxforce/sm
            Steer[1]=Steer[1]*I.maxforce/sm
            
        #I=bird.appliquer_force(I,Steer)
        return(Steer)

#s'occupe de la condition d'alignement

    
    def alignement(I,groupe,Rali,maxspeed,maxforce):
        somme=[0,0]
        c=0
        dist=0
        Steer=[0,0]
        for J in groupe:
            d=bird.dist(I,J)
            if d<Rali and d>0:
                somme=[somme[0]+J.vitesse[0],somme[1]+J.vitesse[1]]
                c+=1
        if c>0:
            somme=[somme[0]/c,somme[1]/c]
            somme=[somme[0]*maxspeed,somme[1]*maxspeed]    
            Steer=[somme[0]-I.vitesse[0],somme[1]-I.vitesse[1]]


        sm=sqrt(Steer[0]**2+Steer[1]**2)
        if sm>I.maxforce:
            Steer[0]=Steer[0]*I.maxforce/sm
            Steer[1]=Steer[1]*I.maxforce/sm

        return(Steer)   

        
#Appliques et balance les differentes forces avec suivie de souris

    def apply_forces_s(I,groupe,Rcoh,Rsep,Rali,maxspeed,maxforce,fcoh,fsep,fali,fsui):

        sep=[0,0]
        sep=bird.separer(I,groupe,Rsep,maxspeed,maxforce)
        sep=[sep[0]*fsep,sep[1]*fsep]



        coh=[0,0]
        coh=bird.cohesion(I,groupe,Rcoh,maxspeed,maxforce)
        coh=[coh[0]*fcoh,coh[1]*fcoh]

        sui=[0,0]
        sui=bird.suivre(I,pg.mouse.get_pos())
        sui=[sui[0]*fsui,sui[1]*fsui]

        ali=[0,0]
        ali=bird.alignement(I,groupe,Rali,maxspeed,maxforce)
        ali=[ali[0]*fali,ali[1]*fali]

        bird.appliquer_force(I,coh)
        bird.appliquer_force(I,sep)
        bird.appliquer_force(I,sui)
        bird.appliquer_force(I,ali)



#Appliques et balance les differentes forces sans suivie de souris

    def apply_forces(I,groupe,Rcoh,Rsep,Rali,maxspeed,maxforce,fcoh,fsep,fali):

        sep=[0,0]
        sep=bird.separer(I,groupe,Rsep,maxspeed,maxforce)
        sep=[sep[0]*fsep,sep[1]*fsep]



        coh=[0,0]
        coh=bird.cohesion(I,groupe,Rcoh,maxspeed,maxforce)
        coh=[coh[0]*fcoh,coh[1]*fcoh]


        ali=[0,0]
        ali=bird.alignement(I,groupe,Rali,maxspeed,maxforce)
        ali=[ali[0]*fali,ali[1]*fali]

        bird.appliquer_force(I,coh)
        bird.appliquer_force(I,sep)
        bird.appliquer_force(I,ali)




    def apply_forces_evite(I,groupe,Rcoh,Rsep,Rali,maxspeed,maxforce,fcoh,fsep,fali,fsui):

        sep=[0,0]
        sep=bird.separer(I,groupe,Rsep,maxspeed,maxforce)
        sep=[sep[0]*fsep,sep[1]*fsep]



        coh=[0,0]
        coh=bird.cohesion(I,groupe,Rcoh,maxspeed,maxforce)
        coh=[coh[0]*fcoh,coh[1]*fcoh]

        sui=[0,0]
        sui=bird.eviter(I,pg.mouse.get_pos())
        sui=[sui[0]*fsui,sui[1]*fsui]

        ali=[0,0]
        ali=bird.alignement(I,groupe,Rali,maxspeed,maxforce)
        ali=[ali[0]*fali,ali[1]*fali]

        bird.appliquer_force(I,coh)
        bird.appliquer_force(I,sep)
        bird.appliquer_force(I,sui)
        bird.appliquer_force(I,ali)













        




