
from hwc_codeElem import HWC_Names



class HWC_File:
    def __init__(self, name):
        self.name = name
        self.decls = []


    def dump(self, pre=""):
        print(pre+"File with the following decls: ")

        # the type changes when we run phase 10.
        if type(self.decls) == list:
            for dec in self.decls:
                print("  File_decl with these decls: ")
                dec.dump(pre+"    ")
        else:
            for name in self.decls:
                print("  File_decl with these decls: ")
                self.decls[name].dump(pre+"    ")


    def do_phase10(self):
        raw_decls = self.decls
        self.decls = HWC_Names(None)

        for dec in raw_decls:
            dec.parent = self
            dec.do_phase10(self.decls)

            name = dec.name
            assert len(name) > 0

            if name in self.decls:
                TODO   #  report duplicate names

            self.decls[name] = dec


    def do_phase20(self):
        TODO


