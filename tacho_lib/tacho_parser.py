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
        else:
            print("File corrupted!")
            break
    return header_list

def print_analysis(data: bytearray | bytes):
    separator = "+" + "-" * 38 + "+" + "-" * 39 + "+"

    idx: int = 0
    headers_list = do_analysis(data)
    fid_list = [header.fid for header in headers_list]

    print("#" * 80)
    print("# {:^76} #".format("ANALYSIS REPORT"))
    print("#" * 80)
    print(separator)

    while idx < len(headers_list):

        if headers_list[idx].fid != headers_list[idx-1].fid:
            print("| {:<36} | {:<37} |".format(tacho_gen1.eFID.get_name(headers_list[idx].fid), ""))
        else:
            print("| {:<36} | {:<37} |".format("Signature:", ""))

        print("|   {:<34} | {:<37} |".format("FID:", headers_list[idx].fid.hex()))
        print("|   {:<34} | {:<37} |".format("Appendix:", headers_list[idx].appendix))
        print("|   {:<34} | {:<37} |".format("Signature Length:", int.from_bytes(headers_list[idx].data_length, "big")))

        if idx < (len(headers_list) - 1) and headers_list[idx].fid != headers_list[idx+1].fid:
            print(separator)

        idx += 1

    print(separator)
    print("#" * 80)
    print("# {:^76} #".format("ANALYSIS SUMMARY"))
    print("#" * 80)

    print(" - {:<}: {:<}".format("Total bytes parsed", len(data)))
    print(" - {:<}: {:<}".format("Total headers found", len(headers_list)))
    print(" - {:<}:".format("EFs not present"))

    for fid in tacho_gen1.eFID:
        if fid.value["fid"] not in fid_list and not tacho_gen1.eFID.get_name(fid.value["fid"]).find("EF"):
            print(" -- {:<}".format(tacho_gen1.eFID.get_name(fid.value["fid"])))

    print("#" * 80)
    print("# {:^76} #".format("END OF ANALYSIS"))
    print("#" * 80)

def save_analysis(data: bytearray | bytes):
    separator = "+" + "-" * 38 + "+" + "-" * 39 + "+\r"

    idx: int = 0
    headers_list = do_analysis(data)
    fid_list = [header.fid for header in headers_list]
    timestamp = datetime.now().strftime("%H-%M-%S %d %B %Y")

    with open(timestamp + " " + "Analysis Output.txt", 'w') as file:
        file.write("#" * 80 + "\r")
        file.write("# {:^76} #\r".format("ANALYSIS REPORT"))
        file.write("#" * 80 + "\r")
        file.write(separator)

        while idx < len(headers_list):

            if headers_list[idx].fid != headers_list[idx-1].fid:
                file.write("| {:<36} | {:<37} |\r".format(tacho_gen1.eFID.get_name(headers_list[idx].fid), ""))
            else:
                file.write("| {:<36} | {:<37} |\r".format("Signature:", ""))

            file.write("|   {:<34} | {:<37} |\r".format("FID:", headers_list[idx].fid.hex()))
            file.write("|   {:<34} | {:<37} |\r".format("Appendix:", headers_list[idx].appendix))
            file.write("|   {:<34} | {:<37} |\r".format("Signature Length:", int.from_bytes(headers_list[idx].data_length, "big")))

            if idx < (len(headers_list) - 1) and headers_list[idx].fid != headers_list[idx+1].fid:
                file.write(separator)

            idx += 1

        file.write(separator)
        file.write("#" * 80 + "\r")
        file.write("# {:^76} #\r".format("ANALYSIS SUMMARY"))
        file.write("#" * 80 + "\r")

        file.write(" - {:<}: {:<}\r".format("Total bytes parsed", len(data)))
        file.write(" - {:<}: {:<}\r".format("Total headers found", len(headers_list)))
        file.write(" - {:<}:\r".format("EFs not present"))

        for fid in tacho_gen1.eFID:
            if fid.value["fid"] not in fid_list and not tacho_gen1.eFID.get_name(fid.value["fid"]).find("EF"):
                file.write(" -- {:<}\r".format(tacho_gen1.eFID.get_name(fid.value["fid"])))

        file.write("#" * 80 + "\r")
        file.write("# {:^76} #\r".format("END OF ANALYSIS"))
        file.write("#" * 80 + "\r")

        file.close()

def print_parsed_data_to_console(data: bytearray | bytes):
    print("TODO")
    # print_analysis(data)




