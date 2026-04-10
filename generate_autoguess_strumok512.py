import os
# example: https://github.com/hadipourh/autoguess/blob/main/ciphers/SNOW2/snow2_v0.py

output_dir = os.path.curdir

def strumok512(T=11):
    cipher_name = 'strumok512'
    eqs = f'#{cipher_name} {T} Rounds\n'
    eqs += 'connection relations\n'

    for t in range(T):
        # r2_{t+1} = T(r1_t)
        eqs += f'R2_{t + 1}, R1_{t}\n'

        # r1_{t+1} = r2_t + s13_t
        eqs += f'R1_{t + 1}, R2_{t}, S_{t}_13\n'

        # a_mul(s0_t)
        eqs += f'A0_{t}, S_{t}_0\n'

        # ainv_mul(s11_t)
        eqs += f'B11_{t}, S_{t}_11\n'

        # new s15
        eqs += f'S_{t + 1}_15, A0_{t}, B11_{t}, S_{t}_13\n'

        # shift
        for i in range(15):
            eqs += f'S_{t + 1}_{i}, S_{t}_{i + 1}\n'

    eqs += 'end'

    eqsfile_path = os.path.join(output_dir, 'relationfile_strumok512_11clk.txt')
    with open(eqsfile_path, 'w') as relation_file:
        relation_file.write(eqs)

def main():
    strumok512(T=11)

if __name__ == '__main__':
    main()