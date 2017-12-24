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


Extensions = {'.pdf': 'PDF document', '.py': 'Python file', '.exe': 'Windows executable', '.cpp': 'C++ source file',
              '.h': 'C++ header file', 'hpp': 'C++ file', '.js': 'JavaScript file', '.html': 'HTML file',
              '.css': 'CSS design file', '.sh': 'Shell script', '.txt': 'Text file', '.aif': 'AIF audio file',
              '.cda': 'CD audio track file', '.midi': 'MIDI audio file', '.mp3': 'MP3 audio file',
              '.mpa': 'MPEG-2 audio file', '.ogg': 'Ogg Vorbis audio file', '.wav': 'WAV audio file',
              '.wpl': 'Windows Media Player playlist', '.7z': '7-zip compressed file', '.arj': 'ARJ compressed file',
              '.deb': 'Debian software package file', '.pkg': 'Package file', '.rar': 'RAR archive',
              '.rpm': 'Red Hat Package Manager', '.tar': 'TAR compressed file', '.gz': 'Gunzip compressed file',
              '.tar.gz': 'Tarball compressed file', '.z': 'Z compressed file', '.zip': 'ZIP compressed file',
              '.bin': 'Binary file', '.dmg': 'macOS X disk image', '.iso': 'ISO disc image',
              '.toast': 'Toast disc image', '.vcd': 'Virtual CD', '.csv': 'Comma separated value file',
              '.dat': 'Data file','.db': 'Database file','.log': 'Log file', '.mdb': ' Microsoft Access database file',
              '.sav': 'Save file','.sql': 'SQL database file', '.xml': 'XML file', '.apk': 'Android package file',
              '.bat': 'Batch file', '.cgi' : 'Common gateway interface executable', '.com':'MS-DOS command file',
              '.jar':'Java archive file', '.wsf': 'Windows script File', '.fnt': 'Windows font file',
              '.fon': 'Generic font file', 'otf': 'Open type font file', '.ttf': 'TrueType font file',
              '.ai': 'Adobe Illustrator file', '.bmp': 'Bitmap image', '.gif': 'GIF File', '.ico': 'Icon file',
              'jpeg': 'JPEG image', '.jpg':'JPEG image', '.png': 'PNG image', '.ps': 'PostScript file',
              '.psd': 'PSD image','.svg': 'Scalable vector graphics file', '.tif': 'TIFF image', '.tiff': 'TIFF image',
              '.php': 'PHP file', '.rss': 'RSS file', '.key':'Keynote presentation',
              '.odp': 'OpenOffice Impress presentation file', '.pps':'PowerPoint slide show',
              '.ppt': 'PowerPoint presentation', '.pptx': 'PowerPoint open XML presentation',
              '.class': 'Java class file', '.vb': 'Visual Basic file', '.swift': 'Swift source code file',
              '.java':'Java source code file', '.bak' : 'Backup file', '.cab': 'Windows cabinet file',
              '.cfg': 'Configuration file', '.config': 'Configuration file', '.cpl': 'Windows Control panel file',
              '.cur': 'Windows cursor file', '.dll' : 'Dynamic link library', '.dmp': 'Dump file',
              '.drv': 'Device driver file', '.icns': 'macOS X icon resource file', '.ico': 'Icon file',
              '.ini': 'Initialization file', '.lnk': 'Windows shortcut file', '.msi': 'Windows installer package',
              '.sys': 'Windows system file', '.tmp': 'Temporary file', '.avi': 'AVI video file',
              '.flv': 'Adobe flash file', '.h265': 'H.264 video file', '.m4v': 'Apple MP4 video file',
              '.mkv': 'Matroska Multimedia Container', '.mp4': 'MPEG4 video file', '.mpg': 'MPEG video file',
              '.mpeg': 'MPEG video file', '.rm': 'RealMedia file', '.swf': 'Shockwave flash file',
              '.vob': 'DVD Video Object', '.wmv': 'Windows Medio Video file'}


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def files(path):
    items = {"visible": {"dirs": [], "files": []}, "invisible": {"dirs": [], "files": []}}

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
