import os, json, time, tempfile, sys, io, urllib, requests
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

auth = OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret'])
auth.set_access_token(os.environ['access_token'], os.environ['access_token_secret'])

class StdOutListener(StreamListener):
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

                r = requests.post(os.environ['colorization_url'], data=image_data)
                if (r.status_code == requests.codes.ok):
                    image_url = r.text.strip()
                    print("Colorization succeeded for " + image_url)
                    r = requests.post(os.environ['tweetpic_url'], data=json.dumps({
                        "status_id": tweet['id_str'],
                        "image": image_url
                    }))
                    if (r.status_code == requests.codes.ok):
                        print('Successfully replied to %s with image %s' % (tweet['user']['screen_name'], image_url))
                    else:
                        print("Tweetback failed for image %s (%s)" % (image_url, r.text))
                else:
                    print("Colorization failed for -> " + media['media_url_https'])

    def on_error(self, status):
        print('Error from tweet streamer', status)

if __name__ == '__main__':
    print('Setting up')
    l = StdOutListener()
    stream = Stream(auth, l)

    print('Listening for tweets')
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['#colouriseme', '#colorizeme', '#coloriseme'])
