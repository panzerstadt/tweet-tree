# import flask to run the backend
# flask stuff
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# interface
from flasgger import Swagger

# the actual logic
from reply_tree import build_reply_tree
import json


# CORS settings (right now, its just everything, so it's not super safe, might be DDOSed)
allowed_domains = [
    r'*'
]

# make that flask app
application = Flask(__name__)
# wrap an automated interface, accessible at /apidoc
Swagger(application)
# wrap the CORS to allow inter-app communication
CORS(application, origins=allowed_domains, resource=r'/v1/*', supports_credentials=True)
    # IMPORTANT: supports_credentials allows COOKIES and CREDENTIALS to be submitted across domains
    # more CORS settings here: https://flask-cors.corydolphin.com/en/latest/api.html#extension
    # github example: https://github.com/corydolphin/flask-cors/blob/master/examples/app_based_example.py
# prevent autosorting of keys in json output
application.config["JSON_SORT_KEYS"] = False


def get_reply_tree_by_id():
    """
    not yet implemented
    :return:
    """
    pass


@application.route('/v1/tweets/tree', methods=['GET'])
def get_reply_tree_by_url():
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
    try:
        url_in = request.args.get('url')
    except:
        print('no url detected. returning a default')
        url_in = "https://twitter.com/fchollet/status/1044304738186014720"

    result = build_reply_tree(url_in)

    # save a backup copy
    with open("temp.json", "w") as d:
        json.dump(result, d, ensure_ascii=False, indent=4)

    return jsonify(result)


@application.route('/')
def home():
    message_1 = "please visit /apidocs for the API"
    message_2 = "or visit /v1/tweets/tree?url=YOUR-TWITTER-URL-OF-INTEREST"
    message_3 = "for some interesting stuff"
    return render_template('index.html', message_1=message_1, message_2=message_2, message_3=message_3)


if __name__ == "__main__":
    # this is only for development purposes. when using docker, gunicorn will run and not these lines.
    # if running dockerfile for heroku, the production PORT will be assigned randomly at runtime
    application.run(host="0.0.0.0", port="5000", debug=False)
    print('a flask app is initiated at {0}'.format(application.instance_path))

