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
        choices=range(1, 26),
        metavar='[1-25]',
        help='Numbered day of the solution (ex: 1, 02, or 25)',
        dest='day',
        required=True
    )
    parser.add_argument(
        '-p', '--part',
        type=int,
        choices=[0, 1, 2],
        metavar='[0-2]',
        help='Question number (or part) used for test/example input/answer file prefixes. If not set (0), script will loop through all parts.',
        dest='part',
        default=0
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


def readcsv(filename, csv_delimeter):
    parsed = []
    try:
        with open(filename, newline='') as csvfile:
            for row in csv.reader(csvfile, delimiter=csv_delimeter, quotechar='"'):
                parsed.append(row)
    except FileNotFoundError:
        print(f"File {filename} could not be opened. Are you sure it exists?")
        exit()
    return parsed


def solve(day, part, input, answer, args):
    solution = importlib.import_module(f'day_{day}')
    this_answer = solution.solve(day, part, input, args)
    if args.test:
        test(this_answer, answer[0][0], args.verbose)


def test(answer, expected, verbose):
    match answer:
        case str():
            expected = str(expected)
        case int():
            expected = int(expected)
    if answer == expected:
        if verbose:
            print("\t✅ Test passed!")
        return True
    else:
        if verbose:
            print(f"\t❌ Test FAILED! Expected answer: {expected}")
        return False


def main(args):
    day = str(args.day).zfill(2)
    part = str(args.part)
    folder = f'day_{day}'
    prefix = f'example{part}-' if args.test else ''
    answer_filename = f'{folder}/{prefix}answer.txt'
    input_filename = f'{folder}/{prefix}input.txt'

    # Each puzzle CSV may use different delimeters
    # Default to comma (,)
    delimeters = {
        2: ';'
    }
    csv_delimeter = delimeters[int(day)] if int(day) in delimeters else ','

    if args.test:
        print('****** RUNNING IN TEST MODE (USING EXAMPLE FILES) ******')
        if args.verbose:
            print(f'Reading Answers CSV: {answer_filename}')
        answer = readcsv(answer_filename, csv_delimeter)
    else:
        answer = []
    if args.verbose:
        print(f'Reading Input CSV: {input_filename}')
    input = readcsv(input_filename, csv_delimeter)
    solve(day, int(part), input, answer, args)


if __name__ == "__main__":
    args = initargs()
    if args.part == 0:
        for x in [1, 2]:
            args.part = x
            main(args)
    else:
        main(args)
