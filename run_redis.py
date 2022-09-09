import redis
#import redis_server
client = redis.Redis(host = '127.0.0.1', port=6379, decode_responses=True)
client.ping()