import os
import sys
# example: https://github.com/hadipourh/autoguess/blob/main/ciphers/SNOW2/snow2_v0.py

output_dir = os.path.join(os.path.curdir, 'results')

def part(name, t, i):
    return f"{name}_{t}_{i}"

def strumok512(T=11):
    cipher_name = 'strumok512'
    eqs = f'#{cipher_name} {T} Rounds\n'
    eqs += 'connection relations\n'

    for t in range(T):
        # 7.3 | 4. Оновлюють значення 16-ї комірки РЗЛЗЗ. Якщо встановлено звичайний режим функції Next, значення цієї комірки обчислюють за правилом:
        eqs += f"{part('S', t+16, 0)}, {part('S', t+13, 0)}, {part('S', t+11, 0)}, {part('S', t, 0)}\n"
        eqs += f"{part('S', t+16, 1)}, {part('S', t+13, 1)}, {part('S', t+11, 1)}, {part('S', t, 1)}\n"

        # 7.3 Функція наступного стану Next (1) 
        eqs += f"{part('R2', t+1, 0)}, {part('R1', t, 0)}, {part('R1', t, 1)}\n"
        eqs += f"{part('R2', t+1, 1)}, {part('R1', t, 0)}, {part('R1', t, 1)}\n"

        # 7.3 Функція наступного стану Next (2) 
        eqs += f"{part('R1', t+1, 0)}, {part('R2', t, 0)}, {part('S', t+13, 0)}\n"
        eqs += f"{part('R1', t+1, 1)}, {part('R2', t, 0)}, {part('S', t+13, 0)}, {part('R2', t, 1)}, {part('S', t+13, 1)}\n" # R1_1_1, R2_0_0, S_13_0, R2_0_1, S_13_1  if R2_0_0 + S_13_0 >= 2^32 

        # 7.4 Функція ключового потоку Strm
        eqs += f"{part('S', t, 0)}, {part('R2', t, 0)}, {part('S', t+15, 0)}, {part('R1', t, 0)}\n" # Z_{t},
        eqs += f"{part('S', t, 1)}, {part('R2', t, 1)}, {part('S', t+15, 0)}, {part('R1', t, 0)}, {part('S', t+15, 1)}, {part('R1', t, 1)}\n" # Z_{t},
 
    # eqs += "known\n"А 
    # for t in range(T):
    #     eqs += f"Z_{t}\n"

    eqs += 'end'

    eqsfile_path = os.path.join(output_dir, f'relationfile_strumok512_{T}clk_32bit.txt')
    os.makedirs(output_dir, exist_ok=True)
    with open(eqsfile_path, 'w') as relation_file:
        relation_file.write(eqs)

def main():
    T = 11Jr
    if len(sys.argv) > 1:
        T = int(sys.argv[1])

    strumok512(T=T)

if __name__ == '__main__':
    main()
