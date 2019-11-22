import argparse
import sys
import time

def parse_args():
    if len(sys.argv) < 2:
        print("Usage: python scan.py -h")
        sys.exit()
    parser = argparse.ArgumentParser(description='Domain scanner')
    parser.add_argument("target")
    parser.add_argument('-f', "--file", default='./dicts/subnames.txt', help='domain dict')
    parser.add_argument('-o', '--output', default='./output/default_output.txt',help='Output file name.')
    parser.add_argument('-t', "--threads", default=100, type=int)
    parser.add_argument('--ip', action='store_true', help='save ip in output file')
    parser.add_argument('--full', action='store_true', help='use big dict')

    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":
    args = parse_args()
    print(args.file)
    print(args.full)
    print(args.output)
    print(args.target)
    print(args.threads)
    output_filename = args.target + "_" + str(time.time()).split('.')[0] + '.txt'
    print(output_filename)