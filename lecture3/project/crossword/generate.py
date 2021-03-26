import sys

from crossword import *


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
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            copy_val = self.domains[variable].copy()
            for value in copy_val:
                if len(value) != variable.length:
                    self.domains[variable].remove(value)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Changing the variables' names just to make it clearer.
        X = x
        Y = y
        # setting revised initially to false
        revised = False
        # looking up the value of overlap for X and Y
        overlap = self.crossword.overlaps[X, Y]

        # if there is not overlapping, return revised(False)
        if overlap == None:
            return revised
        # otherwise unpack it to get ith char of xword and jth char of yword
        (i, j) = overlap
        # iterating through the words in X's domain
        for x in self.domains[X]:
            # iterating through the words in Y's domain
            for y in self.domains[Y]:
                # check to see if the overlapping character for each word is the same
                if x[i] != y[j] and x != y:
                    # if not the same, remove that word from X's domain
                    self.domains[X].remove(x)
                    # set revised to true
                    revised = True            
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        """
        def AC-3(csp):
            queue = all arcs in csp
            while queue non-empty:
                (X, Y) = DEQUEUE(queue)
                if REVISE(csp, X, Y):
                    if x.domain.size == 0:
                        return False
                    for each Z in X.neighbors - {Y}:
                        ENQUEUE(queue, (Z, X))
            return True
        """
        # initializing the queue
        queue = arcs
        # if arcs is none, meaning no argument is provided
        if arcs == None:
            # then we append all of the connected(overlapped) nodes
            overlaps = self.crossword.overlaps
            queue = [overlaps[key] for key in overlaps if overlaps[key] != None]
        # while queue is non-empty
        while len(queue) > 0:
            # dequeue the two variables
            (X, Y) = queue.pop()
            # if revised
            if self.revise(X, Y):
                # if length of 
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
        for key in assignment:
            if len(assignment[key]) == 0 or assignment[key] == None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check to see if the assignment is complete
        if not self.assignment_complete(assignment):
            return False
        # look for any duplicate values,
        seen = {}
        for key in assignment:
            val = assignment[key]
            # and check for length.
            if val in seen or key.length != assignment[key]:
                return False
            seen.add(val)

        # then we append all of the connected(overlapped) nodes
        overlaps = self.crossword.overlaps
        queue = [overlaps[key] for key in overlaps if overlaps[key] != None]
        for X in assignment:
            for Y in assignment:
                if X == Y:
                    continue
                # looking up the value of overlap for X and Y
                overlap = self.crossword.overlaps[X, Y]

                # if there is not overlapping, ignore the rest and head to the next iteration.
                if overlap == None:
                    continue

                # otherwise unpack it to get ith char of xword and jth char of yword
                (i, j) = overlap
                # iterating through the words in X's domain
                for x in assignment[X]:
                    # iterating through the words in Y's domain
                    for y in assignment[Y]:
                        # check to see if the overlapping character for each word is the same
                        if x[i] != y[j] and x != y:
                            # if not the same, remove that word from X's domain
                            return False
        
        return True
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


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
