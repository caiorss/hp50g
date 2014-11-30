#!/usr/bin/python
# author: doug@neverfear.org
# date: 09/04/2007
# date: 02/03/2010: Cleaned code up a bit, added some syntactical checks.
#
# Implementation of infix to postfix conversation.
# based around the shunting yard algorithm
# see http://en.wikipedia.org/wiki/Shunting_yard_algorithm
# for more information
#
# Long code because of all the verbose prints
#
# Example usage
# $ ./infixtopostfix.py "(8 * 5) / 4"
#
# Ultra verbose usage with multiple expressions:
# $ ./infixtopostfix.py -v -v -v "(8 * 5) / 4" "1+(42 +31)+1" "5+1"
#
 
import sys
 
 
formattingops    = ['(', ')']
associative      = ["*", "+"]
leftassociative  = ["-", "/"]
rightassociative = ["^"]
operators        = formattingops + associative + leftassociative + rightassociative
arithmeticops    = associative + leftassociative + rightassociative
precedence       = {} # high value == high precedence
precedence["^"]  = 3 
precedence["+"]  = 1
precedence["-"]  = 1
precedence["*"]  = 2
precedence["/"]  = 2
precedence["%"]  = 3
precedence["("]  = 4
precedence[")"]  = 4
 
simplestack      = [] # ordered list
 
input            = [] # input list
verbose          = 0  # if 0 just output is printed
                      # if 1 just the summary is printed.
                      # if 2, token, output string, and stack are printed.
                      # if 3, verbose information is printed
 
 
 
 
 
def push(what):
    simplestack.append(what)
 
def pop():
    if len(simplestack):
        return simplestack.pop(-1) # remove the last 
    return None
 
def peek():
    if len(simplestack):
        return simplestack[-1]
    return None
 
def getprecedence(op):
    if op == None:
        return op
    return precedence[op]
 
def stacktostring(stack):
    if not stack:
        return "Empty"
    out = ""
    for i in reversed(stack):
        out = out + str(i) + " "
    return out[:-1]
 
def beVerbose(level, text):
    global verbose
    if verbose >= level:
        print text,
 
def concatsymbol(current, token):
    return current + token
 
def infixtopostfix(input):
    output = ""
    lastwasspace = False
    lasttoken = None
    for token in input:
 
 
        if not token.strip():
            lastwasspace = True
            continue
 
        beVerbose(2, "Token='%c'" % (token))
 
 
 
        if not token in operators:
 
            if lastwasspace and not lasttoken in operators:
                # Catch terms that were delimited by whitespace
                # but then the next token is a non-operator
                # Example string that would cause this "123 4+1"
                # since this doesn't make sense.
                print "ERROR: Unexpected token '%c'" % (token)
                sys.exit(1)
 
            output = output + token
 
            beVerbose(3, "added to output")
 
            lastwasspace = False
 
        else: # operators
 
            if lasttoken in arithmeticops and token in arithmeticops:
                # Catch duplication of operators. An example would
                # be "4 // 2" or "823 + - / 2" which makes no sense in infix.
                # The only operators allowed next to one another are
                # the formatting operators '(' and ')' used to group operations.
                print "ERROR: Unexpected token '%c'" % (token)
                sys.exit(1)
 
 
            if token == '(':
                push(token)
 
                beVerbose(3, "pushed onto stack")
 
            elif token == ')':
                tok = pop()
 
                beVerbose(3, "'%s' popped off stack" % (tok))
 
                while tok != "(":
                    if tok == None: #stack is empty
                        print
                        print "ERROR: Parenthesis mismatch"
                        sys.exit(1)
 
                    output = output + " " + tok
 
                    beVerbose(3, "and added to output")
 
                    tok = pop()
 
                    beVerbose(3, "'%s' popped off stack" % (tok))
 
            else: # mathematical operators
 
                tok = peek()
 
                while tok and tok != '(':
 
                    beVerbose(3, "'%s' is on the top of the stack" % (tok))
 
                    if ((
                            (token in associative or token in leftassociative) and
                            (getprecedence(token) <= getprecedence(tok))
                        ) or (
                            token in rightassociative and
                            getprecedence(token) < getprecedence(tok)
                        )):
 
                        tok = pop()
                        output = output + " " + tok
 
                        beVerbose(3, "'%s' popped off the stack and added to output" % (tok))
 
                    else:
                        break
 
                    tok = peek()
 
                push(token)
 
                beVerbose(3, "'%s' pushed onto stack" % (token))
                output = output + " "
 
        lastwasspace = False
        lasttoken = token
 
        if verbose == 2:
            format = "Output=% -40s Stack: % -30s"
        elif verbose >= 3:
            format = "Output=%s Stack: %s" # no field justification
        if verbose >= 2:
            print format % (output, stacktostring(simplestack))
 
    beVerbose(2, "Token=end")
 
    tok = peek()
 
    while tok:
        if tok == "(":
            print
            print "ERROR: Parenthesis mismatch"
            sys.exit(1)
 
        tok = pop()
 
        output = output + " " + tok
 
        beVerbose(3, "%s popped and added to output" % (tok))
 
        tok = peek()
 
    if verbose >= 3:
        print
    if verbose >= 2:
        print
    if verbose >= 1:
        print "Infix input =", input 
        print
        print "Postfix output =", output
 
    return output
 
 
 
if (len(sys.argv) < 2):
    print "Please provide infix input string or use --help for help"
    sys.exit(1)
 
# I should have really used getopts but I was young and naive when I wrote this!
for v in sys.argv[1:]:
    if v == "-v" or v == "--verbose":
        verbose = verbose + 1
    elif v == "-h" or v == "--help":
        print "usage: infixtopostfix [-v|-h] infix_input ..."
        print "-v, --verbose be verbose. use twice or thrice for more output"
        print "-h, --help show this help"
        sys.exit(0)
    else:
        input.append(v)
 
if not len(input):
    print "Please provide infix input string"
else:
    # Print all input strings
    for i in input:
        if verbose:
            print "Processing:", i
        print infixtopostfix(i.strip())
