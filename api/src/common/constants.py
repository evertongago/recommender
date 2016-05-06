def constant(f):
    def fset(self, value):
        """ Error """

    def fget(self):
        return f()

    return property(fget, fset)

class Const(object):
    @constant
    def NOT_FOUND():
        return 404

    @constant
    def BAD_REQUEST():
        return 400

    @constant
    def OK():
        return 200
