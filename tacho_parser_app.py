from tacho_lib import tacho_parser
import argparse

input_parser = argparse.ArgumentParser(description="Script for parsing *.DDD files")
input_parser.add_argument("-f", "--file", help="path to *.DDD file")
input_parser.add_argument("-pa", "--print_analysis", help="print data analysis to console", action="store_true")
input_parser.add_argument("-sa", "--save_analysis", help="save data analysis to file", action="store_true")
input_parser.add_argument("-pr", "--print_raw", help="print raw data to console", action="store_true")
input_parser.add_argument("-sr", "--save_raw", help="save raw data to <date>_<time>_output.txt file", action="store_true")
input_parser.add_argument("-pp", "--print_parsed", help="print parsed data to console", action="store_true")
input_parser.add_argument("-sp", "--save_parsed", help="save parsed data to <date>_<time>_output.txt file", action="store_true")
arguments = input_parser.parse_args()

with open(arguments.file, 'rb') as file:
    raw_data = file.read()

    if arguments.print_analysis:
        tacho_parser.print_analysis(raw_data)

    if arguments.save_analysis:
        tacho_parser.save_analysis(raw_data)
    if arguments.print_raw:
        tacho_parser.print_raw_data_to_console(raw_data)

    if arguments.save_raw:
        tacho_parser.save_raw_data_to_file(raw_data)

    if arguments.print_parsed:
        tacho_parser.print_parsed_data_to_console(raw_data)

    if arguments.save_parsed:
        print("TODO")

    file.close
