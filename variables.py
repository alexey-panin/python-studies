import functools
import logging

logger = logging.Logger

# Main Data Types in Python


first_dict = {
    "hello": "world",
    "it is": "me",
    "I am": "a boy"
}
a_list = [1, 2, 3, 4, 5]
integer = "Hello world"
float_num = 1.34
number = 1
boolean = False

print(type(boolean))

filter_result = list(filter(lambda num: num < 4, a_list))
print(filter_result)

map_result = list(map(lambda num: num + 1, a_list))
print(map_result)

logging.error(a_list)

reduce_result = list(functools.reduce(lambda accum, curr: accum + curr, a_list))


print(first_dict)
print(first_dict.items())

for [key, value] in first_dict.items():
    print("the key is {} and corresponding value is {}".format(key, value))

try:
    print(not_existing_variable)
except NameError as e:
    print("variable is not assigned, error {}".format(e))


def hello_name(name: str) -> str:
    """Returns Hello Name """
    return(f"Hello {name}")
