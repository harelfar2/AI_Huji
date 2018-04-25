315363838
203572375
*****
Comments:
Evaluation function:
When we play 2048 at our free time we like to keep the tiles in a form of a snake:
The biggest tile will be in the left bottom corner, next one above and the rest follow like a snake jumping to the next
column when the previous one is full. To "encourage" this behavior we multiplied our board by a snake matrix (starting
from 15 at the left bottom corner and ending with 0 in the bottom right corner) and summed up the values - the bigger
the better obviously, so this was our heuristics score.
We also added some penalties. If we saw the biggest tile wasn't at the bottom left corner (and the game was already
advanced enough with at least 16 as our biggest tile) we summed up the values of the tiles violating the order in the
leftmost column - a violation is defined when value at (row, col) < (row - 1, col). In addition the snake matrix was
replaced with a matrix with smaller values (so this action won't happen unless it's the only way), concentrating on
putting bigger values near the left corner so the number of violations will decrease.
Another penalty we subtracted from the score was all the tiles multiplied by the number of their neighbors being bigger
than them - we want to avoid big tiles being surrounded by small ones.

