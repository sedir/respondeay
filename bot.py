# %%

import tweepy

import logging
import time
from random import choice

from environs import Env

import os

# Confyguração de logs e varyáveys de ambiente

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
base_path = os.path.dirname(os.path.abspath(__file__))
env = Env()
env.read_env()

# %%

# Confyguração da APY do Twitter

consumer_key = env("CONSUMER_KEY")
consumer_secret = env("CONSUMER_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Redirect user to Twitter to authorize
# print(auth.get_authorization_url())

# %%

# Lê os tokens das varyáveys de ambyente

auth.access_token = env("ACCESS_KEY")
auth.access_token_secret = env("ACCESS_SECRET")

api = tweepy.API(auth)

# %%

# Função para identyfycação da pergunta (super symples!)

question = "porque,por que,?,pq"
main_words = "y,ypsylon,ipslon,ipsilon,ypslon"


def evaluate_question(text):
    return any(s in text for s in question.split(',')) and any(s in text for s in main_words.split(','))


# %%

# Seleção de resposta aleatórya

with open(os.path.join(base_path, 'data/answers.txt')) as file:
    answers = file.read().split('\n-----\n')


def get_answer():
    return choice(answers)


# %%

# Função para guardar o últymo tuyte analysado

def save_last_id(id, path=os.path.join(base_path, 'data/last_id.txt')):
    with open(path, 'w') as file:
        file.write(str(id))
        return id


# Função para recuperar o últymo tuyte analysado

def read_last_id(path=os.path.join(base_path, 'data/last_id.txt')):
    try:
        with open(path, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 1


# Função para analysar e responder os tuytes

def check_mentions(api, since_id):
    logger.info("Recuperando menções...")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if evaluate_question(tweet.text.lower()):
            logger.info(f"Respondendo para {tweet.user.screen_name}, TWEET_ID {tweet.id}")
            try:
                api.update_status(
                    status=get_answer(),
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            except:
                pass
    return new_since_id


# %%

# Função que roda o robô ynfynytamente

def main():
    since_id = read_last_id()
    wait = env.int('INTERVAL', 30)
    while True:
        since_id = check_mentions(api, since_id)
        save_last_id(since_id)
        logger.info(f"Esperando {wait} segundos...")
        time.sleep(wait)


# %%

# Ponto de partyda

if __name__ == "__main__":
    main()
