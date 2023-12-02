import re

def solve(day, part, input, answer, args):
    print(f"Day {day} Solution.")
    values = []
    for row in input:
        values.append(calibration_value(row[0], part, args))
    # Remove None values, convert to int
    values = list(map(int, filter(lambda a: a is not None, values)))
    if args.verbose:
        print("All calibration values:")
        print(values)
    this_answer = sum(values)
    # Get the calibration value for each row
    # Add them up together (sum) to get answer for part one
    print(f"\t Part {part}: Sum of Calibration values = {this_answer}")
    if args.test:
        if this_answer == int(answer[0][0]):
            print("\t✅ Test passed!")
        else:
            print(f"\t❌ Test FAILED! Expected answer: {answer[0][0]}")

def calibration_value(row, part, args):
    # Get first and last digit
    # Combine them to get the calibration value
    if part == 1:
        match = re.findall(r'\d', row)
    if part == 2:
        # Find all matches even overlapping ones
        # In the end we only care about the first and last match
        match = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', row)

    first = match[0]
    last = match[-1]

    if part == 2:
        # Create a dictionary matching phonetic number strings to integers
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

        # Now replace phonetic number strings with their matching integer
        for k, v in phonetic_numbers.items():
            first = first.replace(k, str(v))
            last = last.replace(k, str(v))

    if len(match) >= 1:
        # first & last
        return ''.join([first, last])
    else:
        return
