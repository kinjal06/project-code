# Kinjal Thaker
# CSCI 5832
# Assignment 2: HMM POS tagging
# This code was modified based on assignment 3 as my previous code didnt run and also it was taking long time to run

import math;
import os;
import sys;

if len(sys.argv)!=3:
	print 'Usage: python POS_HMM.py trainingData_filename testData_filename'
	sys.exit(1)
# Reading training and test data
training = []
test = []
training_data = open(sys.argv[1], 'r').read().splitlines()
test_data = open(sys.argv[2], 'r').read().splitlines()

for line in training_data:
	if line:
		data1 = line.split()
		training.append(data1)
for line in test_data:
	if line:
		data1 = line.split()
		test.append(data1)

word_count = {}
tag_count = {}
bigram_count = {}
word_tag_count = {}

print 'Training on', sys.argv[1]
# Follwoing code Counts number of occurrences of each word (dealing with unknown words)
for i in range(len(training)):
	if training[i][0] not in word_count:
		word_count[training[i][0]] = 1
	else:
		word_count[training[i][0]] += 1

for i in range(len(training)):

	# Replacing words that occur once with U
	if word_count[training[i][0]] == 1:
		training[i][0] = 'U'

	# Get tag bigram counts C(t_i-1, t_i)
	if(i != 0):
		if (training[i - 1][1], training[i][1]) not in bigram_count:
			bigram_count[training[i - 1][1], training[i][1]] = 1
		else:
			bigram_count[training[i - 1][1], training[i][1]] += 1

	# Get tag counts C(t_i)
	if training[i][1] not in tag_count:
		tag_count[training[i][1]] = 1
	else:
		tag_count[training[i][1]] += 1

	# Get word/tag pair counts C(t_i, w_i)
	if (training[i][0], training[i][1]) not in word_tag_count:
		word_tag_count[training[i][0], training[i][1]] = 1
	else:
		word_tag_count[training[i][0], training[i][1]] += 1

# Remove words that occur only once from word_count
word_count = dict((i,j) for i, j in word_count.iteritems() if j>1)

# Compute the prior P(t_i|t_i-1) = C(t_i-1, t_i) / C(t_i-1) 
# First compute for the bigrams we have encountered
trans_mat = {}
for line in bigram_count:
	if line not in trans_mat:
		trans_mat[line] = float(float(bigram_count[line])/float(tag_count[line[0]]))
# Now account for unseen bigrams by going through all permutations of tags (approach could be more elegant)
for tag_i in tag_count:
	for tag_j in tag_count:
		if (tag_i, tag_j) not in trans_mat:
			trans_mat[tag_i, tag_j] = .000000001
# Compute the likelihood
emis_mat = {}
for line in word_tag_count:
	if line not in emis_mat:
		emis_mat[line] = float(float(word_tag_count[line])/float(tag_count[line[1]]))
# Account for unseen tag/word pairs
for line in training:
	for tag in tag_count:
		if (line[0], tag) not in emis_mat:
			emis_mat[line[0], tag] = 0

print 'Running Virterbi on', sys.argv[2]
# VIRTERBI Algorithm
v = {}
obs_tags = []
for i in range(len(test)):
	# Set current observation
	o_i = test[i][0]
	cur_max = 0.0
	if o_i not in word_count:
		o_i = 'U'
	for tag in tag_count:
		emission_prob = emis_mat[o_i, tag]
		# Set back prob = trans prob = 1 first observation or end of sentence 
		if (i == 0 or o_i == "."):
			back_prob = 1.0
			transition_prob = 1.0
		else:
			# back values
			back_prob = obs_tags[i-1][2]
			back_tag = obs_tags[i-1][1]
			transition_prob = trans_mat[back_tag, tag]
		v[tag] = emission_prob * transition_prob * back_prob
		if v[tag] > cur_max:
			cur_max = v[tag]
			cur_max_tag = tag
	obs_tags.append([o_i, cur_max_tag, cur_max])

# Write to file
f = open('result.txt','w')
for i in range(len(test)):
	f.write(test[i][0] + '\t' + obs_tags[i][1] + '\n')
	if test[i][0] == '.':
		f.write('\n')
f.close()

print 'output to result.txt'
