
import code
import inspect
from timeit import default_timer

class Solution:
  def __init__(self) -> None:
    self.cache = []
    
  def dfs(self, amount):
    if amount == 0:
      return 0
    if self.cache[amount] != self.MAX_INT:
      #print("exist subproblem get result: ", self.cache[amount])
      return self.cache[amount]
    
    for c in self.coins:
      if c <= amount:
        #v = amount - c
        #print(f"sub problem: [{amount} -> {amount-c}]")
        self.cache[amount] = min(self.cache[amount], 1 + self.dfs(amount-c))
    
    return self.cache[amount]
    
  def coinChange(self, coins, amount):
    self.coins = coins
    self.MAX_INT = int(1e9)
    self.cache = [self.MAX_INT for i in range(amount+1)]
    ans = self.dfs(amount)
    if ans == self.MAX_INT:
      if amount > 0:
        return -1
      else:
        return 0
    return ans

    
  
    
v = "2fc:8=>?"
d = ""
for i in range(len(v)):
  ch = ord(v[i])
  new_ch = chr(ch - i)
  d += str(new_ch)
  
print(d)
