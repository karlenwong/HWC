
from hwc_codeElem import HWC_CodeElem



class HWC_BitType(HWC_CodeElem):
    def __init__(self, start,end):
        super().__init__(start,end)

    def dump(self, pre):
        print(pre+"bit")



# used for all IDENT types - that is, user-defined names, before phase 20
class HWC_UnresolvedType(HWC_CodeElem):
    def __init__(self, start,end, txt):
        super().__init__(start,end)
        self.txt = txt



# used for all array types.  Can be a wrapper around UnresolvedType
class HWC_ArrayType(HWC_CodeElem):
    def __init__(self, baseType, count, suffixEnd):
        super().__init__(baseType.start, suffixEnd)
        self.baseType = baseType
        self.count    = count


