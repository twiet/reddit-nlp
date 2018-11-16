# sports - r/tennis, r/nba
# games - r/PUBATTLEGROUNDS, r/leagueoflegends
# politics - r/PoliticalDiscussion, r/Libertarian
# education - r/Economics, r/science
# tech - r/apple, r/programming

import praw
import json

# Hardcoded categories to match 
supercategories = json.loads('''
{
  "sports": [
    "tennis",
    "nba"
  ],
  "games": [
    "PUBATTLEGROUNDS",
    "leagueoflegends"
  ],
  "politics": [
    "PoliticalDiscussion",
    "Libertarian"
  ],
  "education": [
    "Economics",
    "science"
  ],
  "tech": [
    "apple",
    "programming"
  ]
}
''')
  
def praw_call():
  # reddit api object instance
  # docs https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

  reddit = praw.Reddit(client_id='6Ac8q3UdUrJR2A',
                      client_secret='unN_bfTDr5Gd-BibYqoMs90GxPQ',
                      user_agent='parser.py')

  l = []
  for label, subreddits in supercategories.items():
    for subreddit in subreddits:
      # search and retrieve subreddit object via string
      sub = reddit.subreddit(subreddit)
      # find top post for subreddit
      top_post = list(sub.top(limit=10))
      for post in top_post:
        # get top ten comments for post
        comments = [comment.body for comment in post.comments[:10]]
        # build and append data object
        data = { "data" : { "title": post.title, "comments": comments }, "label": label }
        l.append(data)
  obj = { "corpus": l }
  # dump results formatted to json
  with open('reddit-nlp/samples.json', 'w') as outfile:
    json.dump(obj, outfile, sort_keys=True, indent=4, separators=(',', ': '))

def request():
  print

praw_call()