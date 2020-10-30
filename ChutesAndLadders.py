import random

board = []
ladders_dict = {}
traps_dict = {}
p1_position = 1
p2_position = 1


def roll_dice():
    choice = random.randint(1,6)
    return choice


def make_board():
    for i in range(1, 101):
        board.append(i)
    j = 0
    while j < 6:
        ups()
        downs()
        j += 1
    return board


def ups():
    up_choice = random.choice(board)
    up_end_choice = random.choice(board)
    if up_choice >= up_end_choice:
        ups()
    else:
        if up_choice in traps_dict or up_choice in ladders_dict:
            ups()
        else:
            ladders_dict[up_choice] = up_end_choice


def downs():
    down_choice = random.choice(board)
    down_end_choice = random.choice(board)
    if down_choice <= down_end_choice:
        downs()
    else:
        if down_choice in traps_dict or down_choice in ladders_dict:
            downs()
        else:
            traps_dict[down_choice] = down_end_choice


def move(player,original_pos, new_pos):
    expected = original_pos + new_pos
    if expected in board:
        if expected in ladders_dict:
            print(f'-------------------------')
            print(f'{player} original:{original_pos}+ roll: {new_pos} = expected {expected} found in ladders, leads to {ladders_dict[expected]}')
            final = ladders_dict[expected]
            print(f'current position: {final}')
        elif expected in traps_dict:
            print(f'-------------------------')
            print(f'{player} original:{original_pos}+ roll: {new_pos} = expected {expected} found in traps, leads to  {traps_dict[expected]}')
            final = traps_dict[expected]
            print(f'current position: {final}')
        else:
            print(f'-------------------------')
            print(f'{player} original:{original_pos}+ roll: {new_pos} = expected {expected}')
            final = expected
            print(f'current position: {final}')
    else:
        print(f'-------------------------')
        print(f'{player} original:{original_pos}+ roll: {new_pos} = expected {expected}')
        final = 100
        print(f'current position: {final}')
    return final


def play():
    global p1_position, p2_position
    while True:
        if p1_position == 100 or p2_position == 100:
            print('-----------------------')
            print(f'we have a winner. Results P1: {p1_position} | P2:{p2_position}')
            break
        p1_position = move('Player 1', p1_position, roll_dice())
        p2_position = move('Player 2', p2_position, roll_dice())


print(make_board())
print('Ladders: ', ladders_dict)
print('Traps: ', traps_dict)
play()
