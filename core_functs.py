import os, json, math, random, time

#yeah yeah sin cos tan but cos and sin should be index 0 and 1 respectively bc I said so
trig_functs = [math.cos, math.sin, math.tan]

def get_ms():
    return round(time.time() * 1000)

def get_distance(coords, target):
     return math.sqrt((coords[0] - target[0])**2 + (coords[1] - target[1])**2)

#takes into account the inverted y-axis of pygame
def get_angle(coords, target):
    return math.atan2(target[1] - coords[1], target[0] - coords[0])

#vec = [start_point, end_point]
def dot(vec_1, vec_2):
    vec_diff = [[vec_1[1][i] - vec_1[0][i] for i in range(2)], [vec_2[1][i] - vec_2[0][i] for i in range(2)]]
    return (vec_diff[0][0] * vec_diff[1][0]) + (vec_diff[0][1] * vec_diff[1][1])

#default range is 0 to 1
def clamp(value, clamp_range=(0, 1)):
    return max(min(value, clamp_range[1]), clamp_range[0])

#linear interpolation
def lerp(current, target, rate):
    return current + (target - current) * rate

#fractional interpolation
def ferp(current, target, rate):
    return (target - current) * rate

#safe division
def divide(dividend, divisor):
    try: return dividend/divisor
    except ZeroDivisionError: return 0

def sgn(value):
    return int(divide(abs(value), value))

def narrow_path(folder, file_name):
    for i in os.listdir(folder):
        if file_name == i or file_name == os.path.splitext(i)[0]:
            return os.path.join(folder, i)

    return os.path.join(folder, file_name)

def read_file(file_path):
    f = open(file_path, 'r')
    data = f.read()
    f.close()
    return data

def read_json(file_path, error_val=None):
    try: 
        f = open(file_path, 'r')
        data = json.load(f)
        f.close()
        return data

    except FileNotFoundError: return error_val

def write_json(file_path, content):
    f = open(file_path, 'w')
    data = json.dump(content, f, indent=6)
    f.close()
    return data


def create_json(file_path, content):
    f = open(file_path, 'w+')
    data = json.dump(content, f, indent=6)
    f.close()
    return data

#checks if a string represents an int or a float i.e. "12" --> True
#wrapper for string.isdigit() to cover for sign cases
def is_digit(string):
    for char in string:
        if char in ["-", "+", "."]:
            string = string.split(char)
            string = char.join(string)
            
    return string.isdigit()

#dict functs

#used to drill a dictionary and input values
def data_pierce(item, key_list, value={}):
    if len(key_list) > 0:
        if len(key_list) == 1:
            ret_val = value
        else: 
            ret_val = {}

        item[key_list[0]] = item.get(key_list[0], ret_val)
        data_pierce(item[key_list[0]], key_list[1:], value=value)

#tries to retrieve data specified in the dictionary path
#returns None if dictionary path doesn't exist
#kinda sounds like a scout right?
def data_scout(item, key_list):
    if len(key_list) > 0:
        if isinstance(item, dict):
            return data_scout(item.get(key_list[0]), key_list[1:])
    return item

def copy_dict(item):
    def replicate_dict(item):
        if isinstance(item, dict):
            copy_dict(item.copy())
        return item

    return {k : replicate_dict(v) for k, v in item.items()}

#this sounds so wrong
def prune_dict(item, blank_val={}):
    if isinstance(item, dict):
        for k in item.copy():
            v = prune_dict(item[k], blank_val=blank_val)
            if v == blank_val:
                item.pop(k)
            if not len(item):
                item = blank_val

    elif item == blank_val:
        return blank_val

    return item

def class_reg_funct(dict_obj):
    def reg(target_cls):
        dict_obj[target_cls.__name__.lower()] = target_cls
        return target_cls
    return reg

def mince_list(lst):
    def mincer(item):
        for i in item:
            if isinstance(i, list):
                for j in mincer(i):
                    yield j
            else:
                yield i
    minced_data = mincer(lst)
    return [i for i in minced_data]

