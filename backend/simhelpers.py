# decimal to binary with sign ext converter
def dec2bin_sext(n,bits):
    n_1 = str(bin(n))
    if n >= 0:
        n_2 = '0' + n_1[2:]
        if len(n_2) > bits:
            x = len(n_2) - bits
            n_2 = n_2[x:]
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
            x = len(n_2) - bits
            n_2 = n_2[x:]
        else:
            n_2 = '1'*(bits-len(n_2)) + n_2
    return n_2

def bin2dec(n):
    #print(n)
    if n[0] == '0':
        a = int(n, 2) 
    else:
        a = ''.join('1' if bit == '0' else '0' for bit in n)
        a = int(a, 2) + 1
        a = (-1)* a
    return a

def unsign_bin2dec(n):
    y = int(n,2)
    return y

def twos_comp(binary_str):
    flipped_binary_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)
    
    twos_comp_result = bin2dec(flipped_binary_str) + 1
    twos_comp_result = dec2bin_sext(twos_comp_result,32)

    return twos_comp_result

def add_signed_binary(bin1, bin2):
    
    # Perform signed binary addition
    a = bin2dec(bin1)
    b = bin2dec(bin2)
    c = a+b
    result = dec2bin_sext(c,32)

    return result
