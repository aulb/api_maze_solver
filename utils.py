# coding:utf8
"""
Quick utilities and helpers to for the API.
"""
import time
import json
import requests
from http import HTTPStatus
from enum import Enum


BASE_URL = 'http://52.27.140.147:9099/maze'
CHECK_ENDPOINT = lambda maze_id: '{}/{}/check'.format(BASE_URL, maze_id)
SOLVE_ENDPOINT = lambda maze_id: '{}/{}/solve'.format(BASE_URL, maze_id)
RETRY_DELAY = 0.25
PATH = 0
WALL = 1


def make_request(endpoint, params=None, http_method='POST', debug=False):
	"""
	Function that makes repeated calls until the response is not 503.
	One assumption is that without the information from the server, in particular
	if whether a cell is valid or not, then we cannot solve this problem.

	Give a brief delay on every retry.
	"""
	# Retries are omitted, we need to make sure we get an answer from the server
	# that is not 503.
	if debug:
		print('Trying to {} {} please wait ...'.format(http_method, endpoint))
	response = make_request_helper(endpoint, params, http_method)
	while response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
		time.sleep(RETRY_DELAY)
		response = make_request_helper(endpoint, params, http_method)
	return response


def make_request_helper(endpoint, params, http_method):
	if http_method == 'GET':
		response = requests.get(endpoint, params=params)
	else:
		response = requests.post(endpoint, json=params)
	return response


def is_position_valid(maze_id, position):
	"""
	Make a request to the server to see if the cell (position) is a valid cell, i.e not a wall.
	"""
	get_url = CHECK_ENDPOINT(maze_id)
	x, y = position
	params = {'x': x, 'y': y}
	response = make_request(get_url, params, 'GET')
	return response.status_code == HTTPStatus.OK


def maze_solver_dfs(maze):
	"""
	Generic DFS maze solver. Modified to not make a lot of expensive unnecessary API calls.
	"""
	start, goal = maze.start, maze.goal
	height, width = maze.height, maze.width
	stack = [('', start)]
	visited = set()

	while stack:
		path, current_position = stack.pop()
		if current_position == goal: return path
		if current_position in visited: continue
		visited.add(current_position)
		if not is_position_valid(maze.id, current_position): continue

		# Add to our stack
		x, y = current_position
		# Walk west
		if x - 1 >= 0:
			stack.append((path + 'N', (x - 1, y)))
		# Walk east
		if x + 1 < width: 
			stack.append((path + 'S', (x + 1, y)))
		# Walk north
		if y - 1 >= 0: 
			stack.append((path + 'W', (x, y - 1)))
		# Walk south
		if y + 1 < height: 
			stack.append((path + 'E', (x, y + 1)))

	# No solution
	return ''


def position_to_object(position):
	"""
	Small utility function to convert a position to the specified object.
	Example: (1, 2) -> {'x': 1, 'y': 2}
	"""
	x, y = position
	return {'x': x, 'y': y}


def decode_path_solution(start, path):
	"""
	Translates a path into a solution that the server accepts.
	Example: (0, 0), 'SE' -> [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}]
	"""
	if not path: return []
	solution = [position_to_object(start)]
	for direction in path:
		current_position = solution[-1]
		x, y = current_position['x'], current_position['y']
		if direction == 'N':
			solution.append(position_to_object((x - 1, y)))
		elif direction == 'S':
			solution.append(position_to_object((x + 1, y)))
		elif direction == 'W':
			solution.append(position_to_object((x, y - 1)))
		else:
			solution.append(position_to_object((x, y + 1)))
	return solution


def is_solution_valid(maze, solution):
	"""
	Checks the endpoint to see if the solution is valid or not.
	"""
	response = make_request(SOLVE_ENDPOINT(maze.id), solution, 'POST')
	return response.status_code == HTTPStatus.OK


def reveal_maze_board(maze):
	"""
	THIS FUNCTION IS NOT USED. Make API calls to all the cells in the maze to
	determine if its valid or not.
	"""
	## Fill the maze
	for x in range(maze.height):
		for y in range(maze.width):
			if not is_position_valid(maze.id, (x, y)):
				maze._mark_maze(x, y, WALL)
