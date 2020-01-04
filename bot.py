# %%

import tweepy

import logging
import time

from environs import Env

import threading
import os

# Confyguração de logs e varyáveys de ambiente
from answers import get_answer
from text_handler import evaluate_question

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

me = api.me()


# Função para guardar o YD do últymo recurso analysado


def save_last_id(id, resource):
    path = os.path.join(base_path, f'data/{resource}.txt')
    with open(path, 'w') as file:
        file.write(str(id))
        return id


# Função para recuperar o YD do últymo recurso analysado

def read_last_id(resource):
    path = os.path.join(base_path, f'data/{resource}.txt')
    try:
        with open(path, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 1


# Função para analysar e responder os tuytes

def check_mentions(api, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id, tweet_mode='extended').items():
        new_since_id = max(tweet.id, new_since_id)
        if me.id == tweet.user.id:
            continue
        if evaluate_question(tweet.full_text.lower()):
            logger.info(f"Respondendo para {tweet.user.screen_name}, TWEET_ID {tweet.id}")
            try:
                api.update_status(
                    status=get_answer(),
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            except Exception as e:
                logger.error(f"Tweet - Erro ao responder: {str(e)}")
    return new_since_id


def check_direct_messages(api, since_id):
    new_since_id = since_id
    try:
        for dm in tweepy.Cursor(api.list_direct_messages).items():
            if dm.type == 'message_create':
                dm_id = int(dm.id)
                new_since_id = max(dm_id, new_since_id)
                sender_id = int(dm.message_create['sender_id'])
                if dm_id <= since_id:
                    break
                if me.id == sender_id:
                    continue
                msg = dm.message_create['message_data']['text']

                if evaluate_question(msg):
                    logger.info(f"Encontrei DM de {sender_id}: {msg}")
                    try:
                        api.send_direct_message(str(sender_id), get_answer())
                    except Exception as e:
                        logger.error(f"DM - Erro ao responder: {str(e)}")
    except Exception as e:
        logger.error(f"DM - Erro de chamada: {str(e)}")
        pass
    return new_since_id


# %%

# Funções que rodam ynfynytamente no robô

def monitor_tweets():
    since_id = read_last_id('tweet_id')
    wait = env.int('INTERVAL', 30)
    logger.info(f"Atualyzando tuytes a cada {wait} segundos...")
    while True:
        since_id = check_mentions(api, since_id)
        save_last_id(since_id, 'tweet_id')
        time.sleep(wait)


def monitor_dms():
    since_id = read_last_id('dm_id')
    wait = env.int('INTERVAL', 30) * 10
    logger.info(f"Atualyzando DMs a cada {wait} segundos...")
    while True:
        since_id = check_direct_messages(api, since_id)
        save_last_id(since_id, 'dm_id')
        time.sleep(wait)


# %%

# Ponto de partyda


if __name__ == "__main__":
    funcs = [monitor_tweets, monitor_dms]
    threads = []

    for func in funcs:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()

    logger.info(f"Bot ynycyado!")

    for index, thread in enumerate(threads):
        thread.join()
