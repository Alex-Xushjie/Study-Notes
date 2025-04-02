# String formatting
There are many methods to format the string in Python

The best way is to use .format method:

Example:

`str = 'There are {} {} students'.format (2, "smart")`

`str = 'There are {0} {1} students'.format (2, "smart")`

`str = 'There are {qty} {adj} students'.format (qty=2,adj="smart")`

There are three placeholders in above example:
1) If there is nothing inside the { }, it means that items are filled in sequence. That is, the parameters following the format function will be inserted into the preceding { } in order.
2) When numbers are added inside the { }, they indicate the corresponding positions (0th position, 1st position, etc.). The parameters following the format function are assigned as the 0, 1, 2... positions sequentially.
* Although the positions marked by {number} can be in any order, the order of the parameters in the format function remains unchanged.
3) When strings are added inside the { }, these strings act as names for those positions. Values can then be assigned to these named positions through the format function, and both the positions and format arguments can be freely arranged.





