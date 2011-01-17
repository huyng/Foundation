#!/usr/bin/env python

import os
import cmdln
import shutil
import subprocess as SP
import os.path as P
import glob as G
import configobj

from functools import wraps
from errors import ConfigMissing, NameConflict, InvalidTemplatePackage



# Monkey patching os.path module to get the real f-ing path
P.wtfpath = lambda p: P.abspath(P.expandvars(P.expanduser(p)))

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
        self.evkpath  = P.join(pkgpath, '.evk')
        self.confpath = P.join(self.evkpath, 'config')
        self.putpath  = putpath
        self.docpath  = P.join(self.evkpath, 'README')

    
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
            shutil.copyfile(self.putpath, dest)
        else:
            shutil.copytree(self.putpath, dest, ignore=shutil.ignore_patterns('*.evk'))

    
    def save(self):
        '''Serialize the config about this template package and save'''
        if not P.exists(self.confpath):
            os.mkdir(self.evkpath)
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
        pkgconfpath = P.join(pkgpath, '.evk/config')
        
        # check path and validity of package
        if not P.exists(pkgpath):
            raise InvalidTemplatePackage(pkgpath, 'path does not exist')
        if not P.exists(pkgconfpath):
            raise InvalidTemplatePackage(pkgpath, 'missing .evk folder')
        
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
        
    @classmethod
    def loadrepo(cls, repopath):
        '''Load all template packages from repository'''
        tpackage_paths = G.glob(P.join(repopath, '*'))
        for pkgpath in tpackage_paths:
            cls.load(pkgpath)



CONFIGPATH = '~/.evoke/config'
class App(cmdln.Cmdln):
    name = 'evk'

    def __init__(self):
        cmdln.Cmdln.__init__(self)

        # load configuration file
        confpath = P.wtfpath(CONFIGPATH)
        if not P.exists(confpath):
            raise ConfigMissing
            
        conf = configobj.ConfigObj(confpath)
        self.repopath = P.wtfpath(conf['repopath'])
        self.completionspath = P.wtfpath(conf['competions'])
        
        # load template packages
        TemplatePackage.loadrepo(self.repopath)
        
        # misc
        self.editor = os.environ.get('EDITOR', 'vi')
    
    @cmdln.alias('p')
    @requires_path           
    def do_put(self, subcmd, opts, *paths):
        '''${cmd_name}: create new project from template'''
        name = paths[0]
        dest = P.wtfpath(paths[1])
        templatepkg = TemplatePackage.pool.get(name)
        templatepkg.put(dest)
    
    @cmdln.alias('clip')
    def do_cliboard(self, subcmd, opts, *paths):
        '''${cmd_name}: copy the contents to clipboard (only valid for file templates)'''
        print paths
        print ''
        
    
    @cmdln.alias('a')
    def do_add(self, subcmd, opts, *paths):
        '''${cmd_name}: add file or folder to your repository of project templates'''
        path    = P.wtfpath(paths[0])
        name    = slugify(P.split(path)[-1].strip(),'-')
        pkgpath = P.join(self.repopath, name)
        
        # check if we've already got the package
        if name in TemplatePackage.pool:
            raise NameConflict(name, TemplatePackage.pool[name].pkgpath)
        
        # copy files into pkgpath
        if P.isfile(path):
            fpath = P.join(pkgpath, name)
            os.mkdir(pkgpath)
            shutil.copyfile(path, fpath)
            templatepkg = TemplatePackage(pkgpath=pkgpath, name=name, putpath=name)
        else:
            shutil.copytree(path, pkgpath)
            templatepkg = TemplatePackage(pkgpath=pkgpath, name=name, putpath='.')
            
        
        templatepkg.save()
    
    @requires_path
    @cmdln.alias('rm')
    def do_remove(self, subcmd, opts, *paths):
        '''${cmd_name}: removes template package NAME from the repository
        
        Usage:
            evk remove NAME
        '''
        name = paths[0]
        templatepkg = TemplatePackage.pool.get(name)
        templatepkg.remove()
        
        

    @cmdln.alias('e')
    @cmdln.option('-c', '--config', action='store_true', dest='config', default=False,
                  help='Edit the configuration file for template package')
    def do_edit(self, subcmd, opts, *paths):
        '''${cmd_name}: edit this project template in your editor
           
           ${cmd_option_list}
        '''
        name = paths[0]
        templatepkg = TemplatePackage.pool.get(name)
        if opts.config:
            SP.call('%s %s' % (self.editor, templatepkg.evkpath), shell=True)
        elif opts.docs:
            SP.call('%s %s' % (self.editor, templatepkg.docpath), shell=True)
        else:
            SP.call('%s %s' % (self.editor, templatepkg.pkgpath), shell=True)
        

    @cmdln.alias('d')
    def do_doc(self, subcmd, opts, *paths):
        '''${cmd_name}: print documentation about the project templates'''
        name = paths[0]
        print ''
        print TemplatePackage.pool.get(name).docs
        

    @cmdln.alias('ls')
    def do_list(self, subcmd, opts, *paths):
        '''${cmd_name}: list all the available templates'''
        templates = TemplatePackage.pool.values()
        maxlen = max(len(i.name) for i in templates)
        print 'template packages:\n'
        print '\n'.join('\t{0:<{maxlen}}\t{1}'.format(i.name, i.docs, maxlen=maxlen) for i in templates)
        
    
    @cmdln.option('-s', '--save', action='store_true', dest='save',
                  help='save the completions to the default completions file')
    def do_compgen(self, subcmd, opts, *paths):
        '''${cmd_name}: generate the completions file
        
           ${cmd_option_list}
        '''
        completions = '\n'.join(TemplatePackage.pool.keys())
        if opts.save:
            f = open(self.completionspath,'w')
            f.write(completions)
            f.close()
            print('saved completions to %s' % self.completionspath)
        else:
            print(completions)
        
        



