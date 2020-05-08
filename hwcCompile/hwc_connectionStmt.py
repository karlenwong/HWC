
class HWC_ConnectionStmt:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


    def dump(self, pre):
        print(pre+"stmt: CONNECTION, with left and right exprs:")
        dump_expr(self.lhs, pre+"  ")
        dump_expr(self.rhs, pre+"  ")


    def do_phase10(self, public_decls, private_names):
        # no names to record, in a connection statement!
        pass



def dump_expr(ex, pre):
    if type(ex) == str:
        print(pre+"Expr: IDENT, name = {}".format(ex))
        return

    TODO


