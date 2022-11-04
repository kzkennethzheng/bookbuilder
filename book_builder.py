import requests

#session = berserk.TokenSession(token)
#client = berserk.Client(session=session)

def query_params(speeds=['rapid'], ratings=['2000'], nmoves=10, moves=[]):
    param_str = ''
    param_str += 'speeds=' + ','.join(speeds)
    param_str += '&ratings=' + ','.join(ratings)
    param_str += '&moves=' + str(nmoves)
    param_str += '&play=' + ','.join(moves)
    return param_str


def get_popularity(move):
    return move['white'] + move['black'] + move['draws']

def sort_by_wins(moves, white):
    if white:
        moves.sort(key=lambda x: x['white'] / get_popularity(x), reverse=True)
    else:
        moves.sort(key=lambda x: x['black'] / get_popularity(x), reverse=True)

def moves_str(moves):
    output = ''
    i = 1
    white = True
    for move in moves:
        if white:
            output += str(i) + '. ' + move
            white = False
        else:
            output += ' ' + move + '\n'
            white = True
            i += 1
    return output

edpt = 'https://explorer.lichess.ovh/lichess?'
move_list = [['d2d4']]
continuations = [['d4']]

BREADTH = 3
DEPTH = 3

for i in range(DEPTH):
    new_moves = []
    new_continuations = []
    for j, moves in enumerate(move_list):
        responses = requests.get(edpt + query_params(moves=moves, nmoves=BREADTH)).json()['moves']
        if i % 2 == 1: # you play most winning response
            sort_by_wins(responses, True)
            new_moves.append(moves + [responses[0]['uci']])
            new_continuations.append(continuations[j] + [responses[0]['san']])
        else: # opponent plays BREADTH most popular responses
            for new_move in responses:
                new_moves.append(moves + [new_move['uci']])
                new_continuations.append(continuations[j] + [new_move['san']])
    move_list = new_moves
    continuations = new_continuations
                
for i, c in enumerate(continuations):
    print('Continuation ' + str(i) + ':')
    print(moves_str(c))
