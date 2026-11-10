"""Hack assembler: .asm -> .hack
Usage: python assembler.py Prog.asm
Extra feature (K = 2): warn if the same label is defined twice.
"""
import sys

COMP = {
    '0': '0101010', '1': '0111111', '-1': '0111010',
    'D': '0001100', 'A': '0110000', '!D': '0001101', '!A': '0110001',
    '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
    'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
    'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
}

for k, v in list(COMP.items()):
    if 'A' in k:
        COMP[k.replace('A', 'M')] = '1' + v[1:]

for a, b in [('A+D', 'D+A'), ('M+D', 'D+M'), ('A&D', 'D&A'),
             ('M&D', 'D&M'), ('A|D', 'D|A'), ('M|D', 'D|M')]:
    COMP[a] = COMP[b]

JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

SYMBOLS = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
           'SCREEN': 16384, 'KBD': 24576}
for i in range(16):
    SYMBOLS['R' + str(i)] = i


def dest_bits(d):
    """Bits are A, D, M in that order."""
    return ('1' if 'A' in d else '0') + \
           ('1' if 'D' in d else '0') + \
           ('1' if 'M' in d else '0')


def clean(line):
    """Remove comments and all whitespace."""
    line = line.split('//')[0]
    return ''.join(line.split())


def assemble(lines):
    symbols = dict(SYMBOLS)
    labels_seen = {}
    program = []

    
    for lineno, raw in enumerate(lines, start=1):
        line = clean(raw)
        if not line:
            continue
        if line.startswith('(') and line.endswith(')'):
            name = line[1:-1]
            if name in labels_seen:
                print(f"Warning: line {lineno}: label '{name}' already "
                      f"defined on line {labels_seen[name]}")
                continue      
            labels_seen[name] = lineno
            symbols[name] = len(program)
        else:
            program.append(line)


    output = []
    next_var = 16
    for line in program:
        if line.startswith('@'):
            value = line[1:]
            if value.isdigit():
                n = int(value)
            else:
                if value not in symbols:
                    symbols[value] = next_var
                    next_var += 1
                n = symbols[value]
            output.append(format(n, '016b'))
        else:
            dest, jump = '', ''
            comp = line
            if '=' in comp:
                dest, comp = comp.split('=', 1)
            if ';' in comp:
                comp, jump = comp.split(';', 1)
            output.append('111' + COMP[comp] + dest_bits(dest) + JUMP[jump])
    return output


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.asm'):
        print("Usage: python assembler.py Prog.asm")
        sys.exit(1)
    path = sys.argv[1]
    with open(path) as f:
        lines = f.read().splitlines()
    result = assemble(lines)
    out_path = path[:-4] + '.hack'
    with open(out_path, 'w', newline='\n') as f:
        f.write('\n'.join(result) + '\n')
    print(f"Wrote {len(result)} instructions to {out_path}")


if __name__ == '__main__':
    main()
