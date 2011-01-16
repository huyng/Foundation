#!/usr/bin/env python
import os
import sys
import cmdln
import shutil
import subprocess as sp
import os.path as P

class NameConflict(Exception):
    def __init__(self):
        Exception.__init__(self, "Two project templates have been created with the same name")


class ProjectTemplate(object):
    pool = {}
    
    def __init__(self, path, name, docs=None):
        object.__init__(self)
        self.path = path
        self.is_file = P.isfile(path)
        self.name = name
        self.docs = docs
        if name not in self.pool:
            self.pool[name] = self
        else:
            raise NameConflict
    
    def copy(self, dest):
        if self.is_file:
            shutil.copyfile(self.path, dest)
        else:
            shutil.copytree(self.path, dest)
    
    def genconfig(self):
        '''serialize the config about this project template into'''
        pass
    
    @classmethod
    def checkpool(cls):
        '''test to make sure all current paths exist'''
        pass
        
    @classmethod
    def load(cls):
        '''test to make sure all current paths exist'''
        pass

from functools import wraps
def requires_path(fn):
    @wraps(fn)
    def _inner(*args, **kwargs):
        assert len(args) + len(kwargs.items()) > 3, 'you must provide a path'
        return fn(*args, **kwargs)
    return _inner    
        
class App(cmdln.Cmdln):
    name = 'evoke'
    editor = 'mate'
    repopath = '~/.evoke/templates'
    
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
        path = P.absolute(P.expandvars(paths[0]))
        if P.isfile(path):
            name = P.split(path)[-1]
            shutil.copyfile(path, P.join(self.repopath))
        else:
            shutil.copytree(path, self.repopath)
    
    @requires_path
    @cmdln.alias('u')
    def do_uninstall(self, subcmd, opts, *paths):
        '''${cmd_name}: uninstalls [name] template from the repository'''
        pass
        

    # @requires_path
    @cmdln.alias('e')
    @cmdln.option('-c', '--config', action='store_true', dest='config', default=False,
                  help=('Edit the configuration file templates instead of the actual'
                        'templates themselves'))
    def do_edit(self, subcmd, opts, *paths):
        '''${cmd_name}: edit this project template in your editor
           ${cmd_option_list}
        '''
        name = paths[0]
        projtpl = ProjectTemplate.pool.get(name)
        sp.Popen('%s %s' % (self.editor, projtpl.path))
        
    @requires_path
    @cmdln.alias('d')
    def do_doc(self, subcmd, opts, *paths):
        '''${cmd_name}: print documentation about the project templates'''
        name = paths[0]
        print ProjectTemplate.pool.get(name).docs
        
    @cmdln.alias('ls')
    def do_list(self, subcmd, opts, *paths):
        '''${cmd_name}: list all the available templates'''
        templates = ProjectTemplate.pool.values()
        maxlen = max(len(i) for i in templates)
        print ''
        print '\n'.join('{0:<{maxlen}}\t{1}'.format(i.name, i.doc, maxlen=maxlen) for i in templates)
        
    
    @cmdln.option('-s', '--save', action='store_true', dest='save',
                  help='save the completions to the default completions file')
    def do_compgen(self, subcmd, opts, *paths):
        '''${cmd_name}: generate the completions file
            
           ${cmd_option_list}
        '''
        print '\n'.join(ProjectTemplate.pool.keys())
        
        



