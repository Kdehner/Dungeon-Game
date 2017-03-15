import random
import os

# draw grid
# pick random location for player
# pick random location for exit door
# pick random location for monster
# draw player in grid
# take input for movement
# move player, unless invalid move (pas edges of grid)
# check for win/lose
# clear screen and redraw grid

CELLS = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
         (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
         (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
         (0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
         (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_locations():
    return random.sample(CELLS ,3)

def move_player(player, move):
    # get the player's location
    x, y = player['location']
    # if move == LEFT, x-1
    if move == 'LEFT':
        x -= 1
    # if move == RIGHT, x+1
    if move == 'RIGHT':
        x += 1
    # if move == UP, y-1
    if move == 'UP':
        y -= 1
    # if move == DOWN, y+1
    if move == 'DOWN':
        y += 1

    return x, y

def get_moves(player):
    moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']
    x, y = player['location']
    # if player's y == 0, they can't move UP
    if y == 0:
        moves.remove('UP')
    # if player's y == 4, they can't move DOWN
    if y == 4:
        moves.remove('DOWN')
    # if player's x == 0, they can't move LEFT
    if x == 0:
        moves.remove('LEFT')
    # if player's x == 4, they can't move RIGHT
    if x == 4:
        moves.remove('RIGHT')

    return moves

def draw_map(location, moves):
    print(' _'*5)
    tile = '|{}'

    for cell in CELLS:
        x, y = cell
        if x < 4:
            line_end=''
            if cell == location:
                output = tile.format('X')
            elif cell in moves:
                output = tile.format('.')
            else:
                output = tile.format('_')
        else:
            line_end = '\n'
            if cell == location:
                output = tile.format('X|')
            elif cell in moves:
                output = tile.format('.|')
            else:
                output = tile.format('_|')
        print(output, end=line_end)

def game_loop(debug):
    player = {'location': None, 'moves': []}
    monster, door, player['location'] = get_locations()
    playing = True
    debug = debug

    while playing:
        clear_screen()
        draw_map(**player)
        valid_moves = get_moves(player)

        if debug == True:
            print('** DEBUG MODE **')
            print('MONSTER: ', monster, 'DOOR: ', door, 'PLAYER: ', player['location'])

        print('You\'re currently in room {}'.format(player['location']))
        print('You can move {}.'.format(', '.join(valid_moves)))
        print('Enter QUIT to quit')

        move = input('> ')
        move = move.upper()

        if move == 'QUIT':
            print('\n ** See you next time! **\n')
            break

        if move == 'DEBUG':
            if debug == True:
                input('\n ** EXITING DEBUG MODE **\n')
                debug = False
                continue
            else:
                input('\n ** ENTERING DEBUG MODE **\n')
                debug = True
                continue

        # Good move? Change player position
        if move in valid_moves:
            player['moves'].append(player['location'])
            player['location'] = move_player(player, move)

            # On the monster? They lose!
            if player['location'] == monster:
                print('\n ** Oh no! The monster got you! Better luck next time! **\n')
                playing = False

            if player['location'] == door:
                print('\n ** You escaped! Congratulations! **\n')
                playing = False

            # Bad Move? Don't change anything!
        else:
            input('\n ** Walls are hard! Don\'t run into them! **\n')
        # On the door? They Win!
        # Otherwise, loop back around
    else:
        if input('Play again? [Y/n] ').lower() != 'n':
            game_loop(debug)

clear_screen()
print('Welcome to the dungeon')
input('Press return to start!')
clear_screen()
game_loop(False)
