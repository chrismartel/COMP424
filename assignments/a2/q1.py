from operator import ne
import numpy as np

# settings
NUMBER_OF_STEPS = 10
INITIAL_STATE = np.array([[0,0,0,4],[0,0,0,2],[1,0,4,0],[0,0,0,1]])

def main():

    # Execute 10 steps of backtracking search without forwarding
    print("Q1 b)\n")
    csp = Sudoku4CSP(INITIAL_STATE.copy(), forward_checking=False)
    for i in range(NUMBER_OF_STEPS):
        print("Step {i}:".format(i=i))
        print(csp.backtrack_search_step(), '\n')

    # Execute 10 steps of backtracking search with forwarding
    print("Q1 c)\n")
    csp = Sudoku4CSP(INITIAL_STATE.copy(), forward_checking=True)
    for i in range(NUMBER_OF_STEPS):
        print("Step {i}:".format(i=i))
        print(csp.backtrack_search_step(), '\n')

class Sudoku4CSP:
    def __init__(self, initial_state=np.zeros((4,4)), forward_checking=False):
        if initial_state.shape != (4,4):
            print("Error: array must be of size 4 x 4.")
            exit(-1)
        self.variables = initial_state

        self.assignment_history = list()

        self.forward_checking = forward_checking

        # initialize domains for each variable
        self.domains = list()
        for row in range(4):
            row_domains = []
            for col in range(4):
                if initial_state[row,col] == 0:
                    row_domains.append({1,2,3,4})
                else:
                    row_domains.append({initial_state[row,col]})
            self.domains.append(row_domains)
        
        self.initial_domains = self.domains.copy()


    '''
    Apply backtrack search algorithm to solve CSP.
    '''
    def backtrack_search_step(self):
        unassigned_variable = None
        # check for unassigned variable
        for i, x in np.ndenumerate(self.variables):
            if x == 0:
                row = i[0]
                col = i[1]
                unassigned_variable = i
                break

        # all variables assigned
        if unassigned_variable is None:
            print("CSP Solved")
            return self.variables

        # initialize variable to first value of domain
        sorted_domain = list(self.domains[row][col])
        sorted_domain.sort()

        for new_val in sorted_domain:
            self.assignment_history.append({'row':row,'col':col,'val':new_val})
            if self.assign(row, col, new_val, forward_checking=self.forward_checking):
                return self.variables
            else:
                self.assignment_history.pop(0)

        # No possible assignment found from domain
        # Revert last assignment

        if len(self.assignment_history) == 0:
            print("No solution")
            return

        last_assignment = self.assignment_history.pop(0)
        row, col, old_val = last_assignment['row'], last_assignment['col'], last_assignment['val']

        self.unassign(col,row,old_val,forward_checking=self.forward_checking)
        return self.variables

    '''
    Verify that all elements in row are dinstinct
    '''
    def row_check(self, row_index):
        row = self.variables[row_index,:].tolist()

        # filter out 0 values
        row = [i for i in row if i != 0]

        return len(set(row)) == len(row)

    '''
    Verify that all elements in column are distinct.
    '''
    def column_check(self, column_index):
        column = self.variables[:,column_index].tolist()

        # filter out 0 values
        column = [i for i in column if i != 0]

        return len(set(column)) == len(column)

    '''
    Verify that all elements of 2x2 block are distinct. 
    Block 0: upper left
    Block 1: upper right
    Block 2: lower left
    Block 3: lower right
    '''
    def block_check(self, block_index):
        if block_index == 0:
            block = self.variables[0:2,0:2]
        elif block_index == 1:
            block = self.variables[0:2,2:4]
        elif block_index == 2:
            block = self.variables[2:4,0:2]
        elif block_index == 3:
            block = self.variables[2:4,2:4]

        block = block.reshape([1,4]).tolist()[0]
        # filter out 0 values
        block = [i for i in block if i != 0]

        return len(set(block)) == len(block)

    '''List of neighbour indices of a square'''
    def neighbours(self,row,col):
        neighbours = set()

        # row and volumn neighbours
        for i in range(4):
            neighbours.add((row,i))
            neighbours.add((i,col))

        # 2 x 2 block neighbours
        # upperleft
        if row in range(2) and col in range(2):
            block_rows = [0,1]
            block_cols = [0,1]
        # upper right
        elif row in range(2) and col in range(2,4):
            block_rows = [0,1]
            block_cols = [2,3]        
        # lower left
        elif row in range(2,4) and col in range(2):
            block_rows = [2,3]
            block_cols = [0,1]          
        # lower right
        elif row in range(2,4) and col in range(2,4):
            block_rows = [2,3]
            block_cols = [2,3] 

        for block_row in block_rows:
            for block_col in block_cols:
                neighbours.add((block_row, block_col))

        # remove itself from set
        neighbours.remove((row,col))
        return neighbours

    '''Refresh domains in function of current variable state'''
    def refresh_domains(self):
        self.domains = self.initial_domains
        for row in range(4):
            for col in range(4):
                neighbours = self.neighbours(row,col)
                val = self.variables[row,col]
                for n in neighbours:
                    n_row, n_col = n[0], n[1]
                    if val in self.domains[n_row][n_col]:
                        self.domains[n_row][n_col].remove(val)


    '''Assign a value to a variable. Possibility to apply one-step forward-checking'''
    def assign(self, row, col, val, forward_checking=False):
        # update variable value and its domain
        self.variables[row,col] = val
        if not self.verify_constraints():
            print("Assign {val} to ({row},{col}): Failure".format(val = val, row=row, col=col))
            return False

        if forward_checking:
            self.domains[row][col] = {val}
            neighbours = self.neighbours(row,col)

            for n in neighbours:
                n_row, n_col = n[0], n[1]
                if val in self.domains[n_row][n_col]:
                    print("Removed {val} from domain of ({i},{j})".format(val=val,i=n_row,j=n_col))
                    self.domains[n_row][n_col].remove(val)

                    if len(self.domains[n_row][n_col]) == 1:
                        self.assign(n_row, n_col, next(iter(self.domains[n_row][n_col])), forward_checking=False)

        print("Assign {val} to ({row},{col}): Success".format(val = val, row=row, col=col))
        return True

    def unassign(self, row, col, old_value, forward_checking=False):
        print("Unassign variable ({row},{col})".format(row=row, col=col))
        self.variables[row,col] = 0

        if forward_checking:
            # reset domain to initial state and remove variable from its set
            self.refresh_domains()
            if old_value in self.domains[row][col]:
                self.domains[row][col].remove(old_value)

    '''
    Verify that constraints of current state are respected. For each row, eah column
    and each 2x2 block, all four digits needs to be different.
    '''
    def verify_constraints(self):
        # row constraints
        for i in range(4):
            if not self.row_check(i):
                return False
        # column constraints
        for j in range(4):
            if not self.column_check(j):
                return False
        # block constraints
        for b in range(4):
            if not self.block_check(b):
                return False
        return True



if __name__ == "__main__":
    main()