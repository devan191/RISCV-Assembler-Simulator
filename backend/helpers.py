from errors import *

# decimal to binary with sign extension converter
def bin_ext_converter(n,bits,line_no):
    n_1 = str(bin(n))
    if n >= 0:
        n_2 = '0' + n_1[2:]
        if len(n_2) > bits:
            print('Syntax error on line',line_no,"\n","Immdiate out of bounds!")
            sys.exit()
        else:
            n_2 = '0'*(bits-len(n_2)) + n_2
    else:
        if abs(n) == 2 ** (bits-1):
            n_2 = str(bin(n))
            n_2 = n_2[3:]
            return n_2
        
        n_2 = '0'+ n_1[3:]
        n_2 = ''.join('1' if b == '0' else '0' for b in n_2)
        n_2 = str(bin(int(n_2,2)+1))
        n_2 = n_2[2:]
        if len(n_2)> bits:
            print('Syntax error on line',line_no,"\n","Immdiate out of bounds!")
            sys.exit()
        else:
            n_2 = '1'*(bits-len(n_2)) + n_2
    return n_2
