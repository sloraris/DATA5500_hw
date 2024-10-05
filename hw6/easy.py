import time
# 1. Given an array of integers, write a function to calculate the sum of all elements in the array.
# Analyze the time complexity of your solution using Big O notation.

anArray = [0, 1, 4, 23, 13, 7]
start_time = time.time()

# This has a time complexity of O(n) because there will only ever be one pass of the array
print(f"The sum of the array: {sum(anArray)}")

end_time = time.time()
print(f"Time elapsed: {end_time - start_time}")
