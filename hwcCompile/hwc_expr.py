
from hwc_codeElem import HWC_CodeElem



class HWC_BaseExpr(HWC_CodeElem):
    def __init__(self, start,end, raw):
        super().__init__(start,end)
        self.raw = raw



class HWC_UnaryExpr(HWC_CodeElem):
    def __init__(self, start, op, base):
        super().__init__(start, base.end)
        self.op   = op
        self.base = base



class HWC_BinaryExpr(HWC_CodeElem):
    def __init__(self, lhs, op, rhs):
        super().__init__(lhs.start, rhs.end)
        self.lhs = lhs
        self.op  = op
        self.rhs = rhs



class HWC_ArrayIndexExpr(HWC_CodeElem):
    def __init__(self, base, indx, suffixEnd):
        super().__init__(base.start, suffixEnd)
        self.base = base
        self.indx = indx



class HWC_ArraySliceExpr(HWC_CodeElem):
    def __init__(self, base, indx1, indx2, suffixEnd):
        super().__init__(base.start, suffixEnd)
        self.base  = base
        self.indx1 = indx1
        self.indx2 = indx2



#    def dump(self, pre=""):
#        print(pre+"File with the following decls: ")
#
#        # the type changes when we run phase 10.
#        if type(self.decls) == list:
#            for dec in self.decls:
#                print("  File_decl with these decls: ")
#                dec.dump(pre+"    ")
#        else:
#            for name in self.decls:
#                print("  File_decl with these decls: ")
#                self.decls[name].dump(pre+"    ")


#    def do_phase20(self):
#        TODO


