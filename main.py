# coding:utf8
import json
import requests
from Maze import Maze
from utils import *


SEED_WITH_SOLUTION = {'height': 6, 'id': 'f5596dd5f', 'width': 6}
SEED_WITHOUT_SOLUTION = {'height': 4, 'id': 'b5f5', 'width': 6}


def main(seed=None, debug=False):
	"""
	Main flow of the program. Print statement
	"""
	## Get maze
	if seed:
		maze = Maze(seed)
	else:
		response = make_request(BASE_URL)
		maze_data = json.loads(response.content)
		maze = Maze(maze_data)
	
	print('Starting to solve for a maze of size {} by {}'.format(maze.height, maze.width))

	if debug:
		reveal_maze_board(maze)
		print('Maze looks like this!')
		print(maze)

	## Get the path that solves
	path = maze_solver_dfs(maze)
	print('A solution looks like this... blank means no solution')
	print(path)

	## Decode path to solution
	solution = decode_path_solution(maze.start, path)

	## Valid solution?
	print('Is this solution valid? {}'.format(is_solution_valid(maze, solution)))
	print('Maze {} is done.'.format(maze.id))

if __name__ == '__main__':
	# Test for a maze that has solution(s)
	main(seed=SEED_WITH_SOLUTION, debug=True)

	# Test for a maze that has no solution
	main(seed=SEED_WITHOUT_SOLUTION, debug=True)

	# Test for a random maze, it might be a big maze, turn debugging on by passing debug=True
	main()
