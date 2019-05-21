import sys
import getopt

from src.memreport import MemReport

help_string = 'Usage: {} -i <inputfile>'.format(__file__)


def parse_input(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:")
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_string)
            sys.exit()
        elif opt == '-i':
            return arg


if __name__ == '__main__':
    input_file_path = parse_input(sys.argv[1:])

    try:
        memreport = MemReport(input_file_path)
    except FileNotFoundError:
        print('Provided input file not found.')