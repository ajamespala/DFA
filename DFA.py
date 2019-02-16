#Authors: James Pala and Zach Fukuhara
#COMP370: Automata project 1
#DFA

import sys
import re

class State:
	def __init__(self,name,start=False,accept=False):
		self.name = name
		self.links = {}
		self.start = start
		self.accept = accept

	def add_link(self, variable, next_state):
		self.links[variable] = next_state

	def get_next_state(self, variable):
		if variable in self.links:
			return self.links[variable]
		else:
			return None
	def __str__(self):
		string = "[ State Name: " + self.name + "\nstart = " + str(self.start) + "\naccept = " + str(self.accept) + "\n\tLinks:\n\t"
		for key, value in self.links.items():
			string = string + key + " -> " + value + "\n\t"
		string = string + '\t]'
		return string

class DFA:
	def __init__(self, num_states, alphabet, start_state, transitions = [], accept_states = []):
		self.num_states = num_states
		self.alphabet = list(alphabet)
		self.transitions = transitions
		self.state_state = re.sub('\n', '', start_state)
		self.accept_states = accept_states
		self.states = {}
		self.results = None
		for transition in transitions:
			t = transition.split(maxsplit=3)
			end_state = t.pop()
			tr = t.pop()
			begin_state = t.pop()
			if begin_state in self.states:
				self.states[begin_state].add_link(tr, end_state)
			else:
				new_state = State(name=begin_state)
				if start_state == begin_state:
					new_state.start = True
				if begin_state in accept_states:
					new_state.accept = True
				self.states[begin_state] = new_state
				self.states[begin_state].add_link(tr, end_state)

	def __str__(self):
		string = ""
		for key, s in self.states.items():
			string = string + str(s) + '\n'
		return string

	def create_DFA(filename):
		#read in DFA file
		f = open(filename)
		num_states = re.sub('\n', '', f.readline())
		alphabet = re.sub('\n', '', f.readline())
		next_line = f.readline()
		transitions = []
		while(next_line.find('\'') >= 0):
			next_line = re.sub('\n', '', next_line)
			next_line = re.sub('\'', '', next_line)
			transitions.append(next_line)
			next_line = f.readline()
		next_line = re.sub('\n', '', next_line)
		start_state = next_line
		accepts_line = f.readline()
		accepts_line = re.sub('\n', '', accepts_line)
		accept_states = accepts_line.split(' ')
		test_cases = f.read()
		return [DFA(num_states, alphabet, start_state, transitions, accept_states), test_cases]

	def run_DFA(self, input, outputfile=None, correctfile=None):
		lines = re.split('\n',input)
		correct = []
		result = ""
		if correctfile:
			c = open(correctfile)
			correct = c.read()
			c.close()
		le = len(lines)
		x = 0
		for line in lines:
			x = x + 1
			if (line == '' and x == le):
				continue
			line = re.sub('\n', '', line)
			res = self.iterate(line)
			result = result + self.iterate(line) + "\n"
		if(outputfile is not None):
			output = open(outputfile, 'w')
			output.write(result)
			output.close()
		self.results = result	
		if correctfile:				
			if correct == result:
				print("Check, DFA works")
			else:
				print("ERROR: CORRECT FILE DOES NOT MATCH RESULTS--------------------")
	def iterate(self, line):
		chars = list(line)
		accept_reject = "Reject"
		state = self.states[self.get_start()]
		for char in chars:
			next_state = state.get_next_state(char)
			if next_state:
				state = self.states[next_state]
			else:
				state = next_state
				break
		if state:
			if state.accept == True:
				accept_reject = "Accept"
		return accept_reject

	def get_start(self):
		for key, state in self.states.items():
			if state.start == True:
				return key
		

if __name__ == "__main__":
	if(len(sys.argv) > 1 and len(sys.argv) < 3):	
		if(sys.argv[1] == '-r'):
			for x in range(1,11):
				dfa_str = "testcases/dfa" + str(x) + ".txt"
				output_str = "testcases/output" + str(x) + ".txt"
				correct_str = "testcases/correct" + str(x) + ".txt"
				print("---File set number " + str(x))
				temp = DFA.create_DFA(dfa_str)
				str_temp = temp.pop()
				dfa = temp.pop()
				dfa.run_DFA(str_temp, output_str, correct_str)	
		elif(sys.argv[1] == '-v'):	
			case = input("Choose option: \n\tRun 10 test cases automatically (r)\n\tEnter test files manually (e)\n")

			if (case=="r"):
				for x in range(1,11):
					dfa_str = "testcases/dfa" + str(x) + ".txt"
					output_str = "testcases/output" + str(x) + ".txt"
					correct_str = "testcases/correct" + str(x) + ".txt"
					print("---File set number " + str(x))
					temp = DFA.create_DFA(dfa_str)
					str_temp = temp.pop()
					dfa = temp.pop()
					dfa.run_DFA(str_temp, output_str, correct_str)
			elif (case == "e"):
				dfa_str = input("Enter in dfa file: ")
				output_str = "temp_output.txt"
				temp = DFA.create_DFA(dfa_str)
				str_temp = temp.pop()
				dfa = temp.pop()
				dfa.run_DFA(str_temp, output_str)
				print("Results: ")
				f = open(output_str)
				print(f.read())	
		else:
			dfa_str = sys.argv[1]
			temp = DFA.create_DFA(dfa_str)
			str_temp = temp.pop()
			dfa = temp.pop()
			dfa.run_DFA(str_temp)
			if(dfa.results is not None):
				print(dfa.results)
	else:
		print("DFA [\e[3moptions\e[0m] [\e[3mfilename\e[0m]\n\toptions: -v \e[3mverbose mode\e[0m\n\t -r \e[3mrun test mode, automatically test all 10 test DFA\e[0m\n\t ")
