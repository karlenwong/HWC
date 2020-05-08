from hwc_file import HWC_File
from hwc_part import HWC_Part
from hwc_plug import HWC_Plug
from hwc_decl import HWC_Decl

from hwc_connectionStmt import HWC_ConnectionStmt



def parse(infile):
    retval = HWC_File("__main__")

    try:
        tokens = pushbackable(tokenize(infile))
        for tok,start,end in tokens:
            if tok == TOK(";"):
                pass   # a bare semicolon - or one after a declaration, is a NOP

            if tok == TOK("part"):
                retval.decls.append(parse_PartPlug(tokens, start, part=True))
            elif tok == TOK("plug"):
                retval.decls.append(parse_PlugPlug(tokens, start, part=False))
            else:
                assert False    # TODO: report syntax error

    except Exception as e:
        print(e)
        TODO   # do better error handling!

    return retval



def parse_PartPlug(tokens, start, part):
    name,_ignore1,_ignore2 = next(tokens)
    if type(name) != str:
        TODO

    tok,_ignore1,_ignore2 = next(tokens)
    if tok != TOK("{"):
        TODO

    if part:
        decls = parse_Part_Stmts(tokens)
    else:
        decls = parse_Plug_Stmts(tokens)

    tok,_ignore1,end = next(tokens)
    if tok != TOK("}"):
        TODO

    if part:
        return HWC_Part(name, decls, start,end)
    else:
        return HWC_Plug(name, decls, start,end)



def parse_Part_Stmts(tokens):
    retval = []

    while True:   # break out when we find something we can't parse as a statement
        tok,start,end = next(tokens)

        if tok == TOK(";"):
            continue   # NOP

        if tok == TOK("public"):
            retval.append(parse_Decl(tokens, start, isPublic=True))
            continue

        if tok == TOK("private"):
            retval.append(parse_Decl(tokens, start, isPublic=False))
            continue

        if tok == TOK("subpart"):
            retval.append(parse_Subpart_decl(tokens, start))
            continue

        if tok == TOK("for"):
            retval.append(parse_For(tokens, start))
            continue

        if type(tok) == str:
            tokens.pushback_last()
            retval.append(parse_single_statement(tokens))
            continue

        # is this the end of the statements?
        if tok == TOK("}"):
            tokens.pushback_last()
            break

        TODO   # handle syntax error

    return retval



def parse_Plug_Stmts(tokens):
    retval = []

    while True:   # break out when we find something that we can't parse as a declaration
        tok,start,end = next(tokens)

        if tok == TOK(";"):
            continue   # NOP

        if type(tok) != str:
            tokens.pushback_last()
            decl = parse_Decl(tokens, True, start)
            if decl.isMemory:
                TODO
            retval.append(retval)

    return retval



def parse_Decl(tokens, start, isPublic):
    (tok,ignored1,ignored2) = next(tokens)
    if tok == TOK("memory"):
        isMemory = True
        (tok,_ignore1,_ignore2) = next(tokens)
    else:
        isMemory = False
        tokens.pushback_last()

    type_ = parse_Type(tokens)

    name,_ignored1,ignored2 = next(tokens)

    after_name,_ignored,end = next(tokens)

    if after_name == TOK("["):
        TODO

    if after_name != TOK(";"):
        print(after_name)
        print(start)
        print(end)
        TODO

    return HWC_Decl(name, type_, isPublic, isMemory)



def parse_Type(tokens):
    tok,start,end = next(tokens)

    if tok == TOK("bit") or type(tok) == str:
        retval = tok
    else:
        TODO

    type_suffix,ignored1,ignored2 = next(tokens)

    if type_suffix == TOK("["):
        TODO
    # not an array, I guess!
    tokens.pushback_last()

    return retval



def parse_single_statement(tokens):
    # someday, we might support function calls.  But otherwise, all statements
    # here are connection statements.

    lhs = parse_Expr(tokens)

    eq,ignored1,ignored2 = next(tokens)
    if eq != TOK("="):
        TODO

    rhs = parse_Expr(tokens)

    semi,ignored1,end = next(tokens)
    if semi != TOK(";"):
        TODO

    return HWC_ConnectionStmt(lhs, rhs)



# Expr1: comparison operators
def parse_Expr(tokens):
    lhs = parse_Expr2(tokens)

    op,ignored1,ignored2 = next(tokens)
    if op not in map(TOK, ["==","!=","<","<=",">",">="]):
        tokens.pushback_last()
        return lhs

    rhs = parse_Expr2(tokens)
    TODO

# NOTE: we skipped the Expr2 from the old Bison parser - because we've replaced
#       the :: operator with the (Pythonic) + operator.

# Expr2: mathematical and boolean/bitwise operators
def parse_Expr2(tokens):
    lhs = parse_Expr3(tokens)

    # loop, handling more and more expressions of this form, as
    # left-associative; we break out when we find something which
    # is not one of our operators.
    while True:
        op,ignored1,ignored2 = next(tokens)
        if op not in map(TOK, ["&","&&", "|","||", "^", "+", "-", "*", "/", "%"]):
            tokens.pushback_last()
            return lhs

        rhs = parse_Expr3(tokens)
        TODO   # build the expression

# Expr3: Unary prefix operators (bitwise and logical negation; arithmetic
#        negation happens later)
def parse_Expr3(tokens):
    tok,start,ignored = next(tokens)
    if tok not in [TOK("!"), TOK("~")]:
        tokens.pushback_last()
        return parse_Expr4(tokens)

    base = parse_Expr3(tokens)    # can recurse, though that would be odd code!
    TODO

# Expr4: array indexing and slicing.  Also left-associative, like Expr2 above.
def parse_Expr4(tokens):
    base = parse_Expr5(tokens)

    while True:
        suff,ignored1,ignored2 = next(tokens)
        if suff != TOK("["):
            tokens.pushback_last()
            return base

        TODO

# Expr5: dot.  Once again, we've got a left-associative rule
def parse_Expr5(tokens):
    base = parse_Expr6(tokens)

    while True:
        dot,ignored1,ignored2 = next(tokens)
        if dot != TOK("."):
            tokens.pushback_last()
            return base

        TODO

# Expr6: arithmetic negation
def parse_Expr6(tokens):
    minus,start,ignored = next(tokens)
    if minus != TOK("-"):
        tokens.pushback_last()
        return parse_Expr7(tokens)

    base = parse_Expr6(tokens)   # again, recursion is odd but legal

# Expr7: parens
def parse_Expr7(tokens):
    paren,start,ignored = next(tokens)
    if paren != TOK("("):
        tokens.pushback_last()
        return parse_Expr8(tokens)

    content = parse_Expr(tokens)

    paren,ignored,end = next(tokens)
    if paren != TOK(")"):
        TODO   # report syntax error

    TODO

# Expr8: base expressions
def parse_Expr8(tokens):
    tok,start,end = next(tokens)

    if type(tok) in [str,int] or tok in [TOK("true"),TOK("false")]:
        return tok

    TODO   # the old Bison parser also parsed "bit" and "flag".  Do we want to do that here???  I think probably not, since we now have an unambiguous type expression.







def tokenize(infile):
    lineNo = 0

    in_comment = False

    for line in infile:
        lineNo += 1
        line_wid = len(line)

        while line != "":
            col = 1 + (line_wid-len(line))

            if line[0].isspace():
                line = line[1:]
                continue

            if in_comment and not line.startswith("*/"):
                line = line[1:]
                continue

            if line[0].startswith("/*"):
                assert not in_comment
                in_comment = True
                line = line[2:]
                continue

            if line[0].startswith("//"):
                break    # ignore the rest of this line!


            # if we get here, then we *DEFINITELY* are going to report a token
            # (or a syntax error).  Each of these paths will set the 'val'
            # field, and must also set the 'count' length.

            if line[0] == '_' or line[0].isalpha():
                count = 1
                while count < len(line) and (line[count] == '_' or line[count].isalnum()):
                    count += 1
                val = line[:count]

                # is this "identifier" actually a keyword?
                if val in ["part", "plug",
                           "public", "private", "subpart",
                           "memory",
                           "for",
                           "if", "else",
                           "assert",
                           "true", "false",
                           "bit", "flag", ]:
                    val = TOK(val)

            elif line.startswith("0x"):
                count = 2
                while count < len(line) and line[count] in "_0123456789aAbBcCdDeEfF":
                    count += 1
                val = int(line[:count], base=16)

            elif line[0].isnumeric():
                count = 1
                while count < len(line) and line[count] in "_0123456789":
                    count += 1

                if line[0] == '0':
                    val = int(line[:count], base=8)   # includes the simple '0' literal
                else:
                    val = int(line[:count])

            else:
                operators = ["<<", ">>",
                             "&&", "||",
                             "==", "!=",
                             "<=", "<", ">=", ">" ] + \
                             list("(){}[]+-*/%=:;,.!~&|^<>")
                val = None
                for op in operators:
                    if line.startswith(op):
                        val = TOK(op)
                        count = len(op)
                        break
                assert val is not None    # TODO: report syntax error

            yield (val, (lineNo,col), (lineNo,col+count-1))
            line = line[count:]



# use this to wrap up a string that represents a keyword or operator.
class TOK:
    def __init__(self, txt):
        self.txt = txt

    def __eq__(self, other):
        if not isinstance(other,TOK):
            return False
        return self.txt == other.txt

    def __str__(self):
        return "TOK({})".format(self.txt)



class pushbackable:
    def __init__(self, stream):
        self.stream = iter(stream)
        self.pushed_back = []

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.pushed_back) != 0:
            retval = self.pushed_back.pop()
        else:
            retval = next(self.stream)
        self.last = retval
        return retval

    def pushback(self, val):
        self.pushed_back.append(val)

    def pushback_last(self):
        self.pushback(self.last)


