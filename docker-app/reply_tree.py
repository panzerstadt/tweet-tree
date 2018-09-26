# twitter stuff
from utils.tweet_replies_api import get_tweet_from_twitter_url, get_tweet_status, get_replies
# natural language stuff
from utils.google_api import analyze_entities_and_sentiment

import json

def tweet_tree_dict(text="", url="", images="", retweets="", favourites="", sentiment=None, entities=None, children=None):
    return {
        "text": text,
        "url": url,
        "images": images,
        "retweets": retweets,
        "favourites": favourites,
        "sentiment": sentiment,
        "entities": entities,
        "children": children
    }


def generate_reply_tree(tweet_object):
    status = get_tweet_status(tweet_object.id).AsDict()
    # the tweet as a dictionary object
    # --------------------------------
    # init
    original_tweet = tweet_tree_dict()
    # tweet
    original_tweet['text'] = status['text']
    # wehre to find it
    original_tweet['url'] = "https://twitter.com/anyuser/status/{}".format(status['id'])
    # how hot is it
    try:
        original_tweet['retweets'] = status['retweet_count']
    except KeyError:
        original_tweet['retweets'] = 0
    # how hot is it
    try:
        original_tweet['favourites'] = status['favorite_count']
    except KeyError:
        original_tweet['favourites'] = 0
    # images
    try:
        imgs = status['media']
        original_tweet['images'] = [m["media_url_https"] for m in imgs]
    except KeyError:
        user_img = status['user']['profile_image_url_https']
        original_tweet['images'] = [user_img]
    # sentiment (calls google API)
    # entities (calls google API)
    nlp_dict = analyze_entities_and_sentiment(status['text'])
    original_tweet['sentiment'] = nlp_dict['sentiment']
    original_tweet['entities'] = nlp_dict['entities']

    # all replies to this tweet as a list of tweet objects (calls get_reply()) then recursively runs tweet dict generation
    # uses the class Tweet (similar to python.twitter)
    # which of the replies match? this is dealt with in tweet_replies_api.py
    original_tweet['children'] = []
    replies = get_replies(tweet_object)
    for r in replies:
        # r is a tweet object, used to recursively generate the dictionary the same way the first tweet does
        original_tweet['children'].append(generate_reply_tree(r))

    # return the original tweet with all its replies connected to it as a dictionary with dictionaries inside it
    #print(json.dumps(original_tweet, indent=4, ensure_ascii=False))
    return original_tweet


def build_reply_tree(twitter_url="https://twitter.com/mincos_magazine/status/1026406786079764482"):
    # get all replies with recursion
    # then build the tree as a graph
    """
    :return:
    """
    tweet_object = get_tweet_from_twitter_url(twitter_url)
    status = get_tweet_status(tweet_object.id).AsDict()  # not used downstream(?)

    # from all these, i only want text, rt, favourite, image
    print('tweet of interest:')
    print(json.dumps(status, indent=4, ensure_ascii=False))

    return generate_reply_tree(tweet_object)


if __name__ == "__main__":
    # r = build_reply_tree(twitter_url="https://twitter.com/mubappemubappe/status/1044424511431430144")
    # print(json.dumps(r, indent=4, ensure_ascii=False))
    r = build_reply_tree()

    with open("dummy.json", "w") as d:
        json.dump(r, d, ensure_ascii=False, indent=4)
    print(json.dumps(r, indent=4, ensure_ascii=False))