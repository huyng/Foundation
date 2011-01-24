[TOC]

## hello ##


## About Foundation ##

Foundation is a scaffolding tool. It tracks your often-used project templates, code snippets and other 
boilerplate in an easy-to-use commandline app. With a single command, generate exactly the source code
you need for starting new projects.

    Usage:
        fdn COMMAND [ARGS...]
        fdn help [COMMAND]

    Options:
        -h, --help  show this help message and exit

    Commands:
        add (a)          add file or folder to your repository of project templates
        clip (cc)        copy the contents of a file-based bundle to clipboard 
        doc (d)          print documentation about the template packages
        edit (e)         edit a template package in your editor
        open (o)         open the directory where the package resides
        help (?)         give detailed help on a specific sub-command
        list (ls)        list all the available templates
        locate (l)       print the directory location of the template package
        put (p)          create new project from template
        remove (rm)      removes template package from the repository
        new (n)          start a new file-based template package

        

## Getting Started ##
    
    # Download source
    git clone git://github.com/huyng/Foundation.git
    
    # Install
    python setup.py install --user
    
    # Add this to your .bashrc or .profile
    source ~/.foundation/foundation.sh
    
    # Create sample package and add to repository
    mkdir samplepackage
    echo "hello world" > samplepackage/test.txt
    fdn add samplepackage
    
    # Generate a new project from previously added scaffold
    cd /tmp
    fdn put samplepackage samplepackage2
    



## Usage Reference ##

**add**

Adds a DIRECTORY or FILE path to your personal repository of code snippets and project templates

    fdn add <DIRECTORY> | <FILE>

**put**

Copies the package NAME from your personal repository into the given PATH

    fdn put <NAME> <PATH>
    
**list**

List the packages available in your repository

    fdn ls

**remove**

Removes the package NAME from your repository
    
    fdn remove <NAME>
    
**edit**

Edit the package NAME from your repository
    
    fdn edit <NAME>
    
**open**

Reveal package NAME from your repository in Finder
    
    fdn open <NAME>
    
**locate**

print the directory location of the template package (use this to quickly jump to the package's directory)

    fdn locate <NAME>

**doc**

Print the documentation for the package <NAME>

    fdn doc <NAME>
    
**clip**

Copy the contents of a package into clipboard (must be file based not directory based)

    fdn clip <NAME>

**help**

Print help message for the given COMMAND

    fdn help <COMMAND> 

## Configuration ##

- All relevant files for this command live under **~/.foundation/**. 
- All template packages are folders that reside in **~/.foundation/repository**.
- All template packages contain an **.fdn** direcotry 
- Each **.fdn** directory contains a *config* file which has settings such as the "name" of a package and the files that should be copied when using the `put` command.
- Each **.fdn** directory contains a *DESCRIPTION* file which contains the description to be printed out when using the `doc` command.

# License #

Copyright (C) Huy Nguyen 2011 

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


    

