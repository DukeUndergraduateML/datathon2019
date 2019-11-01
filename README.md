# Datathon 2019, Sponsored by the Duke Undergraduate Machine Learning Program 

# Valassis

Valassis is the leader in marketing technology and consumer engagement. They work with over 60,000 companies and brands in a wide array of industries, partnering to anticipate consumer intent, inspire action, and create demand, while saving consumers money. They own and use predictive intelligence to anticipate purchase intent, deliver value, optimize campaigns, and drive results by inspiring consumers to act.  Every day, Valassis converts billions of signals into meaningful engagement across all channels to drive exponential growth.  

Valassis examines content across 80 billion web pages each day and derives meaning from words and sentences to determine likely purchase intent.  Their page-level analysis enables a deep understanding of the shopper’s browsing behavior across 1400 interest topics.   For example, they know the difference between someone interested in running shoes, running for office or running a small business.  They can differentiate between recent in-market shopping patterns and long-term interests over time.  The in-depth understanding of the shoppers’ online activity is only part of their story. To get a holistic view, marketers must connect the shoppers’ online activity to their real-world actions. The Valassis Consumer Graph does this by synthesizing accurate, real-world data across 540K stores, 900K points of interest, and 110MM households together with browsing and buying data.


# 2019 Challenge Dataset

## Background 

In digital advertising, a “conversion” refers to the event when the shopper clicks on an ad and performs a valuable action such as signup, registration, or make a purchase.  Since a "conversion" is a measurable event, it represents a reasonable proxy for the number of customers acquired during the ad campaign.  Increasingly, brands and agencies are looking to put a value on the Return on Advertising Spend (ROAS), which requires marketers such as Valassis to optimize the ad spend such that customer acquisition is maximized.

In order to wisely spend the limited marketing dollars, we need to identify the shoppers who are more likely to respond to our ad and convert.  While the number of devices to target is nearly one billion, the number of conversion events range from just a few hundreds to few thousands during the period of the ad campaign.  In other words, these conversion events are extremely rare.   
 

## The Challenge 

**The primary objective is to predict the shoppers who are likely to convert with very little false alarm.** An added impediment is that the information we know about the shopper is incomplete which means the data is sparse.

## The Ask

The dataset is already divided into two groups (refer to Table 1) for your convenience, training and validation.

1. Use the training data to build a model to predict shoppers who are likely to convert.  
2. Then, use the validation data to evaluate the performance of your model.  
3. Feel free to use any appropriate metric to evaluate the models on the training and validation sets. (You will need to decide on appropriate metrics on your own). 

For various reasons, marketers will have to understand the profile of the shoppers who converted.  
4. What is your take on the profile of the converters?  
5. What other insights can you gain from the data and the model you have built?

## Data Description 

There are two zip files that hold the same data, albeit, in a different format.  
- valassis_dataset.zip: Preferable for Python programmers.
- valassis_tallskinny_dataset.zip: Preferable for R programmers.

### Dataset Version 1: valassis_dataset.zip (preferable for Python users)
You should see three main data files:

1. **training.csv**: Contains the training data, which is needed for training the model
   - Total number of data points: 96,406
   - Positive data points: 1,465
   - Negative data points: 94,941
   
2. **validation.csv**: Contains the samples for validating the model
   - Total number of data points: 80,008
   - Positive data points: 620
   - Negative data points: 79,388
   
3. **interest_topics.csv**: Contains the topic labels and topic descriptions
   - 1,411 total interest topics in the file
   
#### *Column descriptions*

##### Interest Topics Dataset
- Each row is one of the interest topics
- *topic_id* (integer): Numerical identifier of the topic
- *topic_name* (string): Interest topic name

##### Training and Validation Datasets
- Each row represents a shopper's long term and short-term interests, across the 1,411 total categories
- *userID* (integer): User identifier.  Unique for each row in this csv file.
- *inAudience* (boolean): Whether or not the shopper has converted in the past
   - TRUE: shopper has converted
   - FALSE: shopper has not converted

- *ltiFeatures* (dictionary, key: string, value: double): Long term interests
   - The dictionary's keys are the interest topics. The value represents the proportional interest the user has in that topic.
   - For example, if the *ltiFeatures* of one of the users is {'34': 0.7, '41': 0.3}, that means that the user has 70% interest in Topic 34, which is */Arts & Entertainment/Movies*, and 30% interest in Topic 41, which is */Games/Computer & Video Games*.
- *stiFeatures* (dictionary, key: string, value: double): Short term interests
   - Format is the same as *ltiFeatures*, except this now refers to short-term interests rather than long-term interests

### Dataset Version 2: valassis_tallskinny_dataset.zip (preferable for R users)

You should see three main data files:

1. **training_tallskinny.csv**: Contains the training data, which is needed for training the model
   - Total number of data points: 96,406
   - Positive data points: 1,465
   - Negative data points: 94,941
   
2. **validation_tallskinny.csv**: Contains the samples for validating the model
   - Total number of data points: 80,008
   - Positive data points: 620
   - Negative data points: 79,388
   
3. **interest_topics.csv**: Contains the topic labels and topic descriptions
   - 1,411 total interest topics in the file

##### Interest Topics Dataset
- Each row is one of the interest topics
- *topic_id* (integer): Numerical identifier of the topic
- *topic_name* (string): Interest topic name

##### Training and Validation Datasets
- Each row represents a shopper's long term and short-term interests in one of the 1,411 total categories
- *userID* (integer): User identifier.  Unique for each row in this csv file.
- *inAudience* (boolean): Whether or not the shopper has converted in the past
   - TRUE: shopper has converted
   - FALSE: shopper has not converted 
- *topic_id* (integer): Integer representing the topic ID
- *ltiFeatures* (double): Level of long-term interest in the topic represented by the topic_id column
- *stiFeatures* (double): Level of short-term interest in the topic represented by the topic_id column

# Code snippets for getting started

### Python

```python
def load(file):
   import pandas as pd
   import ast
   df = pd.read_csv(file)
   
   # convert the column values from literal string to dictionary
   df['ltiFeatures'] = df['ltiFeatures'].apply(ast.literal_eval)
   df['stiFeatures'] = df['stiFeatures'].apply(ast.literal_eval)
   
   return df

# load all the data
training = load("training.csv")
validation = load("validation.csv")
interest_topics = pd.read_csv("interest_topics.csv")

# inspect the data
interest_topics.head()
training.head()
validation.head()
```

### R

```r
library(readr)

training = read_csv("training_tallskinny.csv")
validation = read_csv("validation_tallskinny.csv")
interest_topics = read_csv("interest_topics.csv")
```

# The Final Product

You will work in teams of up to four members. You must submit your submission (and only one submission per group) to https://cmt3.research.microsoft.com/User/Login?ReturnUrl=%2FDATATHON2019 by the deadline. Multiple submissions will be disqualified. 

1. Please submit early and often. 
2. Please assign one person in your group to be in charge of your submissions. Please make sure to keep track of your submission number in CMT. 
3. You must submit a report consisting of an abstract, data description, methodology, analysis section, and discussion. 
4. Your report may not be longer than 4 pages in length. You may have an optional appendix (maximum 2 pages), however, this may not be read by the reviewers. 
5. You must submit your code (in a .zip file) and it must be runnable in order to be considered for a submission. 

# Rubric 

Your work will be judged based on the following criteria:
- Task & Goals
   - The report must state the question that the team is trying to answer and explain why this question is relevant/important
- Evidence & Methods
   - The report and findings must be supported by the data through properly conducted analysis and carry objectively correct interpretations of evidence.
- Visual Materials
   - The report should contain meaningful visualizations that supplement the findings described.
- Organization
   - The report should be organized in a logical progression for the audience to follow. Additionally it will be important to use terminology and phrasing that are clearly understandable. 

# Tips / Suggestions

Please see [this document](https://github.com/DukeUndergraduateML/datathon/blob/master/datathon/datathon-2019/hints/2019-datathon-guide.pdf) for a few tips/suggestions!
