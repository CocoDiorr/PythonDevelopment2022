import ast
import difflib
import sys
import importlib
import inspect
import textwrap


def rec_names(name, prefix):
    res = []
    for member in inspect.getmembers(name):
        if not member[0].startswith('__') and not inspect.ismodule(member[1]):
            if inspect.isclass(member[1]):
                res.extend((rec_names(member[1], prefix + '.' + member[0])))
            elif inspect.isfunction(member[1]):
                res.append((prefix + '.' + member[0], textwrap.dedent(inspect.getsource(member[1]))))
        elif inspect.isfunction(member[1]):
            res.append((prefix + '.' + member[0], textwrap.dedent(inspect.getsource(member[1]))))
    return res



modules_funcs = []

for arg in sys.argv[1:]:
    module = importlib.import_module(arg)
    modules_funcs.extend(rec_names(module, arg))

funcs = []

for f in modules_funcs:
    tmp = ast.parse(f[1])

    for node in ast.walk(tmp):
        node.__setattr__('name', '_')
        node.__setattr__('id', '_')
        node.__setattr__('arg', '_')
        node.__setattr__('attr', '_')

    funcs.append((f[0], ast.unparse(tmp)))

for i in range(len(funcs)):
    for j in range(i + 1, len(funcs)):
        if difflib.SequenceMatcher(None, funcs[i][1], funcs[j][1]).ratio() > 0.95:
            print(funcs[i][0], funcs[j][0])
