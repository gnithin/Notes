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
	- Therefore, doing this sometime makes the algo run 2N the time. Asymptotically it's nothing. 
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
- In the above we notice the while loop when shrinking. We can remove the while-loop by using a queue. The point of the queue is to store the indices of 0s. So that whenever the number of 0s go beyond a limit, we can simply pop the queue, and assign l to (q.pop() + 1). Like this, some problems will require a hash-table, or a heap.

