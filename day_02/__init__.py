import re


class Game:
    id: int
    red: int
    green: int
    blue: int

    def __init__(self, id, red=0, green=0, blue=0):
        self.id = id
        self.red = red
        self.green = green
        self.blue = blue


def solve(day, part, input, args):
    print(f"Day {day} Solution.")

    games = []

    for row in input:
        game = re.split(r'Game\ (\d+):\ ', row[0])
        # Remove the empty first value in the list
        game.pop(0)
        # Next value is the game id; remaining values are each round
        id = game.pop(0)
        game = game + row[1:]

        # Initialize a new Game object for this game
        thisGame = Game(id)

        for round in game:
            # Strip whitespace for each round and split each colour
            round = [r.strip() for r in re.split(r',\ ', round)]
            for r in round:
                # Get the count for each colour and accumulate a total for the round
                hand = re.findall(r'(\d)\ (red|green|blue)', r)
                # Accumulate colours for this Game
                setattr(thisGame, hand[0][1], getattr(thisGame, hand[0][1]) + int(hand[0][0]))
        games.append(thisGame)

    if args.verbose:
        print(f"\tNumber of Games counted: {len(games)}")

    if part == 1:
        # Track possible games
        possible_games = []

        # Define constraints of coloured cubes in the bag
        bag_contains = {
            'red': 12,
            'green': 13,
            'blue': 14
        }

        # Check each game and determine if it was possible based on the coloured cube count constraints
        # TODO: Getting answer of 839 for the sum but site says it's too low
        for g in games:
            if g.red <= bag_contains['red'] and g.green <= bag_contains['green'] and g.blue <= bag_contains['blue']:
                possible_games.append(g.id)

        sum_of_possible_games = sum(map(int, possible_games))
        print(
            f"\tPart {part}: Sum of Possible Game IDs = {sum_of_possible_games}")
        if args.verbose:
            print(f"\tAll possible game IDs: {possible_games}")
        return sum_of_possible_games

    return
