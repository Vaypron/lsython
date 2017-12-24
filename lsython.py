import os
import sys


class bcolors:
    HEADER = '\033[91m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def files(path):
    items={"visible": {"dirs": [], "files": []}, "invisible": {"dirs" : [], "files": []}}

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if file[0] == '.':
                items["invisible"]["files"].append(file)
            else:
                items["visible"]["files"].append(file)

        elif os.path.isdir(os.path.join(path, file)):
            if file[0] == ".":
                items["invisible"]["dirs"].append(file)
            else:
                items["visible"]["dirs"].append(file)

    return  items


def get_file_information(filename):
    file = os.stat(filename)
    print(file)


def output(path, use_subfix):
    print("")
    directory = files(path=path)

    print(bcolors.BOLD+bcolors.HEADER+bcolors.UNDERLINE+"Files and directories you shouldn't be allowed to see:"+bcolors.ENDC)
    print("")
    for invisible in directory["invisible"]["dirs"]:
        prefix = "    "
        if is_exe(invisible):
            prefix[0] = "+"
        print(bcolors.OKGREEN+prefix+invisible)

    for invisible in directory["invisible"]["files"]:
        prefix = "    "
        if is_exe(invisible):
            prefix[0] = "+"
        print(bcolors.WARNING+prefix+invisible)

    print("")
    print(bcolors.BOLD+bcolors.HEADER+bcolors.UNDERLINE+"That are files you should be allowed to see:"+bcolors.ENDC)
    print("")

    for visible in directory["visible"]["dirs"]:
        prefix = "    "
        if is_exe(visible):
            prefix[0] = "+"
        print( bcolors.OKGREEN + prefix + visible)

    for visible in directory["visible"]["files"]:
        prefix=generate_prefix(path,visible)
        subfix=""
        if use_subfix == True:
            subfix=generate_subfix(path,visible)
        print(bcolors.WARNING +prefix + visible + subfix)

    print(bcolors.ENDC)
    print("")
    print("")
    generate_legend()


def generate_legend():
    print("+Executables  " + bcolors.WARNING + u"\u2588" +bcolors.ENDC+"File  " + bcolors.OKGREEN + u"\u2588" +bcolors.ENDC+"Directory")


def generate_prefix(path,file):
    prefix = "    "
    if is_exe(os.path.join(path, file)):
        tmp = list(prefix)
        tmp[0] = "+"
        prefix = "".join(tmp)
    return prefix

def generate_subfix(path, file):
    subfix= ""
    Extension=file[-3:]
    tmp = list(subfix)
    for i in range(15-len(file)):
        tmp.append(" ")
    subfix = "".join(tmp)
    subfix+="----    "
    if Extension == ".py":
        subfix+="Python File"
    elif Extension == ".sh":
        subfix+="Shell Script"
    elif Extension == "pdf":
        subfix+="PDF Document"
    return subfix






if __name__ == "__main__":
    use_subfix=False
    path="."
    if len(sys.argv) == 1:
        path="."
    for index,arg in enumerate(sys.argv):
        if arg[0] == "-":
            if arg[1] == "d":
                path=sys.argv[index+1]
            if arg[1] == "m":
                use_subfix = True

    output(path, use_subfix)
