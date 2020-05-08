
class HWC_CodeElem:
    def __init__(self, start,end):
        self.start = start
        self.end   = end



# this is basically a dictionary, but with a recursive structure, and
# write-once functionality.
class HWC_Names:
    def __init__(self, parent):
        self.parent = parent
        self.names  = {}

    def __contains__(self, name):
        if name in self.names:
            return True
        if self.parent is None:
            return False
        return name in self.parent

    def __setitem__(self, name, val):
        assert name not in self
        self.names[name] = val

    def __getitem__(self, name):
        if name in self.names:
            return self.names[name]
        if self.parent is None:
            raise IndexError(name)
        return self.parent[name]
            


