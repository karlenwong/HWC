
from hwc_codeElem import HWC_CodeElem,HWC_Names

from hwc_decl import HWC_Decl



class HWC_Part(HWC_CodeElem):
    def __init__(self, name, stmts, start,end):
        super().__init__(start,end)
        self.name  = name
        self.stmts = stmts


    def dump(self, pre):
        print(pre+"Part_decl: named '{}', with stmts: ".format(self.name))
        for s in self.stmts:
            s.dump(pre+"  ")


    def do_phase10(self, file_public_names):
        raw_stmts = self.stmts
        self.stmts = []

        self.decls     = HWC_Names(None)
        self.prv_names = HWC_Names(file_public_names)

        for s in raw_stmts:
            s.do_phase10(self.decls, self.prv_names)


