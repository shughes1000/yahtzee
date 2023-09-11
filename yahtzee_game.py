import numpy as np


def display_scoreboard(scoreboard, turn):
    print()
    print('SCOREBOARD')
    print('----------')
    for k, v in scoreboard.items():
        print(f'{k}: {v}')
    print()
    numbers_score = sum({k: v for k, v in scoreboard.items() if k.endswith('s') and v is not None}.values())
    total_score = sum({k: v for k, v in scoreboard.items() if v is not None}.values())
    if numbers_score >= 63:
        total_score += 35
    print(f'Numbers Score: {numbers_score}')
    if turn == 13:
        print(f'FINAL SCORE: {total_score}')
        print('Thank you for playing!')
    else:
        print(f'Total Score: {total_score}')
    print()


def roll_dice(dice):
    new_dice = []
    for d in dice:
        if d is None:
            new_dice.append(np.random.randint(1, 7))
        else:
            new_dice.append(d)
    return new_dice


def check_kinds(dice, category):
    for freq in set(np.unique(dice, return_counts=True)[1]):
        if freq >= category:
            return True
    return False


def check_full_house(dice):
    return set(np.unique(dice, return_counts=True)[1]) == {2, 3}


def check_straights(dice, sequence_length):
    sorted_dice = sorted(set(dice))
    for i in range(len(sorted_dice) - sequence_length + 1):
        if all(sorted_dice[i + j] == sorted_dice[i] + j for j in range(sequence_length)):
            return True
    return False


def check_yahtzee(dice):
    return set(np.unique(dice, return_counts=True)[1]) == {5}


def update_score(scoreboard, decision, dice):
    # make sure category has not been played yet
    # should not ever happen due to earlier checks
    if scoreboard[decision] is not None:
        raise ValueError(f'You have already played {decision}!')
    if decision == 'Ones':
        score = dice.count(1) * 1
        scoreboard[decision] = score
    elif decision == 'Twos':
        score = dice.count(2) * 2
        scoreboard[decision] = score
    elif decision == 'Threes':
        score = dice.count(3) * 3
        scoreboard[decision] = score
    elif decision == 'Fours':
        score = dice.count(4) * 4
        scoreboard[decision] = score
    elif decision == 'Fives':
        score = dice.count(5) * 5
        scoreboard[decision] = score
    elif decision == 'Sixes':
        score = dice.count(6) * 6
        scoreboard[decision] = score
    elif decision == 'Three of a Kind':
        if check_kinds(dice, 3):
            score = sum(dice)
        else:
            score = 0
        scoreboard[decision] = score
    elif decision == 'Four of a Kind':
        if check_kinds(dice, 4):
            score = sum(dice)
        else:
            score = 0
        scoreboard[decision] = score
    elif decision == 'Full House':
        if check_full_house(dice):
            score = 25
        else:
            score = 0
        scoreboard[decision] = score
    elif decision == 'Small Straight':
        if check_straights(dice, 4):
            score = 30
        else:
            score = 0
        scoreboard[decision] = score
    elif decision == 'Large Straight':
        if check_straights(dice, 5):
            score = 40
        else:
            score = 0
        scoreboard[decision] = score
    elif decision == 'Yahtzee':
        if check_yahtzee(dice):
            score = 50
        else:
            score = 0
        scoreboard[decision] = score
    elif decision == 'Chance':
        score = sum(dice)
        scoreboard[decision] = score
    return scoreboard, score


def reroll_dice(dice):
    decision = str(input(
        "Please press the relevant keys for the numbers you would like to play.\n"
    ))
    kept_dice = []
    if 'Q' in decision:
        kept_dice.append(dice[0])
    else:
        kept_dice.append(None)
    if 'W' in decision:
        kept_dice.append(dice[1])
    else:
        kept_dice.append(None)
    if 'E' in decision:
        kept_dice.append(dice[2])
    else:
        kept_dice.append(None)
    if 'R' in decision:
        kept_dice.append(dice[3])
    else:
        kept_dice.append(None)
    if 'T' in decision:
        kept_dice.append(dice[4])
    else:
        kept_dice.append(None)
    return kept_dice


def play_category(dice, scoreboard, turn):
    decision = 'N'
    while decision not in scoreboard.keys():
        decision = str(input(
            "Please type the name of the category you would like to play.\n"
        ))
        if decision not in scoreboard.keys():
            print(f'Sorry, "{decision}" is not a valid entry.')
        elif scoreboard[decision] is not None:
            print(f'You have already played {decision}!')
            decision = 'N'

    scoreboard, score = update_score(scoreboard, decision, dice)
    print(f'You scored {score} for {decision}.')
    display_scoreboard(scoreboard, turn)
    return scoreboard


def play_turn(scoreboard, turn):
    dice = [None, None, None, None, None]
    for roll in range(1, 4):
        print(f'Roll {roll}')
        dice = roll_dice(dice)
        print(" ".join(str(d) for d in dice))
        print("Q W E R T")
        if roll == 3:
            return play_category(dice, scoreboard, turn)
        else:
            choice = 'N'
            while (choice != "1") and (choice != "2"):
                choice = str(input(
                    "Please press the corresponding number to make a choice.\n"
                    "1. Play a category\n"
                    "2. Reroll\n"
                ))
                if (choice != "1") and (choice != "2"):
                    print('Sorry, you need to type "1" or "2" to make a choice.')
            if choice == "1":
                return play_category(dice, scoreboard, turn)
            elif choice == "2":
                roll += 1
                dice = reroll_dice(dice)


def play_yahtzee():
    scoreboard = {
        'Ones': None,
        'Twos': None,
        'Threes': None,
        'Fours': None,
        'Fives': None,
        'Sixes': None,
        'Three of a Kind': None,
        'Four of a Kind': None,
        'Full House': None,
        'Small Straight': None,
        'Large Straight': None,
        'Yahtzee': None,
        'Chance': None
    }

    # start = 'N'
    # while start != 'Y':
    #     start = str(input('Ready to play?\nType "Y" when ready.\n'))

    for turn in range(1, 14):
        print(f'Turn {turn}')
        scoreboard = play_turn(scoreboard, turn)


if __name__ == '__main__':
    play_yahtzee()
