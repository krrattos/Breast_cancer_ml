import time


#Static variables 
PUZZLE_SIZE= 3

UP= 0
LEFT= 1
DOWN= 2
RIGHT= 3


# List to take input from the file
starting_state_array= []
goal_state_array= []


with open('input.dat') as f:
    input_lines_list = [line.rstrip('\n') for line in f]#stripping each line in the file 

scanning_starting_state_line=0
scanning_goal_state_line= 0
for line in input_lines_list:
	try:
		if len(line) > 2 and line[1] == 'S':
			scanning_starting_state_line= 1;
			continue
		elif len(line) > 2 and line[1] == 'G':
			scanning_goal_state_line= 1;
			continue
	except :
		pass

	if scanning_starting_state_line > 0 and scanning_starting_state_line < 4:
		scanning_starting_state_line+= 1
		for tile in line.split(" "):#splitting the starting state tiles
			if len(tile)>0:
				starting_state_array.append(tile);

	if scanning_goal_state_line > 0 and scanning_goal_state_line < 4:
		scanning_goal_state_line+= 1
		for tile in line.split(" "):#splitting the goal state tiles
			if len(tile)>0:
				goal_state_array.append(tile);
#converting the tiles into puzzle array        
def convert_state_array_to_puzzle_array(state_array):
	puzzle_array= []
	for item in state_array:
		if item[0] == 'T':
			puzzle_array.append(int(item[1:])-1)
		else:
			puzzle_array.append(PUZZLE_SIZE*PUZZLE_SIZE-1)
	return puzzle_array       

starting_puzzle_array= convert_state_array_to_puzzle_array(starting_state_array)
goal_puzzle_array= convert_state_array_to_puzzle_array(goal_state_array)   


def convert_index_to_xy(index):
	return {
		"x": index%PUZZLE_SIZE,
		"y": int(index/PUZZLE_SIZE)
	}

def convert_xy_to_index(xy_location):
	return xy_location['y']*PUZZLE_SIZE+xy_location['x']


class puzzle_state:
	def __init__(self, _puzzle_array, _already_played_steps, last_step, _heuristic_distance):
		self.heuristic_distance= _heuristic_distance
		self.puzzle_array= [];
		for item in _puzzle_array:
			self.puzzle_array.append(item)
		self.played_steps= []
		for step in _already_played_steps:
			self.played_steps.append(step)
		if last_step> -1:
			self.played_steps.append(last_step)


	def print(self):
		print('     ------------')
		for y in range(PUZZLE_SIZE):
			print('     |', end='')
			for x in range(PUZZLE_SIZE):
				if self.puzzle_array[y*PUZZLE_SIZE+x]+1 == PUZZLE_SIZE*PUZZLE_SIZE:
					print('  B', end='')
				else:
					print(' T'+str(self.puzzle_array[y*PUZZLE_SIZE+x]+1), end='')
			print(' |')
		print('     ------------')

#To print the steps taken to reach the goal
	def print_steps(self):
		for step in self.played_steps:
			if step == 0:
				print("U, ",end='')
			elif step == 1:
				print("L, ",end='')
			elif step == 2:
				print("D, ",end='')
			elif step == 3:
				print("R, ",end='')
			else:
				print("unknown step...!!!")


#To spot equality of two lists
	def equals(self,_match_array):
		i=0
		while i< PUZZLE_SIZE*PUZZLE_SIZE:
			if not self.puzzle_array[i] == _match_array[i]:
				return False
			i+= 1
		return True


# mahattan and misplaced tiles heuristic used

def count_manhatten_distance(puzzle_array):
	dist= 0
	for index, tile in enumerate(puzzle_array):
		if tile == PUZZLE_SIZE*PUZZLE_SIZE-1:
			continue
		goal_index= goal_puzzle_array.index(tile)
		current_pos= convert_index_to_xy(index)
		goal_pos= convert_index_to_xy(goal_index)
		dist+= abs(current_pos['x']- goal_pos['x'])+ abs(current_pos['y']- goal_pos['y'])
	return dist


def count_misplaced_tiles(puzzle_array):
	dest= 0
	for index, tile in enumerate(puzzle_array):
		if tile == PUZZLE_SIZE*PUZZLE_SIZE-1:
			continue
		if not goal_puzzle_array[index] == tile:
			dest+= 1
	return dest

#Function to apply moves
def move_blank(direction, puzzle_array):
	blank_index= puzzle_array.index(PUZZLE_SIZE*PUZZLE_SIZE -1)
	blank_pos_xy= convert_index_to_xy(blank_index)

	new_blank_pos= {'x': blank_pos_xy['x'], 'y': blank_pos_xy['y']}

	if direction == UP:
		if blank_pos_xy['y'] == 0:
			return -1
		new_blank_pos['y']-= 1

	elif direction == DOWN:
		if blank_pos_xy['y'] == PUZZLE_SIZE-1:
			return -1
		new_blank_pos['y']+= 1

	elif direction == LEFT:
		if blank_pos_xy['x'] == 0:
			return -1
		new_blank_pos['x']-= 1

	elif direction == RIGHT:
		if blank_pos_xy['x'] == PUZZLE_SIZE-1:
			return -1
		new_blank_pos['x']+= 1

	else:
		raise Exception("Direction Unspecified")

	new_blank_index= convert_xy_to_index(new_blank_pos)
	new_puzzle_array= puzzle_array.copy()
	new_puzzle_array[blank_index]= puzzle_array[new_blank_index]
	new_puzzle_array[new_blank_index]= PUZZLE_SIZE*PUZZLE_SIZE-1

	return new_puzzle_array

# Dictionary for storing already visited configurations

class dictionary:
	def __init__(self):
		self.data= {}
		self.size= 0

	def insert(self, _puzzle_array):
		state_as_str= ""
		for tile in _puzzle_array:
			state_as_str+= str(tile)
		self.data.update({state_as_str: True})
		self.size+= 1

	def has_seen(self, _puzzle_array):
		# print(self.length())
		state_as_str= ""
		for tile in _puzzle_array:
			state_as_str+= str(tile)
		if self.data.get(state_as_str) == True:
			return True
		return False

	def length(self):
		return self.size




class priority_queue:
	def __init__(self, sort_function):
		self.queue= []
		self.enqueue_index=0
		self.dequeue_index=-1
		self.total_items=0
		self.sort_function= sort_function
		self.have_already_sorted= False

	def sort(self):
		self.queue.sort(key=self.sort_function)
		self.have_already_sorted= True

	def enque(self, item):
		self.queue.append(item)
		self.total_items+=1
		self.have_already_sorted= False

	def deque(self):
		if self.total_items < 1:
			raise Exception("No items left in the Queue")
		self.total_items-= 1
		if not self.have_already_sorted:
			self.sort()
		return self.queue.pop(0)

	def length(self):
		return self.total_items

	def remove_items_with(self, remove):
		for index, item in enumerate(self.queue):
			if remove(item) == True:
				self.queue.pop(index)

def solve_using_hill_climb(heuristic_distance_algo):
	start_time= time.time()
	total_states_visited= 0
	starting_state= puzzle_state(starting_puzzle_array, [], -1, heuristic_distance_algo(starting_puzzle_array))

	Q= priority_queue(lambda state: state.heuristic_distance)
	Q.enque(starting_state)

	D= dictionary()
	D.insert(starting_state.puzzle_array)

	moves= [UP, LEFT, DOWN, RIGHT]

	print("\n\tProcessing...", end='')

	while Q.length()> 0:
		total_states_visited=total_states_visited+1
		current_state= Q.deque()
		if (total_states_visited % 1000) == 0:
			print('.', end='', flush=True)

		if current_state.equals(goal_puzzle_array):
			print('\n')
			execution_time= time.time()-start_time

			return {
				'solved': True,
				'execution_time': execution_time,
				'total_no_of_states_explored': total_states_visited,
				'last_condition': current_state
			}

		current_best_heuristics= current_state.heuristic_distance
		for move in moves:
			next_array= move_blank(move, current_state.puzzle_array)
			if (not next_array == -1) and (heuristic_distance_algo(next_array) <= current_state.heuristic_distance and not D.has_seen(next_array)):
				D.insert(next_array)
				heuristic_distance= heuristic_distance_algo(next_array)
				next_state= puzzle_state(next_array, current_state.played_steps, move, heuristic_distance)
				Q.enque(next_state)
			

#To calculate the total time taken
	execution_time= time.time()-start_time

	return {
		'solved': False,
		'execution_time': execution_time,
		'total_no_of_states_explored': total_states_visited,
	}

def solve_8_puzzle():

	print("Input State from file-")
	puzzle_state(starting_puzzle_array, [], -1, 0).print()
	print("Goal State from file-")
	puzzle_state(goal_puzzle_array, [], -1, 0).print()

	

	#print("\nEnetr 0 to start hill Climbing")
	algo= input("\n\nEnter 0 to start hill Climbing ")
	print("\nChoose the Heuristic?")
	heuristic_distance_algo= input("(1) Misplaced tiles, (2) Manhatten distance :- ")

	try:
		algo= int(algo)
		heuristic_distance_algo= int(heuristic_distance_algo)
	except :
		print("\n\n\Input Undefinded\n\n")
		return solve_8_puzzle()



	if algo== 0 and heuristic_distance_algo== 1:
		result= solve_using_hill_climb(count_misplaced_tiles)
	elif algo== 0 and heuristic_distance_algo== 2:
		result= solve_using_hill_climb(count_manhatten_distance)
	else:
		print("\n\n\tInput Undefinded\n\n")
		return solve_8_puzzle()

	if(result.get('solved')):
		print("\n\tCongartulations,Solved the problem...\n")
		print("Starting state:")
		puzzle_state(starting_puzzle_array, [], -1, 0).print()
		print("Final state:")
		result.get('last_condition').print()
		print("\nNo of steps in path:- ",end='')
		print(len(result.get('last_condition').played_steps))
		print('\n  Path->\n\t', end='')
		result.get('last_condition').print_steps()
	else:
		print("\n\tCould Not solve the Problem...\n")
		print("Starting state:")
		puzzle_state(starting_puzzle_array, [], -1, 0).print()
		print("Final state:")
		puzzle_state(goal_puzzle_array, [], -1, 0).print()

	print("\n\nTotal states explored = ", end='')
	print(result.get('total_no_of_states_explored'))
	print("execution_time: ", end='')
	print(result.get('execution_time'), end='')
	print(' s\n\n')





solve_8_puzzle()