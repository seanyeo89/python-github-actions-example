import time
 
# Functions are the first class objects in Python. 
# What it means is that they can be treated just like other variables and you can pass them as
# arguments to another function  or even return them as a return value.
 
def time_it (func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__ + "took" + str(1000*(end - start)) + "mil sec")
        return result
    return wrapper
 
 
@time_it
def calc_square(num):
    start = time.time()
    result = []
    for num in num:
        result.append(num*num)
        end = time.time()
        print("calc_square took: " + str(1000*(end - start)) + "mil sec")
 
 
@time_it
def calc_cude(num):
    start = time.time()
    result = []
    for num in num:
        result.append(num*num*num)
        end = time.time()
        print("calc_cube took: " + str(1000*(end-start)) + "mil sec")
 
array = range(1,100)
out_square = calc_square(array)
