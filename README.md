# Running the API
For your convenience, please have virtualenv installed. I'm sure you all have it :)
All the requirements are now in requirements.txt.

- `git clone albert_untung_backend.bundle` or `git clone https://github.com/aulb/api_maze_solver`
- `cd albert_untung_backend`
- `virtualenv --no-site-packages -p python3.6 venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- [optional] `deactivate` and `source venv/bin/activate`

You might have to deactivate and reactivate virtualenv after installing all the requirements.

# Main Function
The maze solver is just running through a main function. To solve the maze first we need to:

1) Obtain the maze
2) Do DFS (or any other solving method), where on each cell we make the API call to check validity
3) Obtain solution from said solver method
4) Check if that solution is valid

API calls are expensive so it is best to make as little as possible.
I implemented a toy debugging option to see how the maze would look like. It is best to not reveal the board if it is big (i.e 15x15 and up) as it will take too much time.

The result should look something like the png attached to this bundle.
