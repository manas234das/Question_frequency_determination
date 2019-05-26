# Data Pre-Processing for topic_dataset

# Importing Libraries
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Importing the dataset of the topics
topic_dataset = pd.read_csv('./Converted Files/topic_dataset.tsv', 
                            delimiter = '\t', 
                            quoting = 3, 
                            encoding = "ISO-8859-1")

# Removing other unwanted columns
topic_df = topic_dataset.iloc[:, 1:2]

# Making the keyword list
key_word = []

# For the complete keyword list
for i in range(0, len(topic_df)):
    keys = re.sub("[^a-zA-Z]", " ", topic_df['topic'][i])
    keys = keys.lower()
    keys = keys.split()
    
    # Stemming the keywords as well using PoterStemmer
    ps = PorterStemmer()
    keys = [ps.stem(word) for word in keys if not word in set(stopwords.words('english'))]
    
    # Finally joining the splitted words
    keys = ' '.join(keys)
    key_word.append(keys)
    
        
##########################################################################################################

# Data preprocessing for 500_questions dataset

# Importing the dataset of the questions
questions_dataset = pd.read_csv('./Converted Files/500_questions.tsv', 
                            delimiter = '\t', 
                            quoting = 3, 
                            encoding = "ISO-8859-1")

# Removing the 1st column 
questions_df = questions_dataset.iloc[:, 1:2]


# Creating the 'corpus'
corpus = []

# for loop for complete dataset
for i in range(0, 500):
    question = re.sub("[^a-zA-Z]", " ", questions_df['question'][i])
    question = question.lower()
    question = question.split()
    
    # Stemming the dataset as well using PoterStemmer
    ps = PorterStemmer()
    question = [ps.stem(word) for word in question if not word in set(stopwords.words('english'))]
    
    # Finally joining the splitted words
    question = ' '.join(question)
    corpus.append(question)


'''Now we have the keyword list in the "key_word" variable and the "corpus" with all the
filtered questions.'''


##########################################################################################################

"""Now we need to find the word's appearance (key_word) in the questions (corpus) through 
the index of the question"""


# Finding the matching words with matching indexes from the corpus using the key_word list

matching_question_index = []
matching_keyword = []

for i in range(0, len(corpus)):
    split_corp = corpus[i].split()
    for j in range(0, len(split_corp)):
        for k in range(0, len(key_word)):
            if  key_word[k] == split_corp[j]:
                matching_question_index.append(i)
                matching_keyword.append(key_word[k])


"""We can't make the matching_index and the matching_word 'now' b/c we will loose the
indexes of some matching keywords....."""


##########################################################################################################


# Combining the matching question index and the keyword

merge_word_index = set(list(zip(matching_question_index, matching_keyword)))
merge_word_index = list(merge_word_index)
merge_word_index = sorted(merge_word_index, key = lambda x:x[0])
merge_word_index = np.array(merge_word_index)


'''Now we have a merged array of keywords along with their respictive Question indexes'''


# This part is for visualisation of the Key_words and the respective indexes 
'''
combined_word_index = np.array(merge_word_index)
combined_word_index = pd.DataFrame(combined_word_index)
combined_word_index.columns = ['index', 'topic']

# Viewing in a proper order
combined_word_index_count = combined_word_index.groupby('topic').count().reset_index()
combined_word_index = combined_word_index.groupby('topic').agg({'index': ', '.join }).reset_index()
'''

##########################################################################################################

'''Now we have to find the respective questions using the index and search for 
the key_word's appearance'''


# Finding the respective questions as per keywords

list_of_qtn = []
list_of_key = []

for i in range(0, len(merge_word_index)):
    temp = merge_word_index[i][0]
    temp = int(temp)
    for j in range(0, len(questions_df)):
        if questions_df.index[j] == temp:
            list_of_qtn.append(questions_df.iloc[j,0])
            list_of_key.append(str(merge_word_index[i][1]))


##########################################################################################################

"""Now we can merge the key_words found in the respective question of the corpus"""


# Merging the questions with keywords
list_of_qtn_key = list(zip(list_of_key, list_of_qtn))
list_of_qtn_key = np.array(list_of_qtn_key)

# Visualising the questions and key_words (topics) associated with the respective question

"""
# Visualising
qtn_ans = pd.DataFrame(list_of_qtn_key)
qtn_ans.columns = ['topics', 'questions']

qtn_ans_v_count = qtn_ans.groupby('topics').count().reset_index()
qtn_ans_v = qtn_ans.groupby('topics').agg({'questions' : '\t, '.join}).reset_index()
"""


##########################################################################################################

'''Now we have to find the related subjects associated with the topic and assigned 
    questions to it'''

# Finding the respective subjects

import functools
topic_sub = topic_dataset.iloc[:, 2:3].values
topic_sub = topic_sub.tolist()
topic_sub = functools.reduce(lambda x,y : x+y ,topic_sub)

topic_sub_key = list(zip(key_word, topic_sub))
topic_sub_key = np.array(topic_sub_key)


list_of_sub = []

for i in range(0, len(list_of_qtn_key)):
    temp = list_of_qtn_key[i][0]
    temp = str(temp)
    for j in range(0, len(topic_sub_key)):
        if topic_sub_key[j][0] == temp:
            list_of_sub.append(str(topic_sub_key[j][1]))


##########################################################################################################

"""Now after we have the question list with the topics associated, We will now create the
    final list which will have the list of All the questions associalted with the topics
    and the subjects respectively"""

# Merging the subjects

# First Converting the subject list into an array
list_of_sub = np.array(list_of_sub)
list_od_sub = list_of_sub[:, np.newaxis]

# Merging the lists into a final list
Final_list = np.column_stack((list_of_sub, list_of_qtn_key))

# Visualising
qtn_topic_sub = pd.DataFrame(Final_list)
qtn_topic_sub.columns = ['subjects','topics', 'questions']

final_qtn_topic_sub = qtn_topic_sub.groupby('subjects').agg({'topics' : ', '.join, 
                                                             'questions' : '\t, '.join}).reset_index()


##########################################################################################################

'''Now we will have to separate the top 10 most frequently asked questions from 
the final dataframe which contains all the questions with the topics and subjects.'''

# Creating the list of top 10 most frequently asked questions

qtn_ans = pd.DataFrame(list_of_qtn_key)
qtn_ans.columns = ['topics', 'questions']
qtn_ans_v_count = qtn_ans.groupby('questions').count().reset_index()


frequent_qtn = []

for i in range(0, len(qtn_ans_v_count)):
    temp = qtn_ans_v_count.iloc[i][1]
    temp = int(temp)
    if temp > 2:
        if temp > 3 or len(frequent_qtn) < 10:
            frequent_qtn.append(str(qtn_ans_v_count.iloc[i][0]))


# Now finding the keys associated to those 10 questions

frequent_topic = []
frequent_sub = []

for i in range(0, len(qtn_topic_sub)):
    temp = qtn_topic_sub.iloc[i][2]
    temp = set(str(temp).split(' '))
    for j in range(0, len(frequent_qtn)):
        temp2 = set(str(frequent_qtn[j]).split())
        if temp == temp2:
            frequent_topic.append(qtn_topic_sub.iloc[i][1])
            frequent_sub.append(qtn_topic_sub.iloc[i][0])


# Making the complete matrix
top_10 = list(zip(frequent_sub, frequent_topic, frequent_qtn))
top_10 = np.array(top_10)

top_10_set = pd.DataFrame(top_10)
top_10_set.columns = ['Subjects', 'Topics', 'Questions']

# Moving the dataframe to the csv file
top_10_set.to_csv('solution.csv', sep=',', index=False, encoding = "ISO-8859-1")


# To visualise further as a collection grouping can be done
top_10_set = top_10_set.groupby('Subjects').agg({'Topics':' | '.join,
                                                 'Questions':' |  '.join}).reset_index()


'''Note : Check the directory for the solution.csv file. It contains the top 10 questions
            with their respective subjects and topics'''

    