# Pseudo code for search
```
Start with a frontier that contains the initial state.
Start with an empty explored set.
Repeat:
    if the frontier is empty, then no solution
    remove a node from the frontier
    if removed node contains goal state, then return solution
    add node to the explored set
    expand node, add resulting nodes to the frontier if not already in frontier or explored set.
    
```