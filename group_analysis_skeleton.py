#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack and Nichole Bouffard
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats as stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#
os.chdir('/Users/nicholebouffard/Documents/GitHub/ps2-nrbouffard/')

testingrooms = ['A','B','C']
for room in testingrooms:
    shutil.copy('testingroom' + room + '/experiment_data.csv', 'rawdata')
    os.rename('rawdata/experiment_data.csv', 'rawdata/experiment_data_' + room + '_moved.csv')



#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#

data = np.empty((0,5))
for room in testingrooms:
    filename = 'rawdata/experiment_data_'+ room + '_moved.csv'
    tmp = sp.loadtxt(filename, delimiter = ',')
    data = np.vstack([data,tmp])



#%%
# calculate overall average accuracy and average median RT
#
acc_avg = np.average(data[:,3])   # 91.48%
mrt_avg = np.average(data[:,4])   # 477.3ms


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#
accWord_sum = 0
rtWord_sum = 0 
accFace_sum = 0
rtFace_sum = 0
facecount = 0
wordcount = 0

for x in range(len(data)):
    if data[x,1] == 1:
        accWord_sum += data[x,3]
        rtWord_sum += data[x,4]
    else:
        wordcount += 1
        accFace_sum += data[x,3]
        rtFace_sum += data[x,4]
        facecount += 1

# words: 88.6%, 489.4ms   
accWord_mean = accWord_sum/wordcount
rtWord_mean = rtWord_sum/wordcount


#faces: 94.4%, 465.3ms
accFace_mean = accFace_sum/facecount
rtFace_mean = rtFace_sum/facecount

#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#
acc_wp = np.mean(data[data[:,2] == 1, 3])  # 94.0%
acc_bp = np.mean(data[data[:,2] == 2, 3])  # 88.9%
mrt_wp = np.mean(data[data[:,2] == 1, 4])  # 469.6ms
mrt_bp = np.mean(data[data[:,2] == 2, 4])  # 485.1ms



#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#
worddat = data[data[:,1]==1,:]
facedat = data[data[:,1]==2,:]

# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms

words_medRT_WP = np.mean(worddat[worddat[:,2]==1,4]) 
words_medRT_BP = np.mean(worddat[worddat[:,2]==2,4]) 
faces_medRT_WP = np.mean(facedat[facedat[:,2]==1,4])
faces_medRT_BP = np.mean(facedat[facedat[:,2]==2,4]) 

#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
t_test_word = stats.ttest_rel(worddat[worddat[:,2]==1,4], worddat[worddat[:,2]==2,4]) 
t_test_face = stats.ttest_rel(facedat[facedat[:,2]==1,4], facedat[facedat[:,2]==2,4]) 


# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#

print('\nOn blocks in which words were categorized, the average median response time for black/pleasant pairings ({:.1f} ms) was significantly greater than the average median response time for white/pleasant pairings ({:.1f} ms), t = {:.2f}, p < .001.'.format(words_medRT_BP, words_medRT_WP, t_test_word[0]))

print('\nOn blocks in which faces were categorized, the average median response time for black/pleasant pairings ({:.1f} ms) was significantly greater than the average median response time for white/pleasant pairings ({:.1f} ms), t = {:.2f}, p < .05.'.format(faces_medRT_BP, faces_medRT_WP, t_test_face[0]))

#other averages
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))
print('\nWORD STIMULI: {:.2f}%, {:.1f} ms'.format(100*accWord_mean,rtWord_mean))
print('\nFACE STIMULI: {:.2f}%, {:.1f} ms'.format(100*accFace_mean,rtFace_mean))
print('\nCONGRUENCY (WHITE/PLEASANT): {:.2f}%, {:.1f} ms'.format(100*acc_wp,mrt_wp))
print('\nCONGRUENCY (BLACK/PLEASANT): {:.2f}%, {:.1f} ms'.format(100*acc_bp,mrt_bp))
...