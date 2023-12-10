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
        self.total = 0
        self.possible = True

    def calculateTotal(self):
        self.total = sum(list([self.red, self.green, self.blue]))
        return self.total

    def calculatePower(self):
        return self.red * self.green * self.blue


class Round(Game):
    round: int = 0

    def __init__(self, round, gameid):
        super().__init__(gameid)
        self.round = round


def solve(day, part, input, args):
    print(f"Day {day} Solution.")

    games = []
    rounds = []

    for row in input:
        game = re.split(r'Game\ (\d+):\ ', row[0])
        # Remove the empty first value in the list
        game.pop(0)
        # Next value is the game id; remaining values are each round
        gameId = game.pop(0)
        game = game + row[1:]
        thisGame = Game(int(gameId))

        for id, round in enumerate(game):
            # Strip whitespace for each round and split each colour
            round = [r.strip() for r in re.split(r',\ ', round)]
            thisRound = Round(int(id)+1, int(gameId))
            for cubes in round:
                # Get the count for each colour and accumulate a total for the round
                hand = re.match(
                    r'(?P<cubes>\d+)\ (?P<colour>red|green|blue)', cubes).groupdict()
                # Accumulate colours for this Round
                setattr(thisRound, hand['colour'], getattr(
                    thisRound, hand['colour']) + int(hand['cubes']))
                thisRound.calculateTotal()
                # Get the total number of each coloured cubes for the Game (not just round)
                if getattr(thisGame, hand['colour']) < int(hand['cubes']):
                    # Set this as the new max num of cubes for this colour
                    setattr(thisGame, hand['colour'], int(hand['cubes']))
            rounds.append(thisRound)
        games.append(thisGame)

    if args.verbose:
        print(f"\tNumber of Games counted: {len(rounds)}")

    # Track possible and impossible game ids
    # Individually we also track if rounds are possible on the object itself
    possible_games = []
    impossible_games = []

    # Define constraints of coloured cubes in the bag
    bag_contains = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    # Check each game and determine if it was possible based on the coloured cube count constraints
    max_cubes = sum(bag_contains.values())

    for g in rounds:
        if args.verbose:
            print(vars(g))

        if g.possible is False or g.id in impossible_games:
            g.possible = False
            if g.id in possible_games:
                possible_games.remove(g.id)
            if args.verbose:
                print(
                    f"\t** Skipping game (id: {g.id}, round: {g.round}). Game already marked not possible.")
                print(f"\t" + str(vars(g)))
            continue

        # Game is impossible if total cubes in the round exceed the maximum
        if g.calculateTotal() > max_cubes:
            g.possible = False
            impossible_games.append(g.id)
            if g.id in possible_games:
                possible_games.remove(g.id)

            if args.verbose:
                print(
                    f"\t** Impossible game (id: {g.id}, round: {g.round}). Total cubes ({g.total}) exceeds the maximum in the bag ({max_cubes}) 🙅‍♂️")
            continue

        # Check individual cube colour constraints
        if g.possible:
            for c in bag_contains:
                if int(getattr(g, c)) > int(bag_contains[c]):
                    g.possible = False
                    impossible_games.append(g.id)
                    if g.id in possible_games:
                        possible_games.remove(g.id)
                    if args.verbose:
                        print(
                            f"\t** Impossible game (id: {g.id}, round: {g.round}). Total {c} cubes ({getattr(g, c)}) exceeds the maximum in the bag ({bag_contains[c]}) 🙅‍♂️")
                    break

        if g.possible:
            if args.verbose:
                print(f"\tGame id: {g.id} is possible 👍")
            if g.id not in possible_games:
                possible_games.append(g.id)
        if args.verbose:
            print(f"\t" + str(vars(g)))

    if part == 1:
        sum_of_possible_games = sum(map(int, possible_games))
        print(
            f"\tPart {part}: Sum of Possible Game IDs = {sum_of_possible_games}")
        if args.verbose:
            print(f"\tAll possible game IDs: {possible_games}")
        return sum_of_possible_games

    if part == 2:
        # Go through each Game
        # Calculate the power by multiplying the max cube count of each colour together
        # Finally, add up all of the powers to return the sum
        power = []

        for g in games:
            thisPower = g.calculatePower()
            if args.verbose:
                print(f"\tGame (id: {g.id}) has a Power value of: {thisPower}")
            power.append(thisPower)

        sum_of_power = sum(map(int, power))

        print(
            f"\tPart {part}: Sum of Power for possible games = {sum_of_power}")

        return sum_of_power

    return
