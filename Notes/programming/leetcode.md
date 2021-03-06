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
	```
      C[i,j] = C[i-1][j-1] -> if s[i] == t[j],
               max(C[i-1][j],C[i][j-1]) -> s[i] != t[j]
	```
	- Then the final solution would be given by - `C[m][n]`

- Coin change problem -
	- Find the minimum number of coins of the given denominations that will add up to the given amount.
	- For particular denominations, this problem is greedy (When the values are exponents of each other)
	- Recurrence - 
		- C[n] - Represents the minimum number of coins for amount n
		```
		C[n] = min(1 + C[n - coin[k]])	For k in 0..number of denominations
		```
		- Note that C[0] is 0. Everything else can be set to positive inf. This will allow us to filter those amounts that cannot be made up by the denominations.
	- Problem - https://leetcode.com/problems/coin-change/

- Circular DP problems -
	- There are some problems which involve circular arrays.
	- We cannot apply DP on them, because when creating a recurrence relation C[i] will depend on other C[i+-1]. It will never depend on itself. In circular lists, this rule breaks. The dependency graph of a DP will no longer be a DAG and there will be a cycle.
	- Usually the solution will involve - 
		- Break the question down into some forms where you can apply the DP.
		- Combine the solution. 
		- When breaking it down does not work, try to think of some property of the input array. Sometimes making something into a cycle will add additional properties and simplify things into 2 groups.
	- Problems - 
		- https://leetcode.com/problems/house-robber-ii/
		- https://leetcode.com/problems/maximum-sum-circular-subarray/

- Longest increasing subsequence -
	- Find the longest (strictly) increasing subsequence.
	- C[i] represents the length of the longest inc. subseqence from i to n. Realizing this was the tricky part.
	- The recurrence - 
	  ```
	  C[i] = max(1 + C[k]) For k in i...n, if A[i] < A[k]
	  ```
	- Problem - https://leetcode.com/problems/longest-increasing-subsequence/


## Really good posts to start leetcoding
- Blind 75
	- These cover most of the techniques asked by interviewers. Covering this would be a good start. 
	- Note that this list contains some questions that are LC hard and require premium.
	- https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions
	- https://www.teamblind.com/post/New-Year-Gift---Curated-List-of-Top-75-LeetCode-Questions-to-Save-Your-Time-OaM1orEU
- Patterns to solve interview questions - 
	- This link is a top-level view of most of the patterns. Really useful - 
		- https://hackernoon.com/14-patterns-to-ace-any-coding-interview-question-c5bb3357f6ed?source=bookmarks---------13-----------------------
- Sliding window - 
	- Really good way to start learning about sliding window - 
		- https://medium.com/@zengruiwang/sliding-window-technique-360d840d5740
	- The best resource on all forms of sliding window. Very good explanation - 
		- https://medium.com/outco/how-to-solve-sliding-window-problems-28d67601a66

## Subsets
- Getting the power set of a given input
	- Requires a queue/stack
	- Pop entry from the queue
	- Add it to result set
	- Iterate through every index of the entry, create a new entry without that index, and add it to the queue.
	- Repeat until the queue is not empty
	```
	res = set()
	q = deque()
	q.append(nums)
	q.append([]) 
	while len(q) > 0:
	    n = q.pop()
	    res.add(tuple(n))
	    for i in range(len(n)):
	        v = n[:i] + n[i+1:]
	        if len(v) > 0:
	            q.append(v)
	return res
	```
	- Problem - https://leetcode.com/problems/subsets/

## Kadane's algorithm 
- This is crucial for finding maximum sum of a sub-array. This is very often asked.
	- https://leetcode.com/problems/maximum-subarray/
	- This is a kind of DP (sliding window)
	- Basic gist is for every element, you can either start a new sub-array from it, or continue from a previous starting point
	- If starting of the sub-array, then you need to use the original element.
	- If it's the middle of the sub-array, then you need a use the rolling sum.
	- Maximization of the both these entries leads to the maximum result somewhere in the array
	```
	def maxSubArray(self, nums: List[int]) -> int:
		max_val = nums[0]
		prev_val = nums[0]
		for i in range(1, len(nums)):
			prev_val = max(nums[i] + nums[0], nums[i])
			max_val = max(max_val, prev_val)
		return max_val
	```

## Trees
All the basic high low questions comes down to how to traverse the tree. Here are the three traversals, both recursive and non-recursive form.

### Preorder traversal
#### Recursive
```
def pre_traverse(self, root):
	if root is None:
	    return
	print(root.val)
	self.pre_traverse(root.left)
	self.pre_traverse(root.right)
```

#### Non recursive
This is straight-forward use of a stack. Replace this with a queue, and you have level-order.
```
def pre_traverse(self, root):
    s = deque()
    s.append(root)
    while len(s) > 0:
        curr = s.pop()
        print(curr.val)
        if curr.right is not None:
            s.append(curr.right)
        if curr.left is not None:
            s.append(curr.left)

```

### Inorder traversal
#### Recursive 
```
def in_traverse(self, root):
    if root is None:
        return 
    self.in_traverse(root.left)
    print(root.val)
    self.in_traverse(root.right)
```

#### Non-recursive 
- Keeping pushing the current element's left entry until there is no more
- Then pop from the stack. Print it.
- Make the current element the right element.
- Repeat.
- Note that the right element is never put in the stack. It is just set to the current element. This was always the confusing thing.
```
def in_traverse(self, root):
    s = deque()
    curr = root
    while True:
        while curr is not None:
            s.append(curr)
            curr = curr.left
        if len(s) == 0:
            break
        curr = s.pop()
        print(curr.val)
        curr = curr.right

```

### Level order traversal
This is basically non-recursive pre-order with a queue, instead of a stack.
```python
def levelOrder(self, root: TreeNode) -> List[List[int]]:
    if root is None:
        return []
    q = deque()
    q.append((root, 0))
    while len(q) > 0:
        curr, lvl = q.popleft()
        print(f"Value - {curr.val} - level - {lvl}")
        
        if curr.left is not None:
            q.append((curr.left, lvl+1))
            
        if curr.right is not None:
            q.append((curr.right, lvl+1))
```
- Related problems - 
	- https://leetcode.com/problems/binary-tree-level-order-traversal

## Binary search

I unnecessarily complicate binary search related questions.
Usually working it out fully on paper is better than writing out the code.
Binary search to find the correct position of insertion.

```python
def getIndex(self, price):
    numStocks = len(self.stocks)
    if numStocks == 0:
        return -1
    
    # find the last value that is <= price
    l = 0
    r = numStocks - 1
    while l <= r:
        if l == r:
            if self.stocks[l] < price:
                return l + 1
            return l
        mid = (l + r) // 2
        if self.stocks[mid] <= price:
            l = mid + 1
        else:
            r = mid - 1
    if r < 0:
        return r
    if price >= self.stocks[r] and price < self.stocks[l]:
        return l
    else:
        return r
```

## Backtracking questions - 

This is a very big write-up.
https://leetcode.com/problems/permutations/discuss/18239/A-general-approach-to-backtracking-questions-in-Java-(Subsets-Permutations-Combination-Sum-Palindrome-Partioning)

Whenever doing backtracking questions, make sure that you also think in terms of DFS. I always for some reason, start with BFS, and code it out, but usually it's inefficient. One disadvantage is storing worlds (in this storing the visited entries). Since with DFS, you can write a recursive solution, the worlds can be handled much better. 

Problem that exhibits the above the idea 
- Word-search 2 - https://leetcode.com/problems/word-search-ii/
	- Refer this answer to how simple and elegant the recursive solution can be - https://leetcode.com/problems/word-search-ii/discuss/59780/Java-15ms-Easiest-Solution-(100.00)
- Word search 1 - https://leetcode.com/problems/word-search 

There is a bunch of problems on matrices, that have standard DFS solutions - 
- Pacific atlantic water flow - https://leetcode.com/problems/pacific-atlantic-water-flow/
- Number of islands - https://leetcode.com/problems/number-of-islands/
- Increasing path in a matrix - https://leetcode.com/problems/longest-increasing-path-in-a-matrix/
	- Note that this has a memoization component to it as well.

These are textbook DFS. Here is a nice rundown of how to approach the DFS questions - 
https://leetcode.com/problems/pacific-atlantic-water-flow/discuss/90739/Python-DFS-bests-85.-Tips-for-all-DFS-in-matrix-question.

Another really unique question, that uses DFS is - 
- Longest consective sequence - https://leetcode.com/problems/longest-consecutive-sequence/
	- This can be done in O(n) with the right use of sets!!!
	- A really awesome answer, if I say so myself :)

Standard DFS solution looks like this - 
```python
def main(matrix, rows, cols):
	for i in range(rows):
		for j in range(cols):
			DFS(matrix, i, j)

def DFS(self, matrix, i, j):
	rows = len(matrix)
	cols = len(matrix[0])
	# Perform bound checks on i and j
	if i < 0 or j < 0 or i >= rows or j >= cols:
		return 

	# Check for some kind of condition here

	# Set current entry as visited
	c = matrix[i][j]
	matrix[i][j] = "V"

	self.DFS(matrix, i+1, j)
	self.DFS(matrix, i-1, j)
	self.DFS(matrix, i, j+1)
	self.DFS(matrix, i, j-1)

	# Unset visited
	matrix[i][j] = c

	return
```

## Array questions -
- When DP, sliding window, and graphs don't work. Try doing the manipulations logically.
- Some sample problems - 
	- https://leetcode.com/problems/contiguous-array/

## Graphs 
- Finding the path with the lowest cost - 
	- https://leetcode.com/problems/network-delay-time/
	- This needs Djikstra's algorithm to be efficient, but the non-efficient solution is also accepted.
	- Read up on Djikstra's algorithm - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- Understanding Bi-partite graphs - 
	- https://leetcode.com/problems/possible-bipartition/
	- NOTE - 
		- I had absolutely no idea on how to solve this properly.
		- Read up on these -
			- https://math.stackexchange.com/a/311670/744624
			- https://www.cs.cmu.edu/~adamchik/21-127/lectures/graphs_5_print.pdf
		- Turns out, that we have to mark nodes as red and blue. 
		- Red will only touch blues, and vice versa. If there's an anomaly, then it's not a bi-partite graph.
		- This cannot be solved using union-find. Union-find is used for finding cycles in a graph. A bi-partite graph can have a cycle, but it needs to be of even length (of both nodes and edges). So in this scenario, finding cycles isn't enough. 
Both the DFS and BFS way will work.