import importlib
import os
import subprocess
import math
import itertools
import random


def eqValue(gbsv, pyv):
    return gbsv == str(pyv)


def delete_files_in_dir(dir, exceptions=[]):
    for f in os.listdir(dir):
        if not f in exceptions:
            os.remove(os.path.join(dir, f))


def group(lst, n):
    res = []
    sublst = []
    for x in lst:
        sublst.append(x)
        if len(sublst) == n:
            res.append(sublst)
            sublst = []
    if len(sublst) > 0:
        res.append(sublst)
    return res


def flatten(lst):
    res = []
    for x in lst:
        if isinstance(x, list):
            res.extend(flatten(x))
        else:
            res.append(x)
    return res


def parent_dir(f):
    return os.path.split(os.path.realpath(f))[0]


def module_dir(obj):
    return os.path.dirname(__file__)


def dir_has_tests(dir):
    for fn in os.listdir(os.path.join(parent_dir(__file__), dir)):
        if "test" in fn:
            return True
    return False


def is_module(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except Exception as e:
        return False

def run_cmd(cmd):
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()

def append_file(fn, s):
    f = open(fn, "a")
    f.write(s)
    f.close

def read_file(fn):
    f = open(fn, 'r')
    s = f.read()
    f.close()
    return s

def read_file_lines(fn):
    f = open(fn, 'r')
    ls = f.readlines()
    f.close
    return ls

def write_file(fn, s):
    f = open(fn, "w")
    f.write(s)
    f.close()


def copy_file(fn, fnnew):
    write_file(fnnew, read_file(fn))


def temp_test_file(codestr):
    fn = os.path.dirname(__file__) + "/examples/" + str(id(codestr)) + ".gbs"
    write_file(fn, codestr)
    return fn


def unzip(l):
    return [list(t) for t in zip(*l)]


def first_half(lst):
    return lst[:len(lst) / 2]


def second_half(lst):
    return lst[len(lst) / 2:]


def all_permutations(xs):
    if xs == []:
        yield []
    else:
        for i in range(len(xs)):
            for p in all_permutations(xs[:i] + xs[i + 1:]):
                yield [xs[i]] + p


def all_subsets(xs):
    if xs == []:
        yield []
    else:
        for s in all_subsets(xs[1:]):
            yield s
            yield [xs[0]] + s

def all_slicings(xs):
    if len(xs) == 0:
        yield []
    elif len(xs) == 1:
        yield [xs]
    else:
        for s in all_slicings(xs[1:]):
            yield [[xs[0]]] + s
            yield [[xs[0]] + s[0]] + s[1:]


def ifloor(f):
    return int(math.floor(f))


def iceil(f):
    return int(math.ceil(f))


randint = lambda x: random.randint(0,x-1)


def randomList(generator, max_size=16):
    return [generator(i) for i in range(randint(max_size) + 4)]


def randomIntList(max_size=16, max_number=99):
    return randomList(lambda i: randint(max_number), max_size)


def nats(start, end):
    if (start < end):
        return list(range(start, end+1))
    else:
        l = list(range(end, start+1))
        l.reverse()
        return l

BINOPS = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "div": lambda x, y: x / y,
    "mod": lambda x, y: x % y,
}

binop = lambda op, x, y: BINOPS[op](x,y)

# Gbs syntax

isEmpty = lambda xs: len(xs) == 0
head = lambda xs: xs[0]
tail = lambda xs: xs[1:]


# Test scripts


def combine_args(args):
    prod = itertools.product(*args.values())
    return [dict(zip(args.keys(),pargs)) for pargs in prod]


COLORS = ["Azul", "Negro", "Rojo", "Verde"]
DIRS = ["Norte", "Este", "Sur", "Oeste"]
BOOLS = ["True", "False"]