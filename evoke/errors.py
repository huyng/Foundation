class NameConflict(Exception):
    def __init__(self, name, conflict_pkgpath):
        Exception.__init__(self, "The name '%s' conflicts with the package at '%s'" %(name, conflict_pkgpath))

class ConfigMissing(Exception):
    def __init__(self):
        Exception.__init__(self, "Missing config file ~/.evoke/default.conf")

class InvalidTemplatePackage(Exception):
    def __init__(self, pkgpath, reason=''):
        if reason:
            reason = '(%s) ' % reason
        Exception.__init__(self, "Invalid Template Package %s%s" % (reason,pkgpath))

