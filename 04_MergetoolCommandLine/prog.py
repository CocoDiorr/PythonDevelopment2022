import cmd
import readline
import shlex
import pynames
import inspect
from collections import defaultdict
from copy import deepcopy

lang = "native"
gender_default = 'm'
suffixes = ["FullnameGenerator", "NamesGenerator", "Generator"]

all_gens = [str(i)[27:-2].split(sep='.') for i in pynames.get_all_generators()]
gens_dict = defaultdict(list)
for k, v in all_gens:
    if v not in gens_dict[k]:
        gens_dict[k].append(v)

gens_names = deepcopy(gens_dict)
for el in gens_names:
    for i in range(len(gens_names[el])):
        for sf in suffixes:
            if gens_names[el][i].endswith(sf):
                gens_names[el][i] = gens_names[el][i].replace(sf, '')

def find_subcls(gens, main_cls, prefix):
    for el in gens[main_cls]:
        if el.startswith(prefix):
            return el


class repl(cmd.Cmd):
    prompt = "(^³^ )⊃━******"

    def do_language(self, arg):
        global lang
        if arg not in ("EN", "RU", "NATIVE"):
            print("Chosen language is not supported, therefore, the native one will be used")
        else:
            lang = arg.lower()

    def complete_language(self, prefix, allcommand, beg, end):
        return [s for s in ("RU", "EN", "NATIVE") if s.startswith(prefix)]

    def do_generate(self, arg):

        args = shlex.split(arg)
        if len(args) == 1:
            s = find_subcls(gens_dict, args[0], args[0][0].upper() + args[0][1:])
            gen = eval(f"pynames.generators.{args[0]}.{s}")
            print(gen().get_name_simple(gender_default, lang))
        elif len(args) == 2:
            if args[1] in ('male', 'female'):
                s = find_subcls(gens_dict, args[0], args[0][0].upper() + args[0][1:])
                gen = eval(f"pynames.generators.{args[0]}.{s}")
                print(gen().get_name_simple(args[1][0], lang))
            else:
                s = find_subcls(gens_dict, args[0], args[1])
                gen = eval(f"pynames.generators.{args[0]}.{s}")
                print(gen().get_name_simple(gender_default, lang))
        else:
            s = find_subcls(gens_dict, args[0], args[1])
            gen = eval(f"pynames.generators.{args[0]}.{s}")
            print(gen().get_name_simple(args[2][0], lang))

    def complete_generate(self, prefix, allcommand, beg, end):
        global gens_dict
        global suffixes
        global gens_names

        args = shlex.split(allcommand, comments=True)
        if len(args) == 1:
            return list(gens_dict.keys())
        elif len(args) == 2:
            if args[1] in ("elven", "iron_kingdoms"):
                return gens_names[args[1]]
            elif args[1] in list(gens_dict.keys()) and args[1] not in ("elven", "iron_kingdoms"):
                return ["female", "male"]
            else:
                return [s for s in list(gens_dict.keys()) if s.startswith(prefix)]
        elif len(args) == 3:
            if args[1] not in ("elven", "iron_kingdoms") or args[2] in gens_names[args[1]]:
                return [s for s in ("female", "male") if s.startswith(prefix)]
            else:
                return [s for s in gens_names[args[1]] if s.startswith(prefix)]
        elif len(args) == 4:
            return [s for s in ("female", "male") if s.startswith(prefix)]

    def do_info(self, arg):
        args = shlex.split(arg)
        if len(args) == 1:
            gen = eval(f"pynames.generators.{args[0]}.{find_subcls(gens_dict, args[0], args[0][0].upper() + args[0][1:])}")
            print(gen().get_names_number())
        elif len(args) == 2:
            if args[0] in ("elven", "iron_kingdoms"):
                gen = eval(f"pynames.generators.{args[0]}.{find_subcls(gens_dict, args[0], args[1])}")
                print(gen().get_names_number())
            else:
                gen = eval(f"pynames.generators.{args[0]}.{find_subcls(gens_dict, args[0], args[0][0].upper() + args[0][1:])}")
                if args[1] == "language":
                    print(*gen().languages)
                else:
                    print(gen().get_names_number(args[1][0]))
        elif len(args) == 3:
            gen = eval(f"pynames.generators.{args[0]}.{find_subcls(gens_dict, args[0], args[1])}")
            print(gen().get_names_number(args[2][0]))

    def complete_info(self, prefix, allcommand, beg, end):
        args = shlex.split(allcommand)
        if len(args) == 1:
            return list(gens_dict.keys())
        if len(args) == 2:
            if args[1] in ("elven", "iron_kingdoms"):
                return gens_names[args[1]]
            elif args[1] in list(gens_dict.keys()) and args[1] not in ("elven", "iron_kingdoms"):
                return ["female", "male", "language"]
            else:
                return [s for s in list(gens_dict.keys()) if s.startswith(prefix)]
        if len(args) == 3:
            if args[1] not in ("elven", "iron_kingdoms") or args[2] in gens_names[args[1]]:
                return [s for s in ("female", "male", "language") if s.startswith(prefix)]
            else:
                return [s for s in gens_names[args[1]] if s.startswith(prefix)]
        if len(args) == 4:
            return [s for s in ("female", "male", "language") if s.startswith(prefix)]

    def do_exit(self):
        return True

repl().cmdloop()
