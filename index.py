import os, json, time, tempfile, sys, io, urllib, requests
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

auth = OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret'])
auth.set_access_token(os.environ['access_token'], os.environ['access_token_secret'])

class TweetListener(StreamListener):
    def on_data(self, data):
        print('Got tweet')
        tweet = json.loads(data)
        print(tweet)
        if (tweet['entities'] and tweet['entities']['media']):
            print(tweet['entities']['media'])
            media = tweet['entities']['media'][0]
            if (media['type'] == 'photo'):
                print("Ooooo a photo")
                image_data = urllib.urlopen(media['media_url_https']).read()

                headers = {'X-Callback-Url': 'http://gateway:8080/async-function/tweetpic'}
                json_data = json.dumps({
                    "image": image_data,
                    "status_id": tweet['id_str']
                })
                requests.post('http://gateway:8080/async-function/colorization', data=json_data, headers=headers)
                if (r.status_code == requests.codes.ok):
                    print("Colorization succeeded for " + image_url)
                else:
                    print("Colorization failed for -> " + media['media_url_https'])

    def on_error(self, status):
        print('Error from tweet streamer', status)

if __name__ == '__main__':
    print('Setting up')
    l = TweetListener()
    stream = Stream(auth, l)

    print('Listening for tweets')
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['#colouriseme', '#colorizeme', '#coloriseme'])
