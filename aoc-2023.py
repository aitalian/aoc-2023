import csv
import argparse
import importlib

def initargs():
    parser = argparse.ArgumentParser(
                prog='aoc-2023',
                description='Advent of Code 2023'
            )
    parser.add_argument(
        '-d', '--day',
        type=int,
        choices=range(1, 25),
        metavar='day',
        help='Numbered day of the solution (ex: 1, 02, or 25)',
        dest='day',
        required=True
    )
    parser.add_argument(
        '-p', '--part',
        type=int,
        choices=[1, 2],
        metavar='part',
        help='Question number (or part) used for test/example input/answer file prefixes',
        dest='part',
        required=True
    )
    parser.add_argument(
        '--test',
        action='store_true',
        dest='test',
        help='Check that given example answers match the calculated answers'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='verbose'
    )
    return parser.parse_args()


def readcsv(filename):
    parsed = []
    with open(filename, newline='') as csvfile:
        for row in csv.reader(csvfile, delimiter=',', quotechar='"'):
            parsed.append(row)
    return parsed

def solve(day, part, input, answer, args):
    solution = importlib.import_module(f'day_{day}')
    solution.solve(day, part, input, answer, args)

def main(args):
    day = str(args.day).zfill(2)
    part = str(args.part)
    folder = f'day_{day}'
    prefix = f'example{part}-' if args.test else ''
    answer_filename = f'{folder}/{prefix}answer.txt'
    input_filename = f'{folder}/{prefix}input.txt'
    if args.test:
        print('****** RUNNING IN TEST MODE (USING EXAMPLE FILES) ******')
        if args.verbose:
            print('Reading Answers CSV: ' + answer_filename)
        answer = readcsv(answer_filename)
    else:
        answer = []
    if args.verbose:
        print('Reading Input CSV: ' + input_filename)
    input = readcsv(input_filename)
    solve(day, int(part), input, answer, args)

if __name__ == "__main__":
    args = initargs()
    main(args)
