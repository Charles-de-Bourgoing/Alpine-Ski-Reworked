

#A FAIRE
=================
# VISUEL
=================



## Skieur qui plie les jambes

Il faut un modèle 3D avec des os qui peuvent bouger, voir si c'est faisable avec ursina ou si on doit télécharger des/crééer nos animations.

## Lignes des skis

Les traces laisées par les 2 skis. Sera probablement réinventé si on considère la physique des skis. Veiller à bien gérer ça pour ne pas faire lagguer.

## Skis visibles

Dans le cas de notre modèle, cela peuten fait voiloir dire soit des skis qui tournent plus que ce qu'on tourne (mais bon cela ne correspond pas au but de réalisme du simulateur), soit un modèle avec de plus gros skis, soit une caméra qui bouge, cf après.

## Caméra intelligente

N'est pas toujours derrière : soit un léger retard, soit moitié derrière moitié dans le sens de la piste. Voir avec les propositions de gameplay à 180° ci-après (mais bon c'est pour plus tard)

## Gerbes de neiges

Dans les gros tournants (angle de vitesse =/= angle des skis)

## Brume 

Pas forcément joli, mais cache la suite de la piste pas encore chargée



================
# Gameplay
================

## Bosses nulles au centre

Avoir une piste bien plate au centre. 

## Choix des paramètres au lancement

Notamment paramètres de la piste et des objets

## Barrières

Suivent des splines, avec une texture de barrrière. Ne pas dépasser les chunks, il faudra ensuite implémenter des collisions mais on est plus dans la phase d'expérimentation donc moins important.


## Descente 180°

La pente n'est pas juste selon une lichette à l'avant, le skieur peut choisir

## Niveaux, types de bosses

Plus grosses bosses que le noise qu'on a jusque là.


===============
# Physique
===============

## Ecrasement de neige 

Simule le fait qu'avec une force importante le terrain/la neige peut être traversée (elle n'est pas 100% rigide) Par exemple, quand on tombe sur une bosse on peut un peu passer à travers en l'applatissant. Cela réduirait le saut constant (90% du temps en l'air et saut direct après) qu'on commence à ressentir à haute vitesse (quoique ce soit aussi causé par la grande quantité de bosses et la vitesse max infinie)

En particulier, on peut le coupler avec le système d'amortissement (mais dans le cadre d'une simulation minimale ce n'est pas forcément intéressant)

## Frottements de l'air

Donne une vitesse limite bienvenue. On peut la couplet avec l'amortissement (ie la hauteur du skieur), mais comme cet amortissement est automatique ce n'est pas forcément intéressant. Il peut être sympa ensuite d'avoir un indicateur visuel de l'atteinte de la vitesse max.

## Deux skis indépendants

C'est probablement juste visuel

## Epatement de neige sous les carres

-> Fait encore plus ralentir lors des tournants

===============
# IA
===============

On essaiera plus tard d'entraîner des IAs (NN) à glisser
 
## Voir comment désactiver le graphique en Ursina

Pour entraîner sans run toute la partie graphique ! Est-ce que c'est même possible ou on ne peut pas le faire avec Ursina ?

## Implémenter une logique de vision/détection minimale