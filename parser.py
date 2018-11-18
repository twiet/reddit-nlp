import json
import time
import os.path
import csv

# subreddits we're interested in
SUBREDDITS = ["tennis", "nba", "apple", "programming", "Economics", "politics", "Music", "news", "movies"]
SUBREDDIT_FILE = 'data/subreddits_basic.csv'
TMP_SUBMISSIONS_FILE = "tmp_submission_dict"
TMP_COMMENTS_FILE = "tmp_comment_dict"
MAX_COMMENTS = 5
SAMPLE_SIZE = 20

# decoder for converting json to python object
def object_decoder(obj):
  if 'body' in obj and 'parent_id' in obj:
      return comment(obj['id'], obj['body'], obj['parent_id'])
  if 'title' in obj and 'subreddit' in obj:
      return submission(obj['title'], obj['subreddit'], [])
  return obj

class submission(dict):
  def __init__(self, title, subreddit, comments):
    self.title = title
    self.subreddit = subreddit
    self.comments = comments
    dict.__init__(self, title = title, subreddit = subreddit, comments = comments)

class comment(dict):
  def __init__(self, id, body, parent_id, parent = None):
    self.id = id
    self.body = body
    self.parent_id = parent_id
    self.parent = parent
    dict.__init__(self, id = id, body = body, parent_id = parent_id, parent = parent)
    
  def get_submission(self):
    if self.__isTopLevel(self.parent_id):
      return self.parent_id[3:]
    elif not self.parent is None:
      return self.parent.get_submission()

  def __isTopLevel(self, parent_id):
    return parent_id.startswith('t3_')

  def set_parents(self, comment_dict):
    if not self.__isTopLevel(self.parent_id):
      parent_id = self.parent_id[3:]
      if parent_id in comment_dict.keys():
        self.parent = comment_dict[parent_id]

def timeit(method):
  def timed(*args, **kw):
    ts = time.time()
    result = method(*args, **kw)
    te = time.time()
    if 'log_time' in kw:
        name = kw.get('log_name', method.__name__.upper())
        kw['log_time'][name] = int((te - ts) * 1000)
    else:
        print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
    return result
  return timed

@timeit
def load_subreddits(file_name):
  subreddits_dict = {}
  if not (os.path.isfile(TMP_SUBMISSIONS_FILE) and os.path.isfile(TMP_COMMENTS_FILE)):
    read_subreddits(file_name, SUBREDDITS, subreddits_dict)
  return subreddits_dict

# TODO: detect bad or obsolete cache instead of path check
@timeit
def load_submissions(file_name, subreddits_dict):
  submission_dict = {}
  if not os.path.isfile(file_name):
    read_submissions(submission_dict, subreddits_dict)
    with open(file_name, 'w') as outfile:
      json.dump(submission_dict, outfile)
  else:
    with open(file_name, 'r') as infile:
      submission_dict = json.load(infile, object_hook=object_decoder)
  return submission_dict

# TODO: detect bad or obsolete cache instead of path check
@timeit
def load_comments(file_name, subreddits_dict):
  comment_dict = {}
  if not os.path.isfile(file_name):
    read_comments(comment_dict, subreddits_dict)
    with open(file_name, 'w') as outfile:
      json.dump(comment_dict, outfile)
  else:
    with open(file_name, 'r') as infile:
      comment_dict = json.load(infile, object_hook=object_decoder)
  return comment_dict

@timeit
def read_subreddits(file_name, subreddits, subreddits_dict):
  with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
      if len(row) > 4:
        id = row[1]
        name = row[3]
        if name in subreddits:
          subreddits_dict[id] = name

#TODO: remove hardcoded filenames
@timeit
def read_submissions(submission_dict, subreddits_dict):
  for i in range(1, 13):
    filename = 'data/RS_v2_2008-' + str(i).zfill(2)
    with open(filename, 'r') as infile:
      for line in infile:
        obj = json.loads(line)
        if obj['subreddit_id'] in subreddits_dict.keys():
          submission_dict[obj['id']] = submission(obj['title'], obj['subreddit'], [])

#TODO: remove hardcoded filenames
@timeit
def read_comments(comment_dict, subreddits_dict):
  for i in range(1, 13):
    filename = 'data/RC_2008-' + str(i).zfill(2)
    with open(filename, 'r') as infile:
      for line in infile:
        obj = json.loads(line)
        if obj['subreddit_id'] in subreddits_dict.keys():
          comment_dict[obj['id']] = comment(obj['id'], obj['body'], obj['parent_id'])

# TODO: need to figure out how to cache the comment chain to improve performance
@timeit
def set_parents(comment_dict):
  for k,v in comment_dict.items():
    v.set_parents(comment_dict)
    
@timeit
def set_comments(comment_dict, submission_dict):
  for k,v in comment_dict.items():
    sub = v.get_submission()
    if sub in submission_dict.keys():
      submission_dict[sub].comments.append(v)

@timeit
def dump_json(file_name, keys, d):
  with open(file_name, 'w') as outfile:
    for key in keys:
      sub = d[key]
      data = { "data" : { "title": sub.title, "comments": sub.comments[:MAX_COMMENTS] }, "label": sub.subreddit }
      json.dump(data, outfile)
      outfile.write('\n')

@timeit
def output_results(file_name, submission_dict):
  keys = list(submission_dict.keys())
  # split dump into a sample for easier debugging
  size = min(SAMPLE_SIZE, len(keys))
  sample = keys[:size]
  rest = keys[size:]
  sample_name = "sample_" + file_name
  dump_json(sample_name, sample, submission_dict)
  dump_json(file_name, rest, submission_dict)

@timeit
def main():
  subreddits_dict = load_subreddits(SUBREDDIT_FILE)
  submission_dict = load_submissions(TMP_SUBMISSIONS_FILE, subreddits_dict)
  comment_dict = load_comments(TMP_COMMENTS_FILE, subreddits_dict)

  set_parents(comment_dict)
  set_comments(comment_dict, submission_dict)

  output_results("data.txt", submission_dict)

main()