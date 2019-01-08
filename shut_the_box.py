__author__ = 'Dave Paquette'

# docstring
'''
Program to play "Shut the Box" and tally results
'''

from random import *
import pandas as pd
import csv

counter = 0

class Game():
    def __init__(self):
        self.d1 = 0
        self.d2 = 0
        self.total = 0
        self.count = 0
        self.rolls = []
        self.board = [1,2,3,4,5,6,7,8,9,10,11,12]
        self.score = None

class Log():
    fout = None
    times = None
    score = []
    count = []
    board = []
    gNums = []

def main():
    log = Log()
    getParameters(log)
    #loop to play that many times
    for i in range (log.times):
        # create new game
        g = Game()
        # play the game until it's over (over when score != None)
        while g.score == None:
            rollDice(g)
            reduce_board(g)
            if sum(g.board) == 0:
                g.score = 0
                break
        # record score, count, board, and current game number in Log
        log.score.append(g.score)
        log.count.append(g.count)
        log.board.append(g.board)
        log.gNums.append(i + 1)
    # write scores to file/memory
    temp = {'Score':log.score,'Dice Rolls':log.count,'Final Board':log.board,'Game Count':log.gNums}
    results = pd.DataFrame(data = temp)
    results.to_csv(log.fout)
    print('finished')

def getParameters(log):
    # get number of games to play
    log.times = int(input('Enter number of games to play:\n\t-> '))
    log.fout = input('Enter complete filepath of write file:\n\t-> ')
    return log

def rollDice(g):
    g.d1 = randint(1,6)
    g.d2 = randint(1,6)
    g.total = g.d1 + g.d2
    g.count = g.count + 1
    return g

def reduce_board(g):
    # find pairs
    lowest_pair = pairs(target = g.total, board = g.board)
    lowest_triple = triples(target = g.total,board = g.board)

    if g.total in g.board:
        temp = g.board.index(g.total)
        g.rolls.append({'roll':g.count,'d1':g.d1,'d2':g.d2,'deleted':g.total})
        del g.board[temp]
    elif lowest_pair != None:
        g.rolls.append({'roll':g.count,'d1':g.d1,'d2':g.d2,'deleted':[g.board[lowest_pair[0]],g.board[lowest_pair[1]]]})
        for i in sorted(lowest_pair, reverse=True):
            del g.board[i]
    elif lowest_triple != None:
        g.rolls.append({'roll':g.count,'d1':g.d1,'d2':g.d2,'deleted':[g.board[lowest_triple[0]],g.board[lowest_triple[1]],g.board[lowest_triple[2]]]})
        for i in sorted(lowest_triple, reverse=True):
            del g.board[i]
    else:
        g.rolls.append({'roll':g.count,'d1':g.d1,'d2':g.d2,'deleted':'none'})
        g.score = sum(g.board)

def find(x,inList):
    try:
        index = inList.index(x)
        return index
    except ValueError:
        return None

def pairs(target,board):
    for i in board:
        pair = target - i
        temp = find(pair,board)
        if temp != None and i != board[temp]:
            out = [board.index(i),temp]
            break
        else:
            out = None
    return out

def triples(target,board):
    for i in board:
        pair_sum = target - i
        found_pair = pairs(pair_sum,board)
        if found_pair != None and board.index(i) != found_pair[0] and board.index(i) != found_pair[1] and found_pair[0] != found_pair[1]:
            out = [board.index(i),found_pair[0],found_pair[1]]
            break
        else:
            out = None
    return out

if __name__ == '__main__':
    main()
