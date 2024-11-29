import csv
import sys

# Инициализация памяти и регистров УВМ
memory = [0] * 256  # 256 байт памяти
registers = [0] * 4  # 4 регистра A, B, C, D

def interpret(input_file, output_file, memory_range):
    with open(input_file, 'rb') as bin_file:
        binary_data = bin_file.read()

    i = 0
    while i < len(binary_data):
        opcode = binary_data[i]
        reg1 = binary_data[i + 1]
        reg2_or_val = binary_data[i + 2]
        
        if opcode == 0xEC:  # LOAD
            registers[reg1] = reg2_or_val
            i += 3
        elif opcode == 0xCE:  # READ
            registers[reg1] = memory[reg2_or_val]
            i += 3
        elif opcode == 0xC2:  # WRITE
            memory[reg2_or_val] = registers[reg1]
            i += 3
        elif opcode == 0x1D:  # ADD
            registers[reg1] += registers[reg2_or_val]
            i += 3

    # Сохранение результатов в файл
    with open(output_file, 'w', newline='') as result_file:
        writer = csv.writer(result_file)
        for address in memory_range:
            writer.writerow([address, memory[address]])

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    memory_range = range(int(sys.argv[3]), int(sys.argv[4]) + 1)
    interpret(input_file, output_file, memory_range)
