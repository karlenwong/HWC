


class HWC_Decl:
    def __init__(self, name, type_, isPublic, isMemory):
        self.name = name
        self.type = type_
        self.isPublic = isPublic
        self.isMemory = isMemory


    def dump(self, pre):
        print(pre+"stmt: DECL:")
        print(pre+"  type:")
        dump_type(self.type, pre+"    ")
        print(pre+"  prefix={}".format( "public" if self.isPublic else "private" ))
        print(pre+"  isMemory={}".format( 1 if self.isMemory else 0 ))
        print(pre+"  name: "+self.name)


    def do_phase10(self, public_decls, private_names):
        if self.name in private_names:
            TODO   # report duplicate name error

        private_names[self.name] = self
        if self.isPublic:
            public_decls[self.name] = self



def dump_type(tp, pre):
    if type(tp) == str:
        TODO    # does this ever happen?

    tp.dump(pre)


