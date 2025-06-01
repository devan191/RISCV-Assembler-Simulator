import sys
from constants import *

class AssemblyError(Exception):
    pass
class SimulationError(Exception):
    pass

def print_and_exit(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def valid_imm(n,line_no):
    numlist = ['0','1','2','3','4','5','6','7','8','9','-','.']
    for i in n:
        if i not in numlist:
            print_and_exit(f"Syntax Error: immediate value is not a number on line {line_no}")

def check_label_redef_error(label,line_no,labels_dict):
    if label in labels_dict:
        print_and_exit(f"Syntax error on line {line_no} Redefining label!")

def check_label_syntax_error(token_1,line_no,opname):
    if len(token_1) > 3:
        print_and_exit(f"Syntax error on line {line_no}\nInvalid label!")
    if (len(token_1) == 3) and (':' not in opname):
        print_and_exit(f"Syntax error on line {line_no}\nInvalid label!")
    if (len(token_1) == 2) and (':' in opname):
        print_and_exit(f"Syntax error on line {line_no}\nInvalid label!")
    if len(token_1) == 1:
        print_and_exit(f"Syntax error on line {line_no}\nInvalid label!")

def check_reg_error(reg,line_no):
    if reg not in registers_dict:
        print_and_exit(f"Error: unknown register name used on line {line_no}")

def check_valid_token_len(token,token_len,line_no):
    if len(token) != token_len:
        print_and_exit(f"Syntax Error on line {line_no}")

def check_I_type_token(token,line_no):
    if (len(token) > 3) or (len(token) < 2):
        print_and_exit(f"Syntax error on line {line_no}")
    if (len(token) == 3) and ('' in token):
        print_and_exit(f'Syntax error on line {line_no}')
    if (len(token) == 2) and ('' in token):
        print_and_exit(f'Syntax Error on line {line_no}')

def check_pmem_exceeded(PrgCMax):
    if PrgCMax > 255:
        print_and_exit('Error: Program memory exceeded: no of instructions > 64')