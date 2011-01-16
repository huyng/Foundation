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
    return re.sub(r'[^A-Za-z0-9]+', char, s)
    
class TemplatePackage(object):
    pool = {}
    
    def __init__(self, path, name, docs=None):
        object.__init__(self)
        self.path = path
        self.evkpath = P.join(path, '.evk')
        self.confpath = P.join(self.evkpath, 'config')
        self.is_file = P.isfile(path)
        self.name = name
        self.docs = docs
    
    def copy(self, dest):
        if self.is_file:
            shutil.copyfile(self.path, dest)
        else:
            shutil.copytree(self.path, dest)
    
    def save(self):
        '''Serialize the config about this template package and save'''
        
        pass
    
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
        
        conf = configobj.ConfigObj(pkgconfpath)
        
        # make sure we don't already have another package with same name
        if conf['name'].strip() in cls.pool:
            raise NameConflict(conf['name'].strip(), cls.pool[conf['name'].strip()].path)
        
        # create and add template to pool
        templatepkg = TemplatePackage(
            path=pkgpath, 
            name=conf['name'].strip(), 
            docs=conf.get('docs', None))
        
        cls.pool[templatepkg.name] = templatepkg
        
        
        
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
        self.repopath = P.abspath(P.expandvars(P.expanduser(self.conf['repopath'])))
        
        # load template packages
        TemplatePackage.loadrepo(self.repopath)
        
        # misc
        self.editor = os.environ.get('editor', 'vi')
    
    @cmdln.alias('p')
    @requires_path           
    def do_put(self, subcmd, opts, *paths):
        '''${cmd_name}: create new project from template'''
        print paths
        print ''
    
    @cmdln.alias('clip')
    def do_cliboard(self, subcmd, opts, *paths):
        '''${cmd_name}: copy the contents to clipboard (only valid for file templates)'''
        print paths
        print ''
        
    
    @requires_path
    @cmdln.alias('i')
    def do_install(self, subcmd, opts, *paths):
        '''${cmd_name}: add [path] to your repository of project templates'''
        path = P.wtfpath(paths[0])
        if P.isfile(path):
            name = P.split(path)[-1]
            name = slugify(name.strip())
            pkgpath = P.join(self.repopath, name)
            shutil.copyfile(path)
        else:
            shutil.copytree(path, self.repopath)
    
    @requires_path
    @cmdln.alias('u')
    def do_uninstall(self, subcmd, opts, *paths):
        '''${cmd_name}: uninstalls [name] template from the repository'''
        pass
        

    @requires_path
    @cmdln.alias('e')
    @cmdln.option('-c', '--config', action='store_true', dest='config', default=False,
                  help=('Edit the configuration file templates instead of the actual'
                        'templates themselves'))
    def do_edit(self, subcmd, opts, *paths):
        '''${cmd_name}: edit this project template in your editor
           ${cmd_option_list}
        '''
        name = paths[0]
        projtpl = TemplatePackage.pool.get(name)
        SP.Popen('%s %s' % (self.editor, projtpl.path))
        

    @requires_path
    @cmdln.alias('d')
    def do_doc(self, subcmd, opts, *paths):
        '''${cmd_name}: print documentation about the project templates'''
        name = paths[0]
        print TemplatePackage.pool.get(name).docs
        

    @cmdln.alias('ls')
    def do_list(self, subcmd, opts, *paths):
        '''${cmd_name}: list all the available templates'''
        templates = TemplatePackage.pool.values()
        maxlen = max(len(i) for i in templates)
        print ''
        print '\n'.join('{0:<{maxlen}}\t{1}'.format(i.name, i.doc, maxlen=maxlen) for i in templates)
        
    
    @cmdln.option('-s', '--save', action='store_true', dest='save',
                  help='save the completions to the default completions file')
    def do_compgen(self, subcmd, opts, *paths):
        '''${cmd_name}: generate the completions file
           ${cmd_option_list}
        '''
        print '\n'.join(TemplatePackage.pool.keys())
        
        



