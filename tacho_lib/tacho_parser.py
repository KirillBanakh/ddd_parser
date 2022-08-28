from email import header
from os import sep
from pipes import Template
from sqlite3 import Timestamp
from unicodedata import name
from tacho_lib import tacho_gen1
from dataclasses import fields, is_dataclass
from datetime import datetime
import copy

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
    timestamp = datetime.now().strftime("%H-%M-%S %d %B %Y")
    with open(timestamp + " " + "Raw Output.txt", 'w') as file:
        for idx, byte in enumerate(data):
            file.write("{0:0{1}X}".format(byte, 2))
            if (idx + 1) % 16 != 0:
                file.write(' ')
            if (idx + 1) % 16 == 0:
                file.write('\r')
        file.close()

def do_analysis(data: bytearray | bytes):
    data_idx: int = 0

    header = tacho_gen1.cHeader()
    header_list: list = []

    HEADER_OFFSET = 5 # fid + appendix + data_length bytes

    while data_idx < len(data):
        if tacho_gen1.eFID.seek(data[data_idx:data_idx+2]):
            header.fid = data[data_idx:data_idx+2]
            header.appendix = data[data_idx+2]
            header.data_length = data[data_idx+3:data_idx+5]

            header_list.append(header)
            header_list = copy.deepcopy(header_list)

            data_idx = data_idx + int.from_bytes(header.data_length, "big") + HEADER_OFFSET
    return header_list

def print_analysis(data: bytearray | bytes):
    separator = "+" + "-" * 38 + "+" + "-" * 39 + "+"

    idx: int = 0
    headers_list = do_analysis(data)

    print("#" * 80)
    print("# {:^76} #".format("ANALYSIS REPORT"))
    print("#" * 80)
    print(separator)

    while idx < len(headers_list):

        if headers_list[idx].fid != headers_list[idx-1].fid:
            print("| {:<36} | {:<37} |".format(tacho_gen1.eFID.get_name(headers_list[idx].fid), ""))
            print("|   {:<34} | {:<37} |".format("FID:", headers_list[idx].fid.hex()))
            print("|   {:<34} | {:<37} |".format("Appendix:", headers_list[idx].appendix))
            print("|   {:<34} | {:<37} |".format("Data Length:", int.from_bytes(headers_list[idx].data_length, "big")))

        else:
            print("| {:<36} | {:<37} |".format("Signature:", ""))
            print("|   {:<34} | {:<37} |".format("FID:", headers_list[idx].fid.hex()))
            print("|   {:<34} | {:<37} |".format("Appendix:", headers_list[idx].appendix))
            print("|   {:<34} | {:<37} |".format("Signature Length:", int.from_bytes(headers_list[idx].data_length, "big")))

        if idx < (len(headers_list) - 1) and headers_list[idx].fid != headers_list[idx+1].fid:
            print(separator)

        idx += 1

    print("#" * 80)
    print("# {:^76} #".format("ANALYSIS SUMMARY"))
    print("#" * 80)


def print_parsed_data_to_console(data: bytearray | bytes):
    print("TODO")
    # print_analysis(data)




