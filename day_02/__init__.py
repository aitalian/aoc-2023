import re


class Game:
    id: int = 0
    red: int = 0
    green: int = 0
    blue: int = 0
    total: int = 0
    possible: bool = True

    def __init__(self, id, red=0, green=0, blue=0):
        self.id = id
        self.red = red
        self.green = green
        self.blue = blue

    def total(self):
        return sum(list([self.red, self.green, self.blue]))


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
        thisGame = Game(int(id))

        for round in game:
            # Strip whitespace for each round and split each colour
            round = [r.strip() for r in re.split(r',\ ', round)]
            for r in round:
                # Get the count for each colour and accumulate a total for the round
                hand = re.match(
                    r'(?P<cubes>\d+)\ (?P<color>red|green|blue)', r).groupdict()
                # Accumulate colours for this Game
                setattr(thisGame, hand['color'], getattr(
                    thisGame, hand['color']) + int(hand['cubes']))
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
        max_cubes = sum(bag_contains.values())

        for g in games:
            if args.verbose:
                print(vars(g))

            # Game is impossible if total cubes exceed the maximum
            if g.total() > max_cubes:
                g.possible = False
                if args.verbose:
                    print(
                        f"\t** Impossible game (id: {g.id}). Total cubes ({g.total()}) exceeds the maximum in the bag ({max_cubes}) 🙅‍♂️")
                continue

            # Check individual cube colour constraints
            if g.possible:
                for c in bag_contains:
                    if int(getattr(g, c)) > int(bag_contains[c]):
                        g.possible = False
                        if args.verbose:
                            print(
                                f"\t** Impossible game (id: {g.id}. Total {c} cubes ({getattr(g, c)}) exceeds the maximum in the bag ({bag_contains[c]}) 🙅‍♂️")
                        break

            if g.possible:
                if args.verbose:
                    print(f"\tGame id: {g.id} is possible 👍")
                possible_games.append(g.id)

        # FIXME: Getting answer of 200 (previously 839) for the sum but site says it's too low
        sum_of_possible_games = sum(map(int, possible_games))
        print(
            f"\tPart {part}: Sum of Possible Game IDs = {sum_of_possible_games}")
        if args.verbose:
            print(f"\tAll possible game IDs: {possible_games}")
        return sum_of_possible_games

    return
