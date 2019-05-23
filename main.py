import sys
import getopt

from src.chart import Chart
from src.memreport import MemReport
from src.threshold import Threshold

help_string = 'Usage: {} -i <inputfile> -c <chart type>'.format(__file__)
obligatory_parameters = ['-i', '-c']
chart_types = ['textures', 'sounds']


def parse_input(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:c:t:")
    except getopt.GetoptError:
        print(help_string)
        sys.exit()

    if not opts:
        print(help_string)
        sys.exit()

    param_requested = list(zip(*opts))[0]

    if '-h' in param_requested:
        print(help_string)
        sys.exit()

    for param in obligatory_parameters:
        if param not in param_requested:
            print('Please provide obligatory parameter <{}>.'.format(param))
            print(help_string)
            sys.exit()

    chart = ''
    input_file = ''
    threshold = None

    for opt, arg in opts:
        if opt == '-c':
            if arg not in chart_types:
                print('Chart type should be one of: {}'.format(chart_types))
                sys.exit()
            else:
                chart = arg
        if opt == '-i':
            input_file = arg
        if opt == '-t':
            threshold = Threshold(arg)

    if not threshold:
        threshold = Threshold(0)

    return input_file, chart, threshold


if __name__ == '__main__':
    input_file_path, chart_type, threshold = parse_input(sys.argv[1:])

    try:
        mem_report = MemReport(input_file_path, threshold.value)
        chart = Chart(mem_report)
        chart.show()
    except FileNotFoundError:
        print('Provided input file not found.')
