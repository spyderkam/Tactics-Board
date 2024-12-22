# Notes

## What is the significance of `BLUE_TEAM = [pos[:] for pos in ORIGINAL_BLUE]` vs. just `BLUE_TEAM = ORIGINAL_BLUE`?

The significance of using `BLUE_TEAM = [pos[:] for pos in ORIGINAL_BLUE]` versus `BLUE_TEAM = ORIGINAL_BLUE` lies in how they handle mutable objects like lists.

### Shallow Copy vs Reference:

- `BLUE_TEAM = [pos[:] for pos in ORIGINAL_BLUE]` creates a new list where each element is a copy of the corresponding element from `ORIGINAL_BLUE`. This means you are creating a new instance of the list, and changes to the objects inside `BLUE_TEAM` won't affect `ORIGINAL_BLUE`, and vice versa.
- `BLUE_TEAM = ORIGINAL_BLUE` merely creates a reference to the same list. Any modification to `BLUE_TEAM` will directly affect `ORIGINAL_BLUE` since they both point to the same object in memory.

### Implications:

- If you want `BLUE_TEAM` to operate independently from `ORIGINAL_BLUE`, as would typically be the case if you're manipulating player positions and want to preserve the original formation for reuse, you need to use the first approach.
- Using the second approach might lead to unintended side effects if either list is modified later in the code.

### Example:

For intance, in a soccer game simulation, if `ORIGINAL_BLUE` holds the initial positions of the players, and during gameplay you want to update them in `BLUE_TEAM` while retaining the original positions for resetting or switching strategies, you would favor the first method.

Here’s an illustrative code snippet:
```python
# Original positions
ORIGINAL_BLUE = [[180, 540], [456, 360], [456, 540]]  # Example positions

# Creating a mutable copy
BLUE_TEAM = [pos[:] for pos in ORIGINAL_BLUE] 

# Now changes to BLUE_TEAM do not affect ORIGINAL_BLUE
BLUE_TEAM[0][0] = 200  # Move first player's position
print(ORIGINAL_BLUE)  # Still [[180, 540], [456, 360], [456, 540]]
print(BLUE_TEAM)      # Now [[200, 540], [456, 360], [456, 540]]
```

### In Summary
Creating a shallow copy: <br>
`BLUE_TEAM = [pos[:] for pos in ORIGINAL_BLUE]`

Creating a reference:: <br>
`BLUE_TEAM = ORIGINAL_BLUE`



<br><br><br><br>
## Why are some of the field lines being drawn in `main.py` and others in `server.py`?

## Document tool usage

## Issues:
