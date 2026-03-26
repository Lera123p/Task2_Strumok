from utils import correct_mask64


#Rewrited example into Python from use-example.c
def a_mul(x, tables):
    return ((x << 8) & correct_mask64) ^ tables['alpha_mul'][x >> 56]

def ainv_mul(x, tables):
    return (x >> 8) ^ tables['alphainv_mul'][x & 0xff]

def transform_T(x, tables):
    return (tables['T0'][x & 0xff] ^
            tables['T1'][(x >> 8) & 0xff] ^
            tables['T2'][(x >> 16) & 0xff] ^
            tables['T3'][(x >> 24) & 0xff] ^
            tables['T4'][(x >> 32) & 0xff] ^
            tables['T5'][(x >> 40) & 0xff] ^
            tables['T6'][(x >> 48) & 0xff] ^
            tables['T7'][(x >> 56) & 0xff])

def fsm_func(x, y, z):
    return ((x + y) & correct_mask64) ^ z