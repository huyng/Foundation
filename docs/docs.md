## About Foundation ##

Foundation is a scaffolding tool. It tracks your often-used project templates, code snippets and other 
boilerplate in an easy-to-use commandline app. With a single command, generate exactly the source code
you need for starting new projects.

**Features:**

- Tab completion
- Post processing hooks
- No-hassle editing - so your code will always stay up-to-date
- Bundling - easily package your code to distribute to others

**Usage:**
 
    Usage:
        fdn COMMAND [ARGS...]
        fdn help [COMMAND]
        
    Options:
        -h, --help  show this help message and exit
        
    Commands:
        add (a)        add file or folder to your repository of project templates
        bundle         Create a fdn bundle to distribute
        cdpath (cd)    print the location of template package. use this to cd i...
        clip (cc)      copy the contents to clipboard (only valid for file temp...
        doc (d)        print documentation about the template packages
        edit (e)       edit a template package in your editor
        help (?)       give detailed help on a specific sub-command
        list (ls)      list all the available templates
        new (n)        add file or folder to your repository of project templates
        open (o)       copy the contents to clipboard (only valid for file temp...
        put (p)        create new project from template
        remove (rm)    removes template package from the repository
    

## Getting Started ##
    
**Installation**

    git clone git://github.com/huyng/Foundation.git
    
    cd Foundation
    python setup.py install --user
    
    # Add this to your .bashrc or .profile
    source ~/.foundation/foundation.sh
    
**Example Usage**

Create sample bundle and add to repository

    mkdir newproject
    echo 'hello world' > newproject/foobar.txt
    fdn add newproject --name "fdn-hello-world"
    
Generate a new project from previously added bundle

    fdn put fdn-hello-world /tmp/helloworld

Edit your bundle
    
    fdn edit fdn-hello-world

Remove the bundle
    
    fdn rm fdn-hello-world
    

## Command Reference ##

#### add (a) ####

Adds a DIRECTORY or FILE path to your personal repository of code snippets and project templates
    
    Usage:
        fdn add <DIRECTORY> | <FILE> | <FDNBUNDLE>
    
    Options:
        -n NAME, --name=NAME
                            a name for the package (defaults to the folder or file name)

    Example:
                                    
        fdn add MyNewDjangoProject -n "django-hello-world"
        
        fdn add snippets.txt
        
        fdn add kylesproject.fdnbundle

#### new (n) ####

Creates a new file-based bundle package and opens up in your editor.

    Usage:
        fdn new `<NAME>` 
    
    Example:
    
        fdn new your-new-bundle-name

#### put (p) ####

Copies the bundle `<NAME>` from your personal repository into the given `<PATH>`. 
    
    Usage:
        fdn put <NAME> <PATH>
    
    Example:
        
        fdn put django-hello-world /tmp/newproject
    
#### list (ls) ####

List all available bundles in your repository
    
    Usage:
        fdn list

#### remove (rm) ####

Removes the package `<NAME>` from your repository
    
    Usage:
        fdn remove <NAME>
    
    Example:
    
        fdn rm crufty-piece-of-code
    
#### edit (e) ####

Opens the bundle package `<NAME>` from your repository in your editor of choice.
    
    Usage:
        fdn edit <NAME>
    
    Options:
        -c, --config  Edit the configuration file for template package
    
    Example:
    
        fdn edit myproject
        
        fdn edit myproject -c
    
#### open (o) ####

Reveal package `<NAME>` from your repository in Finder
    
    Usage:
        fdn open <NAME>
    
    Example:
    
        fdn edit myproject


#### bundle ####

Packages the bundle `<NAME>` from your repository into zip file that you can distribute to other developers

    Usage:
        fdn bundle `<NAME>`
    
    Example:
        
        fdn bundle yourproject
    

#### cdpath (cd) ####

Print the directory location of the bundle package `<NAME>`. Use this to quickly jump to the package's directory.
    
    Usage:
        fdn cdpath <NAME>
    
    Example:
        
        cd `fdn cdpath myproject`

There's also a bash function that you can use that is equivalent to the above command. 
    
    fdncd <NAME>
        
#### doc (d) ####

Print the documentation for the package <NAME> that is stored in its DESCRIPTION file
    
    Usage:
        fdn doc <NAME>
    
    Example:
    
        fdn doc myproject
    
#### clip (cc) ####

Copy the contents of a bundle package `<NAME>` into clipboard (must be file based not directory based)

    Usage:
        fdn clip <NAME>
    
    Example:
    
        fdn clip my-snippets-file


## Configuration ##

- All relevant files for this command live under **~/.foundation/**. 
- All bundle packages are folders that reside in **~/.foundation/repository**.
- All bundle packages contain an **.fdn** direcotry 
- Each **.fdn** directory contains a *config* file which has settings such as the "name" of a package and the files that should be copied when using the `put` command.
- Each **.fdn** directory contains a *DESCRIPTION* file which contains the description to be printed out when using the `doc` command.
- Each **.fdn** directory optionally contains a *hooks* directory where you can place scripts that FDN will execute during certain events. FDN currently only supports the "post-put" hook. 

## Related Pages ##

- [FDN Project Homepage](http://www.huyng.com/projects/fdn/)
- [FDN Github Repository](https://github.com/huyng/Foundation)
- [Author's Homepage](http://www.huyng.com)

## License ##

Copyright (C) Huy Nguyen 2011 

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


