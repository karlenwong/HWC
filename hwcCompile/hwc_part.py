
from hwc_codeElem import HWC_CodeElem



class HWC_Part(HWC_CodeElem):
    def __init__(self, name, stmts, start,end):
        super().__init__(start,end)
        self.name  = name
        self.stmts = stmts


