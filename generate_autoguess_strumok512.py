import os
# example: https://github.com/hadipourh/autoguess/blob/main/ciphers/SNOW2/snow2_v0.py

output_dir = os.path.curdir

def strumok512(T=11):
    cipher_name = 'strumok512'
    eqs = f'#{cipher_name} {T} Rounds\n'
    eqs += 'connection relations\n'

    for t in range(T):
        # 7.3 | 4. Оновлюють значення 16-ї комірки РЗЛЗЗ. Якщо встановлено звичайний режим функції Next, значення цієї комірки обчислюють за правилом:
        eqs += f"S_{t+16}, S_{t+13}, S_{t+11}, S_{t}\n"

        # 7.3 Функція наступного стану Next (1) 
        eqs += f"R2_{t+1}, R1_{t}\n"

        # 7.3 Функція наступного стану Next (2) 
        eqs += f"R1_{t+1}, R2_{t}, S_{t+13}\n"

        # 7.4 Функція ключового потоку Strm
        eqs += f"S_{t+15}, R1_{t}, R2_{t}, S_{t}\n" # Z_{t}, 
 
    # eqs += "known\n"
    # for t in range(T):
    #     eqs += f"Z_{t}\n"

    eqs += 'end'

    eqsfile_path = os.path.join(output_dir, 'relationfile_strumok512_11clk.txt')
    with open(eqsfile_path, 'w') as relation_file:
        relation_file.write(eqs)

def main():
    strumok512(T=11)

if __name__ == '__main__':
    main()
