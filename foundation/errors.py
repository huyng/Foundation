class BaseError(Exception):
    pass

class NameConflict(BaseError):
    def __init__(self, name, conflict_pkgpath):
        BaseError.__init__(self, "The name '%s' conflicts with the package at '%s'" %(name, conflict_pkgpath))
        
class PackageDoesNotExist(BaseError):
    def __init__(self, name):
        BaseError.__init__(self, "The package '%s' does not exist" % name)
        
class IncompatiablePackage(BaseError):
    def __init__(self):
        Exception.__init__(self, "The package must be file based, not directory based")


class ConfigMissing(BaseError):
    def __init__(self):
        BaseError.__init__(self, "Missing config file ~/.evoke/default.conf")

class InvalidTemplatePackage(BaseError):
    def __init__(self, pkgpath, reason=''):
        if reason:
            reason = '(%s) ' % reason
        BaseError.__init__(self, "Invalid Template Package %s%s" % (reason,pkgpath))

