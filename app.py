# import flask to run the backend
from reply_tree import build_reply_tree
import json

def get_reply_tree_by_id():
    {"user": {"screen_name": "HumanoidHistory"}, "id": 970447777053462528}


def get_reply_tree_by_url(url_in):
    """
    give me the url, and i will give you the reply tree (after a long while)
    ---
    parameters:
      - name: url
        in: query
        type: string
        required: true
        default: https://twitter.com/fchollet/status/1044465230317645824
    responses:
      200:
        description: returns a json dictionary representing a reply tree
        schema:
          id: replyTree
          properties:
            results:
              type: json
              default: {
                    "text": "the tweet of your interest",
                    "url": "the tweet's url",
                    "images": "the tweet's image url if it exists",
                    "retweets": "how many retweets",
                    "favourites": "how many favorites",
                    "sentiment": "sentiment of the tweet, as a dictionary",
                    "entities": "entities of the tweet, as a dictionary",
                    "children": "tweet dictionaries in the similar format as above, representing reply tweets"
                }
            status:
              type: number
              default: 200
    """

    result = build_reply_tree(url_in)
    return result


if __name__ == "__main__":
    twitter_url = "https://twitter.com/fchollet/status/1044304738186014720"

    r = get_reply_tree_by_url(twitter_url)
    with open("dummy.json", "w") as d:
        json.dump(r, d, ensure_ascii=False, indent=4)

    print(json.dumps(r, indent=4, ensure_ascii=False))
