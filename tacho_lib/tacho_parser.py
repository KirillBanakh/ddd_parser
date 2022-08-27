from tacho_lib import tacho_gen1
from dataclasses import fields, is_dataclass
from datetime import datetime

def iterate_test(dataclass, depth_symbol: str = " ", depth: int = 1):
    if depth < 0:
        raise Exception("depth should be >= 0")

    if type(dataclass) == tacho_gen1.cMF:
        print(type(dataclass).__name__)

    for field in fields(dataclass):
        if is_dataclass(field.type):
            if(field.type == tacho_gen1.cHeader):
                print(depth_symbol * depth + field.name)
            else:
                print(depth_symbol * depth + field.name)
            iterate_test(field.type, depth_symbol, depth + 1)
        else:
            print(depth_symbol * depth + field.name)

def print_raw_data_to_console(data: bytearray | bytes):
    for idx, byte in enumerate(data):
        print("{0:0{1}X}".format(byte, 2), end = ' ')
        if (idx + 1) % 16 == 0:
            print()
    print()

def save_raw_data_to_file(data: bytearray | bytes):
    time = datetime.now()
    time = time.strftime("%H-%M-%S")
    date = datetime.today()
    date = date.strftime("%d %B %Y")
    with open(date + " " + time + " " + "Raw Output.txt", 'w') as file:
        for idx, byte in enumerate(data):
            file.write("{0:0{1}X}".format(byte, 2))
            if (idx + 1) % 16 != 0:
                file.write(' ')
            if (idx + 1) % 16 == 0:
                file.write('\r')
        file.close()

def do_analysis(data: bytearray | bytes):
    idx: int = 0
    fid_list = list(tacho_gen1)


def print_analysis(data: bytearray | bytes):
    separator = "+" + "-" * 38 + "+" + "-" * 39 + "+"
    idx: int = 0
    fid_list = list(tacho_gen1.eFID)
    fid_pointer: int = 0
    fid = bytes([0x00] * 2)
    fid_previous = bytes([0x00] * 2)

    print("#" * 80)
    print("# {:^76} #".format("ANALYSIS REPORT"))
    print("#" * 80)
    print(separator)

    while idx < len(data):
        while fid_pointer < len(tacho_gen1.eFID):
            if data[idx:idx+2] == fid_list[fid_pointer].value:

                fid = data[idx:idx+2]
                signature = data[idx+2]
                length = int.from_bytes(data[idx+3:idx+5], "big")
                idx = idx + 5 + length
                if fid_previous != fid:
                    print("| {:<36} | {:<37} |".format(fid_list[fid_pointer].name, " "))
                    print("|   {:<34} | {:<37} |".format("FID", fid.hex()))
                    print("|   {:<34} | {:<37} |".format("Appendix", signature))
                    print("|   {:<34} | {:<37} |".format("Data Length", length))
                    fid_previous = fid
                else:
                    print("| {:<36} | {:<37} |".format("Signature", " "))
                    print("|   {:<34} | {:<37} |".format("FID", fid.hex()))
                    print("|   {:<34} | {:<37} |".format("Appendix", signature))
                    print("|   {:<34} | {:<37} |".format("Signature Length", length))

                if data[idx:idx+2] != fid_list[fid_pointer].value:
                    print(separator)

            if idx < len(data):
                if data[idx:idx+2] != fid_list[fid_pointer].value:
                    fid_pointer += 1
                if fid_pointer == len(tacho_gen1.eFID):
                    fid_pointer = 0
            break
    print("#" * 80)
    print("# {:<} {:<56} #".format("Total Bytes Parsed:", idx))
    print("#" * 80)

def print_parsed_data_to_console(data: bytearray | bytes):
    print("TODO")
    # print_analysis(data)




