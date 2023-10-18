import pygame
import consts
import entityhandler
import converter
from player import Player
from consts import colors
from server import ThreadServer, get_current_ip, get_current_hostname
from client import Client


class GameState:
	connecting = 1
	ingame = 2

gamestate = GameState.connecting


# Setup game window
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
pygame.display.set_caption(consts.PROGRAM_NAME)
pygame.init()


# Client for conencting to game or
# Server to host game 
ishosting = False
server:ThreadServer = None
client:Client = None


def game_loop():
	running = True

	while running:
		# Handle game step
		clock.tick(consts.FPS_CAP)
		screen.fill(colors.white)

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

		pygame.display.flip()


def connection_loop(events):
	global ishosting, server, client, gamestate

	name = input("Enter name: ")
	ishosting = input("Hosting ? (y/n): ") == 'y'

	entityhandler.thisPlayer.name = name

	if ishosting:
		addr = get_current_ip()
		port = consts.SERVER_PORT

		server = ThreadServer("0.0.0.0", port)
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

	# Send and get data from server
	player = entityhandler.thisPlayer
	playerjson = converter.player_to_json(player)
	client.send(playerjson)
	allplayers = client.recv()

	entityhandler.update_players(allplayers)


game_loop()
pygame.quit()
server.stop()
