# Simple 2D Tank Game
This game is built using the python language and the pygame module. It allows 
players to host their own games and others to join them via IP.

All collision, graphics, map structure, shadow ect - is custom made by me.

The game uses a UDP socket for sending data between players.

## Start
You can start the game by running 'python main.py' 

or by running 'python toexe.py' which will create an exe file int
in the dist folder.

## Controls
- W - Drive forward
- S - Drive backwards
- A - Rotate left
- D - Rotate right

- Left key - Rotate cannon left
- Right key - Rotate cannon right

- Space - Shoot

## Gameplay 
When a tank is shot it will immediately respawn in the nearest spawn point in the map.

![image](https://github.com/Daniel-WORK-GH/tank_game/assets/120199463/f2191261-277f-464d-93cf-781dd95f1fcd)

![image](https://github.com/Daniel-WORK-GH/tank_game/assets/120199463/57351dfb-e9b9-4fa4-8616-66dc19c871f5)



