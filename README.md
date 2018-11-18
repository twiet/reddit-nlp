# reddit-nlp

To run 
1. download the data from https://files.pushshift.io/reddit/submissions/ and https://files.pushshift.io/reddit/comments/
2. You will need all the 2008 files. There should be 12 for comments and 12 for submissions.
3. Also you need the subreddit csv here https://files.pushshift.io/reddit/subreddits/
4. Running will take about an hour and should generate a data.txt file. I've added a sample.txt and a trimmed data.txt taken from that as an example.

Feel free to add comments on any inefficiencies since I didn't focus too much on performance. Also feel free to adjust any of the parameters as well

To-do
1. Count word count per input [TODO: Kevin]
2. Store json object per interval to not lose data [TODO: Kevin]
3. Provide code for reading json object. Labels and input in list. [TODO: Kevin]
4. Clean data (separate *) [TODO: Mingwei]
  - tokeninze
  - strip new lines
5. Investigate scaling the data retrieval 
  - Current implementation using praw api is throttled by one request per sec and not scalable
    - pros: api code is clean and get associated values fast
    - cons: throttled via requests thus is not scalable by machine
  - Downloading data from pushshift.io and manually categorizing an associating them is not performant due to having to loop through gigabytes of data. 
    - pros: easier to scale
    - cons: need to handle more cases including bad and/or missing data
    
Cleaning
  - some posts and comments just say [deleted] which means the original post was removed. We should not include those
  - submissions with no comments or comments less than some threshold should also be removed
  - for comments we can focus on the higher rated ones more

To run clean.py
  - python clean.py sample_data.txt
  - this generates two separate files labels.txt and contents.txt
  
  
  
Data source: https://files.pushshift.io/reddit/
