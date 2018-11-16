# reddit-nlp

Needs praw. run "pip install praw" first

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
    

Data source: https://files.pushshift.io/reddit/
