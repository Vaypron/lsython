# Lsython

Lsython is a python implementation of the linux `ls` command.
It aims to later run a database of extensions and specific files, to be able to 
tell you more about a file/directory than just the usual stuff.  

Usage
--------
As simple as 
```
Usage:
        lsython [-d|-g] [path|file] [-h|-f|-s|-m|-i|]
                -d [path]       List directory information
                -g [file]       List file information
                -s [a|m|e]      Sort (a)lphabetically[default] | by (m)odified date | by (e)xtension
                -c              Cut off long filenames to keep format. No cut if set
                -h              Show help page
                -f              Show additional information : file type
                -r              Show additional information : recommended software
                -m              Show additional information : modified date


```

A collections of files to test each flag can be found in the `test_directory`.

Supported OS
--------
* Linux (functionality and design) [tested]
* Windows (functionality) [tested]
* MacOS [not tested yet]



Building/Installing
--------

### Auto-Install with pip

```
Coming soon.
```

### Install with pip (currently recommended)

1. Clone the repository
2. Navigate into the directory and run:
```
pip install .
```

Dependencies
------------

None yet


License
-------

Copyright &copy; 2018 by [Tim Gebauer][vaypron].


This project is licensed under the MIT license, please see the file **LICENSE** for more information.



[vaypron]: https://github.com/Vaypron
