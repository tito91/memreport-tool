import sys
import getopt

from src.chart import Chart
from src.filesize.filesize import FileSize
from src.memreport import MemReport
from src.threshold import Threshold

help_string = 'Usage: {} -i <inputfile> -c <chart type> -t <size threshold in KB>'.format(__file__)
obligatory_parameters = ['-i', '-c']


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
            if arg not in MemReport.asset_types:
                print('Chart type should be one of: {}'.format(MemReport.asset_types))
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
        size_threshold = FileSize.from_int(threshold.value, 'kb') if threshold else None

        try:
            mem_report = MemReport(input_file_path, chart_type, size_threshold)
        except Exception as e:
            print('Could not parse the report file.')
            sys.exit()

        chart = Chart(mem_report)
        chart.show()
    except FileNotFoundError:
        print('Provided input file not found.')
