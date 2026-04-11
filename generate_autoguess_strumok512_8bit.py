import os
import sys
# example: https://github.com/hadipourh/autoguess/blob/main/ciphers/SNOW2/snow2_v0.py

output_dir = os.path.join(os.path.curdir, 'results')

def part(name, t, i):
    return f"{name}_{t}_{i}"

def parts(name, t):
    return [part(name, t, i) for i in range(8)]

def strumok512(T=11):
    cipher_name = 'strumok512'
    eqs = f'#{cipher_name} {T} Rounds\n'
    eqs += 'connection relations\n'

    for t in range(T):
        # 7.3 | 4. Оновлюють значення 16-ї комірки РЗЛЗЗ. Якщо встановлено звичайний режим функції Next, значення цієї комірки обчислюють за правилом:
        for i in range(8):
            eqs += f"{part('S', t+16, i)}, {part('S', t+13, i)}, {part('S', t+11, i)}, {part('S', t, i)}\n"

        # 7.3 Функція наступного стану Next (1)
        for i in range(8):
            eqs += f"{part('R2', t+1, i)}, {', '.join(parts('R1', t))}\n"

        # 7.3 Функція наступного стану Next (2)
        for i in range(8):
            variables = [part('R1', t+1, i)]
            for j in range(i + 1):
                variables.append(part('R2', t, j))
                variables.append(part('S', t+13, j))
            eqs += f"{', '.join(variables)}\n"

        # 7.4 Функція ключового потоку Strm
        for i in range(8):
            variables = [part('S', t, i), part('R2', t, i)]
            for j in range(i + 1):
                variables.append(part('S', t+15, j))
                variables.append(part('R1', t, j))
            eqs += f"{', '.join(variables)}\n" # Z_{t},

    # eqs += "known\n"
    # for t in range(T):
    #     eqs += f"Z_{t}\n"

    eqs += 'end'

    eqsfile_path = os.path.join(output_dir, f'relationfile_strumok512_{T}clk_8bit.txt')
    os.makedirs(output_dir, exist_ok=True)
    with open(eqsfile_path, 'w') as relation_file:
        relation_file.write(eqs)

def main():
    T = 11
    if len(sys.argv) > 1:
        T = int(sys.argv[1])

    strumok512(T=T)

if __name__ == '__main__':
    main()
