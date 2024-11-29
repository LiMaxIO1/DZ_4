import csv
import sys

# Таблица команд УВМ
commands = {
    "LOAD": 0xEC,
    "READ": 0xCE,
    "WRITE": 0xC2,
    "ADD": 0x1D
}

# Маппинг регистров
registers = {
    "A": 0x00,
    "B": 0x01,
    "C": 0x02,
    "D": 0x03
}

def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        program_lines = f.readlines()

    binary_instructions = []
    log_entries = []

    for line in program_lines:
        parts = line.strip().split()
        command = parts[0]
        if command == "LOAD":
            reg = parts[1]
            value = int(parts[2])
            binary_instructions.append([commands["LOAD"], registers[reg], value & 0xFF])
            log_entries.append(f"{command}={reg} {value}")
        elif command == "READ":
            reg = parts[1]
            address = int(parts[2])
            binary_instructions.append([commands["READ"], registers[reg], address & 0xFF])
            log_entries.append(f"{command}={reg} {address}")
        elif command == "WRITE":
            address = int(parts[1])
            reg = parts[2]
            binary_instructions.append([commands["WRITE"], address & 0xFF, registers[reg]])
            log_entries.append(f"{command}={address} {reg}")
        elif command == "ADD":
            reg1 = parts[1]
            reg2 = parts[2]
            binary_instructions.append([commands["ADD"], registers[reg1], registers[reg2]])
            log_entries.append(f"{command}={reg1} {reg2}")

    # Запись бинарного файла
    with open(output_file, 'wb') as bin_file:
        for instruction in binary_instructions:
            bin_file.write(bytes(instruction))

    # Запись лог-файла
    with open(log_file, 'w') as log:
        log_writer = csv.writer(log)
        for entry in log_entries:
            log_writer.writerow([entry])

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)
