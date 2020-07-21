 # CS121: Analyzing Election Tweets

# Omar Elmasry and Mufitcan Atalay 

# Interface the algorithms in the previous part to the dataset
# of tweets. Every tweet is represented as a JSON file. Functions to implement:
# find_top_k_entities, find_min_count_entities, find_frequent_entities,
# find_top_k_ngrams, find_min_count_ngrams, find_frequent_ngrams
# find_top_k_ngrams_by_month

# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg=missing-docstring, wildcard-import, invalid-name
# pylint: disable-msg=redefined-outer-name, broad-except, unused-import
# pylint: disable-msg=unused-wildcard-import


import argparse
import json
import string

from clean import *
from util import get_json_from_file, grab_year_month, pretty_print_by_month
from basic_algorithms import find_top_k, find_min_count, find_frequent

# Tweets are represented as dictionaries that has the same keys and
# values as the JSON returned by Twitter's search interface.

# ####################  MODIFY THIS CODE #####################


# PUT YOUR AUXILIARY FUNCTIONS HERE


# Task 1
def find_top_k_entities(tweets, entity_key, k):
    '''
    Find the K most frequently occurring entities.

    Inputs:
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"),
          ("user_mentions", "screen_name"), etc.
        k: integer

    Returns: list of entity, count pairs

    '''

    """
    Your code goes here
    """
    word = []
    ktop = []
    for x in tweets:
        entities = x['entities']
        tagtag = entities[entity_key[0]] 
        for y in tagtag:
            word.append(str.lower(y[entity_key[1]]))
    ktop = find_top_k(word, k)
    return ktop

# Task 2
def find_min_count_entities(tweets, entity_key, min_count):
    '''
    Find the entities that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"),
          ("user_mentions", "screen_name"), etc
        min_count: integer

    Returns: list of entity, count pairs
    '''

    """
    Your code goes here
    """
    word1 = []
    minny = []
    for x in tweets:
        entities = x['entities']
        tagtag = entities[entity_key[0]] 
        for y in tagtag:
            word1.append(str.lower(y[entity_key[1]]))
    minny = find_min_count(word1, min_count)
    return minny

# Task 3
def find_frequent_entities(tweets, entity_key, k):
    '''
    Find entities where the number of times the specific entity occurs
    is at least 1/k * the number of entities in across the tweets.

    Input:
        tweets: list of tweets
        entity_key: a pair ("hashtags", "text"),
          ("user_mentions", "screen_name"), etc.
        k: integer

    Returns: list of entity, count pairs
    '''

    """
    Your code goes here
    """

    word2 = []
    freqy = []
    for x in tweets:
        entities = x['entities']
        tagtag = entities[entity_key[0]] 
        for y in tagtag:
            word2.append(str.lower(y[entity_key[1]]))
    freqy = find_frequent(word2, k)
    return freqy


#Helper Functions'
    '''
    converts tweets to lowercase. demarcates based on spaces and cleans
    the tweets of punctuation, stopprefexies and stopwords.

    input:
        tweet: a tweet
    output:
        a clean list of strings.
    '''
def make_nice(tweet):
    lowtweet = tweet['text'].lower()
    splittweet = lowtweet.split()   
    cleansed =[]
    for word in splittweet:
        word = word.strip(PUNCTUATION)
        if not word.startswith(STOP_PREFIXES) and word not in STOP_WORDS and word !="":
            cleansed.append(word)
    return cleansed     



def make_ngram(tweet, n):
    '''
    makes an ngram out of a clean list of strings

    input:
        tweet: a tweet
        n: an integer
    output:
        output: a list of ngrams  
    '''


    output = []
    cleansed = make_nice(tweet)
    speed = len(cleansed)
    for tweet in range(speed-n+1):
        output.append(tuple(cleansed[tweet:tweet+n]))
    return output

# Task 4
def find_top_k_ngrams(tweets, n, k):
    '''
    Find k most frequently occurring n-grams.

    Inputs:
        tweets: a list of tweets
        n: integer
        k: integer

    Returns: list of key/value pairs
    '''

    """
    Your code goes here
    """
    topk_grams = []
    output = []
    for tweet in tweets:
        output += make_ngram(tweet, n)
    topk_grams = find_top_k(output, k)
    return topk_grams


# Task 5
def find_min_count_ngrams(tweets, n, min_count):
    '''
    Find n-grams that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        n: integer
        min_count: integer

    Returns: list of ngram/value pairs
    '''

    """
    Your code goes here
    """
    minc_ngrams = []
    output1 = []
    for tweet in tweets:
        output1 += make_ngram(tweet, n)
    minc_ngrams = find_min_count(output1, min_count)
    return minc_ngrams


# Task 6
def find_frequent_ngrams(tweets, n, k):
    '''
    Find the most frequently-occurring n-grams.

    Inputs:
        tweets: a list of tweets
        n: integer
        k: integer

    Returns: list of ngram/value pairs
    '''
    """
    Your code goes here
    """
    freq_ngrams = []
    output2 = []
    for tweet in tweets:
        output2 += make_ngram(tweet, n)
    freq_ngrams = find_frequent(output2, k)
    return freq_ngrams 

'''
#Helper for 7:
    
    Creates a dictionary of tweets that has the year-month element
    and the list of tweets 

    input:
        tweets: list of tweets
    output:
        monthly tweets: a dictionary of tweets and dates

'''

def create_tweet_dic(tweets):
    monthly_tweets = {}
    for tweet in tweets:
        grabbed = grab_year_month(tweet["created_at"])
        if grabbed in monthly_tweets:
            monthly_tweets[grabbed].append(tweet)
        else:
            l_grabbed =[]
            l_grabbed.append(tweet)
            monthly_tweets[grabbed] = l_grabbed
    return monthly_tweets 


# Task 7
def find_top_k_ngrams_by_month(tweets, n, k):
    '''
    Find common n-grams used by two Twitter users.

    Inputs:
        tweets: list of tweet dictionaries
        n: integer
        k: integer

    Returns: list of pairs w/ month and the top-k n-grams for that month
    '''

    """
    Your code goes here
    """

    monthly_tweets = create_tweet_dic(tweets)
    months = []
    monthly_ngrams = []

    for key in monthly_tweets:
        monthly_ngrams.append((key,find_top_k_ngrams(monthly_tweets[key], n, k)))

    monthly_ngrams.sort()

    return monthly_ngrams

    pretty_print_by_month(monthly_ngrams)

"""
DO NOT MODIFY PAST THIS POINT
"""


def parse_args(args):
    '''
    Parse the arguments.

    Inputs:
        args: list of strings

    Result: parsed argument object.

    '''
    s = 'Analyze presidential candidate tweets.'
    parser = argparse.ArgumentParser(description=s)
    parser.add_argument('-t', '--task', nargs=1,
                        help="<task number>",
                        type=int, default=[0])
    parser.add_argument('-k', '--k', nargs=1,
                        help="value for k",
                        type=int, default=[1])
    parser.add_argument('-c', '--min_count', nargs=1,
                        help="min count value",
                        type=int, default=[1])
    parser.add_argument('-n', '--n', nargs=1,
                        help="number of words in an n-gram",
                        type=int, default=[1])
    parser.add_argument('-e', '--entity_key', nargs=1,
                        help="entity key for task 1",
                        type=str, default=["hashtags"])
    parser.add_argument('file', nargs=1,
                        help='name of JSON file with tweets')

    try:
        return parser.parse_args(args[1:])
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def go(args):
    '''
    Call the right function(s) for the task(s) and print the result(s).

    Inputs:
        args: list of strings
    '''

    task = args.task[0]
    if task <= 0 or task > 7:
        print("The task number needs to be a value between 1 and 7 inclusive.",
              file=sys.stderr)
        sys.exit(1)

    if task in [1, 2, 3]:
        ek2vk = {"hashtags":"text", 
                 "urls":"url", 
                 "user_mentions":"screen_name"}
        entity_type = (args.entity_key[0], ek2vk.get(args.entity_key[0], ""))

    tweets = get_json_from_file(args.file[0])

    if task == 1:
        print(find_top_k_entities(tweets, entity_type, args.k[0]))
    elif task == 2:
        print(find_min_count_entities(tweets, entity_type, args.min_count[0]))
    elif task == 3:
        print(find_frequent_entities(tweets, entity_type, args.k[0]))
    elif task == 4:
        print(find_top_k_ngrams(tweets, args.n[0], args.k[0]))
    elif task == 5:
        print(find_min_count_ngrams(tweets, args.n[0], args.min_count[0]))
    elif task == 6:
        print(find_frequent_ngrams(tweets, args.n[0], args.k[0]))
    else:
        result = find_top_k_ngrams_by_month(tweets, args.n[0], args.k[0])
        pretty_print_by_month(result)
        

if __name__=="__main__":
    args = parse_args(sys.argv)
    go(args)
