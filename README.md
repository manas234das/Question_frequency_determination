# Question frequency Determination
### Problem Statement : 
* Given two different Datasets ( 500_questions.csv and subject_topic.csv ) find at least 10 frequently asked questions for each of the subject mentioned in the Dataset.
* Subjects and topics are mentioned in the dataset : [Subject_Topic Dataset](http://bit.ly/epo_FAQ_sample_topics)
* Questions are mentioned in the dataset : [500_questions](http://bit.ly/epo_FAQ_superset_Sample).
* The second dataset contains list of 500 questions that was asked in the interview.

### Output format (column names) :

    | Subject name | Topic name | Question |


## Author and contributors
- Manas Das <manas234das@gmail.com>

## Python Libraries used
    numpy
    pandas
    re
    nltk

## How to run the program
- After cloning to the local machine simply run the **frequency_finder.py** file or the **frequency_finder.ipynb**
- A solution.csv file will be generated which contains all the questions with respect to its subject and the frequency of it's appearance.