import os
from random import choice

# Seleção de resposta aleatórya
from tweepy import DirectMessage

base_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base_path, 'data/answers.txt')) as file:
    answers = file.read().split('\n-----\n')


def get_answer():
    return choice(answers)
