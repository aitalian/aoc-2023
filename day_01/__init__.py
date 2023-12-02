import re


def solve(day, part, input, args):
    print(f"Day {day} Solution.")
    # Get the calibration value for each row
    # Add them up together (sum) to get answer
    values = []
    for row in input:
        values.append(calibration_value(row[0], part))
    # Remove None values, convert to int
    values = list(map(int, filter(lambda a: a is not None, values)))
    this_answer = sum(values)
    print(f"\tPart {part}: Sum of Calibration values = {this_answer}")
    if args.verbose:
        print(f"\tAll calibration values: {values}")
    return this_answer


def calibration_value(row, part):
    # Get first and last digit
    # Combine them to get the calibration value
    if part == 1:
        # Match any digit
        r = r'\d'
    if part == 2:
        # Create a dictionary matching phonetic number strings to integers
        # NOTE: Omitted zero (0) as it was not mentioned in the puzzle
        phonetic_numbers = {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9
        }

        # Build a regex that will search for digits and phonetic strings
        p = '|'.join(k for k, v in phonetic_numbers.items())
        # Find all matches even overlapping ones
        r = f'(?=(\d|{p}))'

    matches = re.findall(r, row)

    # In the end we only care about the first and last match
    first = matches[0]
    last = matches[-1]

    if part == 2:
        # Replace phonetic number strings with their matching integer
        for k, v in phonetic_numbers.items():
            first = first.replace(k, str(v))
            last = last.replace(k, str(v))

    if len(matches) >= 1:
        # first & last; if there is only one match, they will be the same value
        return ''.join([first, last])

    return
