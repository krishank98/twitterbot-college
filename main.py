
//comment

API_KEY = "YGV37Oyu2myhWQhtiOqQ7TW1I"
API_SECRET = "Wt9Nx5UfWz3qgUxhoejoajDvkxNaHH8fe7ipT2GBzywLA1lBPM"
ACCESS_TOKEN = "995165324554072064-9HUFpUF7d0A7JFE0WqG0wqYMBmjvVLC"
ACCESS_TOKEN_SECRET = "kkNwvKACEQ6Zgjwrrvv0g56VjFL60bfz9vsaL84JA4Zfk"

paralleldots_api_key='CkstN34JUDrM6JDxXb0B5HuUqSyPSZ1g8SZ91l5DSZQ'


import tweepy, re, operator

import nltk
from nltk.corpus import stopwords

from paralleldots import set_api_key, sentiment

oauth = tweepy.OAuthHandler(API_KEY, API_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(oauth)


def get_tweets():
    user_input = raw_input("Enter the query without Hashtag: ")

    hash_tag = "#" + user_input
    print(hash_tag)
    tweets = api.search(q=hash_tag, count=200)
    return tweets


def test_sentiments():
    list_of_sents = []
    tweets = get_tweets()
    set_api_key(paralleldots_api_key)
    for tweet in tweets:
        list_of_sents.append(sentiment(tweet.text))
    return list_of_sents


def location():
    lang = {}
    loc = {}
    time = {}
    search = raw_input("Enter the query without the hashtag: ")
    hash_tag = "#" + search
    print(hash_tag)
    tweets = api.search(q=hash_tag, count=200)
    for tweet in tweets:
        if tweet.user.lang in lang.keys():
            lang[tweet.user.lang] += 1
        else:
            lang[tweet.user.lang] = 1

        if tweet.user.location in loc.keys():
            loc[tweet.user.location] += 1
        elif tweet.user.location != '':
            loc[tweet.user.location] = 1

        if tweet.user.time_zone in time.keys():
            time[str(tweet.user.time_zone)] += 1
        else:
            time[str(tweet.user.time_zone)] = 1

    top_location = sorted(loc, key=loc.get, reverse=True)
    top_timezones = sorted(time, key=time.get, reverse=True)
    top_lang = sorted(lang, key=lang.get, reverse=True)

    print("Top 5 Locations for this hashtag are:")
    i = 0
    for k in top_location[0:5]:
        i += 1
        print(i, k, loc[k])

    print("Top 5 timezones for this hashtag are:")
    i = 0
    for k in top_timezones[0:5]:
        i += 1
        print(i, k, time[k])
    i = 0
    print("Top 5 languages used:")
    for k in top_lang[0:5]:
        i += 1
        print(i, k, lang[k])

def tweet_match():
    trump = 0
    tweets = api.user_timeline(screen_name="@realdonaldtrump", count=200, tweet_mode="extended")
    for tweet in tweets:
        tweet_text = re.sub(r"http\S+", "", tweet.full_text)   # Removing the URL texts
        if "India" in tweet_text or "INDIA" in tweet_text or "Bharat" in tweet_text or "Hindustan" in tweet_text or "india" in tweet_text:
            trump += 1

    modi = 0
    tweets = api.user_timeline(screen_name="@narendramodi", count=200, tweet_mode="extended")
    for tweet in tweets:
        tweet_text = re.sub(r"http\S+", "", tweet.full_text)   # Removing the URL texts
        if "US" in tweet_text or "USA" in tweet_text or "America" in tweet_text or "United States Of America" in tweet_text or "america" in tweet_text:
            modi += 1

    # showing the comparison
    print("Modi-" + str(modi))
    print("Trump-" + str(trump))

def top_usage():

    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    dict = {}
    tweet_words = []
    tweet = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for x in tweet:
        y = x.full_text.split(" ")
        for z in y:
            tweet_words.append(z)
    for word in tweet_words:
        if word not in stop_words and "http" not in word:
            if word in dict.keys():
                dict[word] += 1
            else:
                dict[word] = 1

    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
    print("The Top Ten Words Are: ")
    for i in range(-1, -11, -1):
        print(sorted_dict[i][0], " - ", sorted_dict[i][1])




def main():
    show_menu=True
    while (show_menu):
        user_choice = input("1.Get the tweets for a certain hashtag\n"
                            "2.Count the followers of People Tweeting using a certain hash Tag\n"
                            "3.Determine the Location,Timezone and Language of people tweeting using a certain hashtag.\n"
                            "4.Determine number of times Narendra Modi has referred to US in post 200 Tweets compared to how may times Trump has mentioned India.\n"
                            "5.Determine the sentiment of People Tweeting using a certain hashtag.\n"
                            "6.Top used words by PM Modi on Twitter.\n"
                            "7.Tweet a message from your account.\n"
                            "8.Exit\n")
        if user_choice == 1:

            tweets = get_tweets()  # getting the tweets from the other function
            print("Following tweets have been made by the people \n")
            for tweet in tweets:
                print(tweet.text)

        if user_choice == 2:

            tweets=get_tweets()
            for tweet in tweets:
                print("User : %s \t Followers:%s " % (tweet.user.name, tweet.user.followers_count))
            print("\n")





        elif user_choice==3:
            location()


        elif user_choice==4:
            tweet_match()

        elif user_choice == 5:

            list_sents = test_sentiments()
            p = 0
            n = 0
            nu = 0
            for x in list_sents:
                if x["sentiment"] == "neutral":
                    nu += 1
                elif x["sentiment"] == "negative":
                    n += 1
                elif x["sentiment"] == "positive":
                    p += 1
            print("Sentiment Result:\nWait for a minute(max 2 min xD)")
            print("Positive:%d \t Negative:%d \t Neutral:%d" % (p, n, nu))


        elif user_choice==6:
            top_usage()

        elif user_choice==7:
            status = raw_input("Enter The Status update:")
            api.update_status(status)

        elif user_choice==8:
            show_menu=False
        else:
            print 'Please enter wrong answer.Please try again'


main()
