#!/usr/bin/env python

import os
import sys
import cmdln
import shutil
import subprocess as SP
import os.path as P
import glob as G
import configobj

from functools import wraps
from errors import ConfigMissing, \
                   NameConflict, \
                   InvalidTemplatePackage, \
                   PackageDoesNotExist, \
                   IncompatiablePackage, \
                   MissingPackageName, \
                   MissingPath



# Monkey patching os.path module to get the real f-ing path
P.wtfpath = lambda p: P.abspath(P.expandvars(P.expanduser(p)))

EMPTY_FILE_LOCATION = P.wtfpath('~/.foundation/datafiles/empty_files')


def requires_path(fn):
    @wraps(fn)
    def _inner(*args, **kwargs):
        assert len(args) + len(kwargs.items()) > 3, 'you must provide a path'
        return fn(*args, **kwargs)
    return _inner    

def slugify(s, char):
    '''removes changes all non [A-Za-z0-9] and changes them to '''
    import re
    return re.sub(r'[^A-Za-z0-9\.\-]+', char, s)
    
class TemplatePackage(object):
    pool = {}
    
    def __init__(self, name, pkgpath, putpath):
        object.__init__(self)
        self.name     = name
        self.pkgpath  = pkgpath
        self.fdnpath  = P.join(pkgpath, '.fdn')
        self.confpath = P.join(self.fdnpath, 'config')
        self.putpath  = putpath
        self.docpath  = P.join(self.fdnpath, 'DESCRIPTION')

    
    @property
    def docs(self):
        f =  open(self.docpath)
        d = f.read()
        f.close()
        return d
    
    def put(self, dest):
        dest = P.wtfpath(dest)
        putpath = P.join(self.pkgpath, self.putpath) if self.putpath else self.pkgpath
        if P.isfile(putpath):
            shutil.copyfile(putpath, dest)
        else:
            shutil.copytree(putpath, dest, ignore=shutil.ignore_patterns('*.fdn'))

    def pbcopy(self):
        if not self.putpath:
            raise IncompatiablePackage
        putpath = P.join(self.pkgpath, self.putpath) if self.putpath else self.pkgpath
        if not P.isfile(putpath):
            raise IncompatiablePackage
        pbcopy = SP.Popen('pbcopy', stdin=SP.PIPE)
        pbcopy.stdin.write(open(putpath).read())
        pbcopy.communicate()
        
    def browse(self):
        SP.call('open %s' % self.pkgpath, shell=True)
        

            

    
    def save(self):
        '''Serialize the config about this template package and save'''
        if not P.exists(self.confpath):
            os.mkdir(self.fdnpath)
        conf            = configobj.ConfigObj()
        conf.filename   = self.confpath
        conf['name']    = self.name
        conf['putpath'] = self.putpath
        conf.write()
        
        # write docs
        f = open(self.docpath,'w')
        f.write(self.docs)
        f.close()
            
        
    @classmethod
    def load(cls, pkgpath):
        '''Load a single template package given a path'''
        pkgpath = P.wtfpath(pkgpath)
        pkgconfpath = P.join(pkgpath, '.fdn/config')
        
        # check path and validity of package
        if not P.exists(pkgpath):
            raise InvalidTemplatePackage(pkgpath, 'path does not exist')
        if not P.exists(pkgconfpath):
            raise InvalidTemplatePackage(pkgpath, 'missing .fdn folder')
        
        conf    = configobj.ConfigObj(pkgconfpath)
        name    = conf['name'].strip()
        putpath = conf['putpath'].strip()
        
        # make sure we don't already have another package with same name
        if conf['name'].strip() in cls.pool:
            raise NameConflict(name, cls.pool[name].path)
        
        # create and add template to pool
        templatepkg = TemplatePackage(
            name=name,
            pkgpath=pkgpath, 
            putpath=putpath)
        
        cls.pool[templatepkg.name] = templatepkg
        
    def remove(self):
        shutil.rmtree(self.pkgpath)
        del TemplatePackage.pool[self.name]
    
    @classmethod
    def create(cls, name, path, repopath):
        path    = P.wtfpath(path) if path else None
        name    = slugify(name,'-') if name else  slugify(P.split(path)[-1].strip(),'-')
        pkgpath = P.join(repopath, name)
        
        # check if we've already got the package
        if name in TemplatePackage.pool:
            raise NameConflict(name, TemplatePackage.pool[name].pkgpath)
        
        # copy files into pkgpath
        if not path:
            # start a new file-based template bundle
            fpath = P.join(pkgpath, name)
            os.mkdir(pkgpath)
            shutil.copyfile(EMPTY_FILE_LOCATION, fpath)
            templatepkg = TemplatePackage(pkgpath=pkgpath, name=name, putpath=name)
        elif P.isfile(path):
            # start a new file-based template bundle from existing file
            fpath = P.join(pkgpath, name)
            os.mkdir(pkgpath)
            shutil.copyfile(path, fpath)
            templatepkg = TemplatePackage(pkgpath=pkgpath, name=name, putpath=name)
        else:
            # start a new folder-based template bundle from existing folder
            shutil.copytree(path, pkgpath)
            templatepkg = TemplatePackage(pkgpath=pkgpath, name=name, putpath=None)

        templatepkg.save()
        return templatepkg
        
        
        
    @classmethod
    def loadrepo(cls, repopath):
        '''Load all template packages from repository'''
        tpackage_paths = G.glob(P.join(repopath, '*'))
        for pkgpath in tpackage_paths:
            cls.load(pkgpath)
    
    @classmethod
    def completegen(cls, completionspath):
        '''generate the completions file'''
        completions = '\n'.join(TemplatePackage.pool.keys())
        f = open(completionspath,'w')
        f.write(completions)
        f.close()

        



CONFIGPATH = '~/.foundation/config'
class App(cmdln.Cmdln):
    name = 'fdn'

    def __init__(self):
        cmdln.Cmdln.__init__(self)

        # load configuration file
        confpath = P.wtfpath(CONFIGPATH)
        if not P.exists(confpath):
            raise ConfigMissing
            
        conf = configobj.ConfigObj(confpath)
        self.repopath = P.wtfpath(conf['repopath'])
        self.completionspath = P.wtfpath(conf['completions'])
        
        # load template packages
        if not P.exists(self.repopath):
            os.mkdir(self.repopath)
        TemplatePackage.loadrepo(self.repopath)
        
        # Generate completions file
        TemplatePackage.completegen(self.completionspath)
        
        # misc
        self.editor = os.environ.get('EDITOR', 'vi')
    
    @cmdln.alias('p')
    def do_put(self, subcmd, opts, *paths):
        '''${cmd_name}: create new project from template'''
        if len(paths) == 0:
            raise MissingPackageName
        elif len(paths) == 1:
            raise MissingPath
        
        dest = P.wtfpath(paths[1])
        
        # get package
        name = paths[0]
        templatepkg = TemplatePackage.pool.get(name)
        if not templatepkg:
            raise PackageDoesNotExist(name)
        
        templatepkg.put(dest)
    
    @cmdln.alias('cc')
    def do_clip(self, subcmd, opts, *paths):
        '''${cmd_name}: copy the contents to clipboard (only valid for file templates)'''
        if len(paths) < 1:
            raise MissingPackageName
            
        # get package
        name = paths[0]
        templatepkg = TemplatePackage.pool.get(name)
        if not templatepkg:
            raise PackageDoesNotExist(name)
            
        templatepkg.pbcopy()
        
    @cmdln.alias('o')
    def do_open(self, subcmd, opts, *paths):
        '''${cmd_name}: copy the contents to clipboard (only valid for file templates)'''
        if len(paths) < 1:
            raise MissingPackageName
        
        # get package    
        name = paths[0]
        templatepkg = TemplatePackage.pool.get(name)
        if not templatepkg:
            raise PackageDoesNotExist(name)
            
        templatepkg.browse()
        
    
    @cmdln.alias('n')
    @cmdln.option('-n','--name', dest='name', help='a name for the package', required=True)
    def do_new(self, subcmd, opts, *paths):
        '''${cmd_name}: add file or folder to your repository of project templates
        
        ${cmd_option_list}
        '''
        templatepkg = TemplatePackage.create(name=opts.name,path=None, repopath=self.repopath)
        TemplatePackage.pool[templatepkg.name] = templatepkg
        TemplatePackage.completegen(self.completionspath)
        
    
    @cmdln.alias('a')
    @cmdln.option('-n','--name', dest='name', help='a name for the package', default=None)
    def do_add(self, subcmd, opts, *paths):
        '''${cmd_name}: add file or folder to your repository of project templates

        ${cmd_option_list}
        '''
        if len(paths) == 0:
            raise MissingPath

        templatepkg = TemplatePackage.create(name=opts.name, path=path[0], repopath=self.repopath)
        TemplatePackage.pool[templatepkg.name] = templatepkg
        TemplatePackage.completegen(self.completionspath)
        
    
        
    
    @cmdln.alias('rm')
    def do_remove(self, subcmd, opts, *paths):
        '''${cmd_name}: removes template package from the repository
        
        Usage:
            fdn remove NAME
        '''
        if len(paths) < 1:
            raise MissingPackageName
            
        # get package
        name = paths[0]
        if not name in TemplatePackage.pool:
            raise PackageDoesNotExist(name)
            
        templatepkg = TemplatePackage.pool[name]
        has_confirmed = raw_input('Type "y" to delete package "%s" at "%s" y/n: ' %(name, templatepkg.pkgpath))
        if has_confirmed == 'y':
            templatepkg.remove()
            TemplatePackage.completegen(self.completionspath)
        else:
            print 'operation canceled'
        
        

    @cmdln.alias('e')
    @cmdln.option('-c', '--config', action='store_true', dest='config', default=False,
                  help='Edit the configuration file for template package')
    def do_edit(self, subcmd, opts, *paths):
        '''${cmd_name}: edit a template package in your editor
           
           ${cmd_option_list}
        '''
        if len(paths) < 1:
            raise MissingPackageName
        
        # get package
        name = paths[0]
        templatepkg = TemplatePackage.pool.get(name)
        if not templatepkg:
            raise PackageDoesNotExist(name)

        if opts.config:
            SP.call('%s %s' % (self.editor, templatepkg.fdnpath), shell=True)
        else:
            SP.call('%s %s' % (self.editor, templatepkg.pkgpath), shell=True)
    
    @cmdln.alias('l')
    def do_locate(self, subcmd, opts, *paths):
        '''${cmd_name}: print the location of template package. use this to cd into the directory

           ${cmd_option_list}
        '''
        if len(paths) < 1:
            raise MissingPackageName

        # get package
        name = paths[0]
        templatepkg = TemplatePackage.pool.get(name)
        if not templatepkg:
            raise PackageDoesNotExist(name)
        sys.stdout.write(templatepkg.pkgpath + '\n')
    

    @cmdln.alias('d')
    def do_doc(self, subcmd, opts, *paths):
        '''${cmd_name}: print documentation about the template packages'''
        if len(paths) < 1:
            raise MissingPackageName
            
        # get package
        name = paths[0]
        templatepkg = TemplatePackage.pool.get(name)
        if not templatepkg:
            raise PackageDoesNotExist(name)
        
        print ''
        print templatepkg.docs
        

    @cmdln.alias('ls')
    def do_list(self, subcmd, opts, *paths):
        '''${cmd_name}: list all the available templates'''
        templates = [i[1] for i in sorted(TemplatePackage.pool.items())]
        if templates:
            maxlen = max(len(i.name) for i in templates)
            print 'Template packages:\n'
            print '\n'.join('\t{0:<{maxlen}}\t\t{1}'.format(i.name, i.docs, maxlen=maxlen) for i in templates)
        else:
            print 'No packages available'
        
        



