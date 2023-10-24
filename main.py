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
from menus.button import Button
from menus.menu import Menu
from menus.textbox import Textbox

class GameState:
	connecting = 1
	client_setup = 2
	server_setup = 3
	ingame = 4

gamestate = GameState.connecting


# Setup game window
screen = pygame.display.set_mode(consts.SCREEN_SIZE, pygame.SRCALPHA)
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


# Menus
def set_game_state(newstate:GameState):
	global gamestate
	gamestate = newstate

sw, sh = consts.SCREEN_SIZE
centerwidth = sw / 2

connetion_menu = Menu([
	Button("Connect to server",
		lambda:set_game_state(GameState.client_setup),
		[centerwidth, 200]),

	Button("Host server",
		lambda:set_game_state(GameState.server_setup),
		[centerwidth, 248])
])


def host_server(name):
	global client, server

	entityhandler.thisPlayer.name = name
	
	addr = get_current_ip()
	port = consts.SERVER_PORT

	server = ThreadServer("", port)
	client = Client()
	client.connect("localhost", port)

	server.start()
	
	set_game_state(GameState.ingame)


def connect_to_server(name, ip):
	global client, server

	entityhandler.thisPlayer.name = name

	port = consts.SERVER_PORT

	client = Client()
	client.connect(ip, port)

	set_game_state(GameState.ingame)
	

csname = Textbox("Name:", [centerwidth, 200], 100)
csip = Textbox("Ip:", [centerwidth, 248], 100)

client_setup_menu = Menu([
	csname,
	csip,
	Button("Connect",
		lambda:connect_to_server(csname.text, csip.text),
		[centerwidth, 296])
])


ssname = Textbox("Name:", [centerwidth, 200], 100)

server_setup_menu = Menu([
	csname,
	Button("Connect",
		lambda:host_server(csname.text),
		[centerwidth, 248])
])


def game_loop():
	running = True

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

		# Update main menu
		if gamestate == GameState.connecting:
			connetion_menu.update(events)
			connetion_menu.draw(screen)

		# Set up hosting
		if gamestate == GameState.server_setup:
			server_setup_menu.update(events)
			server_setup_menu.draw(screen)

		# Set up client
		if gamestate == GameState.client_setup:
			client_setup_menu.update(events)
			client_setup_menu.draw(screen)

		# Update in game loop
		# Update the player and get data from server
		if gamestate == GameState.ingame:
			in_game_loop(events)
			
		pygame.display.flip()


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
