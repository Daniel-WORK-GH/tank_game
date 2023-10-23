import pygame

pygame.init()

import consts
import entityhandler
from mapobjects.player import Player
from consts import colors
from network.server import ThreadServer, get_current_ip, get_current_hostname
from network.client import Client
from network import converter
from mapobjects.map import Map
from mapobjects.shadow import Shadow
from menus.button import Button
from menus.textbox import Textbox

class GameState:
	connecting = 1
	ingame = 2

gamestate = GameState.connecting


# Setup game window
screen = pygame.display.set_mode((600, 400), pygame.SRCALPHA)
clock = pygame.time.Clock()
pygame.display.set_caption(consts.PROGRAM_NAME)


# Client for conencting to game or
# Server to host game 
ishosting = False
server:ThreadServer = None
client:Client = None


# Ingame objects
map = Map()
map.load("maps/map1.txt")
shadow = Shadow(screen, map)


def game_loop():
	running = True

	t = Textbox([250, 250], 100)

	while running:
		# Handle game step
		clock.tick(consts.FPS_CAP)
		screen.fill(colors.grass)
		#print(clock.get_fps())

		# Get all events since last step
		events = pygame.event.get()

		# Check for game close event
		for event in events: 
			if event.type == pygame.QUIT:
				running = False

		# Update connection loop
		# Set up hosting / login to other server
		if gamestate == GameState.connecting:
			connection_loop(events)

		# Update in game loop
		# Update the player and get data from server
		if gamestate == GameState.ingame:
			in_game_loop(events)

			t.update(events)
			t.draw(screen)

		pygame.display.flip()


def connection_loop(events):
	global ishosting, server, client, gamestate

	name = input("Enter name: ")
	ishosting = input("Hosting ? (y/n): ") == 'y'
	
	entityhandler.thisPlayer.name = name

	if ishosting:
		addr = get_current_ip()
		port = consts.SERVER_PORT

		server = ThreadServer("", port)
		client = Client()
		client.connect("localhost", port)

		server.start()
	else:
		addr = input("Enter server ip: ")
		port = consts.SERVER_PORT

		client = Client()
		client.connect(addr, port)

	gamestate = GameState.ingame


def in_game_loop(events):
	# Update players
	entityhandler.update(clock, events)

	# Draw players
	entityhandler.draw(screen)

	# Draw vision
	shadow.draw(screen, entityhandler.thisPlayer.position)

	# Draw map
	map.draw(screen)

	# Send and get data from server
	player = entityhandler.thisPlayer
	playerjson = converter.player_to_json(player)

	client.send(playerjson)
	allplayers = client.recv()

	if allplayers != None:
		entityhandler.update_players(allplayers)


game_loop()
pygame.quit()
server.stop()
