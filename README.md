﻿# project-code
 Approach to build system:
 
1. Reading file and generation of transition matrix:
I first converted the .txt file to the .csv, as the .txt did not have tab for tags in the new line. I then created two different arrays for words and tags. The array of tags will now have duplicate tags present. So I used set() function to find unique from the tag array.

A transition matrix of size unique_tag*unique_tag is created. Where probability of every tag given each tag is calculated and stored.

2. Calculating observation matrix:
Observation matrix, is of size unique_ tags*word. In order to calculate it probability P(word|tag) is found out for every word and every tag. Now there is a chance that observation of certain word given a tag can be zero for example : P(race|PRP). Therefore in order to avoid the MLE of entire sentence to be zero, Laplace smoothing or add-1 smoothing is applied on the observation matrix where the word count is added by 1 and the divided by (N+V) where V is the word in vocabulary and n is the N is the normalizing count. Thus now we have our observation_matrix for the observed sequences of words.

3. Implementing Viterbi Algorithm on development set: 
The format of the file give did not had a start tag at the start of the sentence, so we cannot use the same approach in initialization step as mentioned in text. Instead I took the probability of the start word in the word array derived from the file. Also from the array of unique_tags ,I found out transition probability of the tag 'space'. Multiplying it with the observation probability of the first word, gives initial path probability. In the same step back trace is applied to store the tag.

Recursive step: 
path probability of the previous word is multiplied with transition probability of the tag given tag from the pervious word . This is then multiplied with the observation probability of the word. Maximum of them is taken and that is feeded in the current path probability matrix. This loop continues to run till the length of observations. Back trace is done at each step to store tags.

4. Implementing recursive step for Viterbi on test set:
In order that my algorithm works for new words, I am checking if the word set from test set matches with the word set from development set. If it matches i.e. word from test set is also present in the development set then i will continue finding tag sequences as mentioned before. If not I will assign the observation probability of that word to be one. Back trace is done at every step to store the tag associated with that word.

How to run program:

The following command will run the algorithm

$ python "filename" berp-POS-train.txt berp-POS-test.txt

The result is stored in result.txt file. this file is then compared with berp-POS-test.txt to get the accuracy percentage. In order to do so, berp-POS-test.txt is formatted using format_gold.py file. the command to run the file is

$ python format_gold.py berp-POS-test.txt

The resulting file form_berp-POS-test.txt is then used for evalPOS.py. The command for it is

$ python evalPOS.py form_berp-POS-test.txt result.txt

