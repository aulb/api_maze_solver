# coding:utf8
class Maze:
	"""
	Small maze class object container.
	"""
	def __init__(self, maze_information):
		self.id = maze_information['id']
		self.width = maze_information['width']
		self.height = maze_information['height']
		self.start, self.goal = (0, 0), (self.height - 1, self.width - 1)
		self.maze = [[0 for x in range(self.width)] for y in range(self.height)]

	def _mark_maze(self, x, y, wall_element):
		self.maze[x][y] = wall_element

	# Magic function to help us visualize how the maze looks
	def __repr__(self):
		representation = '' 
		for index, row in enumerate(self.maze):
			representation += str(row)
			if index != self.height - 1:
				representation += '\n'
		return representation
