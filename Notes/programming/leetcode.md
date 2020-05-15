# Leetcode
This is going to be some notes on handling certain types of problems when doing leetcode for interview prep.

## Sliding window technique
- [All sliding window questions link](https://leetcode.com/problemset/all/?topicSlugs=sliding-window)
- I had a general idea about this technique. 
- The fixed-size sliding window was intuitive for me, but I couldn't really figure out variable-sized window sometimes.
- Even when I solved using variable-sized windows, my solutions weren't always efficient.

### Readings 
- Gem of a page - 
	- https://medium.com/@zengruiwang/sliding-window-technique-360d840d5740
	- This is a very good page to start understanding the basic approach to solve the problem.
	- The last example required some time to be understood properly.
- This is even more comprehensive - 
	- https://medium.com/outco/how-to-solve-sliding-window-problems-28d67601a66
	- This is a really good resource.
	- Start reading this when you are trying to solve medium questions.
- Note that sliding window is a kind of DP! Since we are expanding and shrinking the window, and not recomputing the elements inside the range in every iteration, we are basically reusing it. So, it's a kind of implicit memoization.

### Basic intuition
- Always start thinking from left to right.
- Always start thinking with the window size as 0. Do NOT make the whole array the window and then start shrinking it. It's usually never the answer and wastes a lot of time.
- For fixed sizes, usually it's a giveaway in the question itself. Max sum with size K.
- For variable sizes, I used the following - 
	- Expansion rule - When should the window grow
	- Shrinking rule - When should the window shrink
- Usually expansion happens one by one. So figuring that out it enough.
- Shrinking can be one index at a time, multiple indexes at a time, or directly assigning value of the leftmost index to the rightmost index.
	- The first and last case are straightforward. After figuring them out, no need to do anything else
	- For the second case, usually it involves a while loop.
	- Therefore, doing this sometime makes the algo run `2N` the time. Asymptotically it's nothing. 
	- But sometimes it can be optimized by using a data-structure 
		- Dicts - If you want to store the indexes or frequency of the entries 
		- Heaps(prority queue) - If you want to store the max or min within the l and r indices.
- Basic boiler plate code ([Max Consecutive Ones problem](https://leetcode.com/problems/max-consecutive-ones-iii/))
```python
# Here we need to make sure that the window has atmost K zeroes
def longestOnes(self, nums: List[int], K: int) -> int:
	max_len = 0
	curr_zeroes = 0
	l = 0
	for r in range(len(nums)):
	    if nums[r] == 0:
	        curr_zeroes += 1
	        
	    # Shrinking logic
	    if curr_zeroes > K:
	        while l <= r and nums[l] != 0:
	            l += 1
	        l += 1
	        curr_zeroes -= 1

	    max_len = max(max_len, r - l + 1)

	return max_len
```
- In the above we notice the while loop when shrinking. We can remove the while-loop by using a queue. The point of the queue is to store the indices of 0s. So that whenever the number of 0s go beyond a limit, we can simply pop the queue, and assign `l` to `(q.pop() + 1)`. Like this, some problems will require a hash-table, or a heap.

- Another type of sliding window problem, disguised as a DP problem - Taking turns to pick an element from either end of an array. This was not at all intuitive at first, but this is a sliding window which loops back from the end to the start, like a circular queue. 
	- Here is a post that explains that very well - https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/discuss/597883/Javascript-and-C%2B%2B-solutions
		- Pay special attention to the diagram
	- Sample problems - 
		- https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/
		- Sliding window problem disguised as DP problem - https://leetcode.com/problems/stone-game/


## Dynamic programming
Coming up with the recursive solution is 80% the battle. After that implementing it via bottom-up with table or top-down with memoization is the challenge.

Here is a [very good link](https://leetcode.com/discuss/general-discussion/475924/my-experience-and-notes-for-learning-dp) that needs to be read

Some common and interesting recursive relations for problems -
- Finding the number of squares with 1 value and it's variations
	- The trick is to assume the current element to be the bottom right index of the square.
	- Then we can calcuate it's size based on the size from top, left and top-left values.
	- `C[i,j] = 1 + min(C[i-1,j], C[i, j-1], C[i-1, j-1])`
	- Problems - 
		- https://leetcode.com/problems/count-square-submatrices-with-all-ones/
		- https://leetcode.com/problems/maximal-square/submissions/

- Checkerboard problem 
	- Find the minimum or maxiumum path length from one side to the other.
	- `C[i,j] = a[i,j] + min(C[i+1, j], C[i+1, j - 1], C[i+1, j + 1])`
	- Problems - 
		- https://leetcode.com/problems/minimum-falling-path-sum/submissions/

- Longest common substring
	- Assume that, from the end, whatever matches is part of the solution.
	- C[i,j] here represents the length of the longest common substring between 0 and i in s1 and 0 and j in s2.
	- ```
	   	C[i,j] =	C[i-1][j-1], 			if s[i] == t[j],
	   				max(					else 
	   					C[i-1][j],			
	   					C[i][j-1]
	   				)						
	```
	- Then the final solution would be given by - `C[m][n]`

- Coin change problem -
	- Find the minimum number of coins of the given denominations that will add up to the given amount.
	- For particular denominations, this problem is greedy (When the values are exponents of each other)
	- Recurrence - 
		- C[n] - Represents the minimum number of coins for amount n
		- ```
			C[n] = min(1 + C[n - coin[k]])	For k in 0..number of denominations
		```
		- Note that C[0] is 0. Everything else can be set to positive inf. This will allow us to filter those amounts that cannot be made up by the denominations.
	- Problem - https://leetcode.com/problems/coin-change/