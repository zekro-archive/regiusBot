import twitter
import json


with open("twittersecrets.json") as f:
    secrets = json.load(f)


api = twitter.Api(consumer_key=secrets["consumer"]["key"],
                  consumer_secret=secrets["consumer"]["secret"],
                  access_token_key=secrets["access"]["key"],
                  access_token_secret=secrets["access"]["secret"])


def post_media(content, media):
    api.PostMedia(content, media)
