from redis import Redis
from decouple import config

redis = Redis(host=config("REDIS_HOST"), port=config("REDIS_PORT"), db=config("REDIS_DB"))


def set_data(key, data, ex=None):
    try:
        redis.set(key, data, ex=ex)
    except Exception as err:
        pass
    redis.close()


def get_data(key):
    try:
        data = redis.get(key)
        redis.close()
        return data
    except:
        redis.close()
        return None


def delete_data(key):
    redis.delete(key)
    redis.close()
