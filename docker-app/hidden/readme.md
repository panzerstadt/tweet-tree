# things needed
- hidden.py
- hidden.json

## how to add the hidden.json
#### its for google's API

1. go to https://console.cloud.google.com/
2. make sure you have a [project](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
3. go to menu > APIs & Services > Credentials
4. do a 'create credentials', set it to 'Service account key', in a JSON format
5. this will auto-download the JSON file. copy paste it into `/hidden` folder and rename it to `hidden.json`
6. make sure you add it to `.gitignore` if you haven't, so that you don't upload your access code to ALL YOUR GOOGLE CLOUD


## how to add the hidden.py
#### its for twitter's API

1. make a Twitter class
2. define an init with 4 attributes:
    ```
    class Twitter:
        def __init__(self):
            self.consumer_key = 'YOUR CONSUMER KEY'
            self.consumer_secret = 'YOUR CONSUMER SECRET'
            self.access_token_key = 'YOUR ACCESS TOKEN KEY'
            self.access_token_secret = 'YOUR ACCESS TOKEN SECRET'
    ```

3. have coffee.
4. make sure you add it to `.gitignore` if you haven't, so as not to upload your twitter app key to the world.