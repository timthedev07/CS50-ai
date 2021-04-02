import sys

from crossword import *
import copy
import random

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        ### This function is checked and performs alright
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for x in self.domains:
            res = []
            for word in self.domains[x]:
                if len(word) == x.length:
                    res.append(word)
            self.domains[x] = set(res)
    def revise(self, x, y):
        """
        ### This function is checked and confirmed to be correct
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # initially set revised to false
        revised = False

        # get overlap
        overlap = self.crossword.overlaps[x, y]

        # if there is not overlap, then no possible revisions could be made
        if not overlap:
            return revised
        else:
            # else un pack to get ith character of xval
            # and the jth character of yval.
            (i, j) = overlap

        # make a static copy of the domains to prevent runtime 
        # set length changing error
        domain_copy = copy.deepcopy(self.domains[x])

        # iterate over the words in x's domain
        for xval in domain_copy:
            # set has overlap to be false
            has_overlap = False
            for yval in self.domains[y]:
                if xval != yval and xval[i] == yval[j]:
                    has_overlap = True
                    break
            
            if not has_overlap:
                self.domains[x].remove(xval)
                revised = True

        return revised
        

    def ac3(self, arcs=None):
        """
        ### This function is checked and confirmed to be correct
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
         # setting the queue to be the argument `arcs`
        queue = arcs

        # if arcs is none, meaning no argument is provided
        if arcs == None:

            # then we append all of the connected nodes to the queue
            queue = []
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    queue.append((x, y))
                    
        # while queue is not empty
        while len(queue) > 0:

            # dequeue the two variables
            (X, Y) = queue.pop()

            # if revised
            if self.revise(X, Y):

                # if there are no words after revising
                if len(self.domains[X]) == 0:
                    return False
                
                for Z in self.crossword.neighbors(X) - {Y}:
                    queue.append((Z, X))
        return True
    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if all of the keys in assignment exist in self.domains
        for var in self.domains:
            if var not in assignment:
                return False
        # Check for empty values
        for val in assignment.values():
            if val == "" or val == None:
                return False
        # if all checks are passed
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check for duplicates
        seen = set()
        for val in assignment.values():
            if val in seen:
                return False
            seen.add(val)

        # check for lengths
        for var, val in assignment.items():
            if var.length != len(val):
                return False

        # Check for conflicts between neighboring variables for each of the 
        # variables in the assignment.
        for var, wordx in assignment.items():
            neighbors = self.crossword.neighbors(var).intersection(assignment.keys())
            for neighbor in neighbors:
                (i, j) = self.crossword.overlaps[var, neighbor]
                if wordx[i] != assignment[neighbor][j]:
                        return False

        # Finally if all checks are passed
        return True

        
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # first get the values that belong to var in the assignment dict
        possible_values = list(self.domains[var])
        
        # set up a dictionary to store the values corresponding to the nodes they affect
        num_effected_nodes = dict()

        # get all the neighbors excluding the variables in the assignment
        neighbors = self.crossword.neighbors(var) - assignment.keys()

        # iterate over the possible values
        for possible_value in possible_values:

            # initially set the number of nodes affected to 0
            nodes_affected = 0

            # iterate over the neighbors
            for neighbor in neighbors:

                # get the overlap between the two variables
                (i, j) = self.crossword.overlaps[var, neighbor]

                # iterate over the neighbor's words
                for word in self.domains[neighbor]:

                    # if there is conflict
                    if possible_value[i] != word[j]:

                        # increment the number of nodes affected
                        nodes_affected += 1

            # record and store it inside of the dictionary previously defined
            num_effected_nodes[possible_value] = nodes_affected

        res = list(sorted(num_effected_nodes.keys(), key=lambda node:num_effected_nodes[node]))
        return res


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # first get all of the variables that are not in the assignment
        excluded = set()
        for var in self.domains:
            if var not in assignment:
                excluded.add(var)

        # getting the minimum number of remaining values
        min_num = 0
        for var in excluded:
            num_val = len(self.domains[var])
            if min_num == 0:
                min_num = num_val
                continue
            min_num = min(min_num, num_val)

        # setting up an array candidates 
        candidates = []

        max_neighbors_num = 0

        # find all variables with number of remaining values == min_num
        for var in excluded:
            if len(self.domains[var]) <= min_num:
                candidates.append(var)

                # and calculate the largest number of neighbors
                if max_neighbors_num == 0:
                    max_neighbors_num = len(self.crossword.neighbors(var))
                else:
                    max_neighbors_num = max(max_neighbors_num, len(self.crossword.neighbors(var)))
        
        # iterating over the candidates and eliminate the ones with fewer neighbors
        for candidate in candidates[:]:
            if len(self.crossword.neighbors(candidate)) < max_neighbors_num:
                candidates.remove(candidate)
        return candidates[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        # choose a variable from the problem that has not yet been assigned
        var = self.select_unassigned_variable(assignment)

        assignment_copy = assignment.copy()

        for value in self.order_domain_values(var, assignment):
            assignment_copy[var] = value
            if self.consistent(assignment_copy):
                result = self.backtrack(assignment_copy)
                if result != None:
                    return result
                assignment_copy.pop(var)
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()