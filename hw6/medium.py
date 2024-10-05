import time
# 2. Given an array of integers, write a function that finds the second largest number in the array.
# Analyze the time complexity of your solution using Big O notation.

anArray = [0, 1, 4, 23, 13, 7]
no1 = 0
no2 = 0
start_time = time.time()

# This has a time complexity of O(n) because there will only ever be one pass of the array
for i in anArray:
    if i >= no1:
        no1 = i
    elif i > no2 and i < no1:
        no2 = i

end_time = time.time()

print(f"Second highest #: {no2}")
print(f"Time elapsed: {end_time - start_time}")
