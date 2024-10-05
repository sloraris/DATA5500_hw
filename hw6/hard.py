import time
# 3. Write a function that takes an array of integers as input and returns the maximum difference between any two numbers in the array.
# Analyze the time complexity of your solution using Big O notation.

anArray = [0, 1, 4, 23, 13, 7]
max_diff = 0
start_time = time.time()

# DISCLAIMER: This is inefficient
# This has a time complexity of O(n^2) because for every nth element added, work must be done for an additional instance of the whole array that many more times
for i in anArray:
    for j in anArray:
        if abs(i - j) > max_diff:
            max_diff = abs(i - j)

end_time = time.time()

print(f"Max difference: {max_diff}")
print(f"Time elapsed: {end_time - start_time}")


# Now for the more efficient version...
start_time = time.time()

# This has a time complexity of O(n) because there will only ever be one pass of the array
max_diff = max(anArray) - min(anArray)

end_time = time.time()

print(f"Max difference: {max_diff}")
print(f"Time elapsed: {end_time - start_time}")
