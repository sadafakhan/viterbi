# viterbi
```viterbi.sh```: implements the Viterbi algorithm on an HMM part-of-speech tagger. 

Args: 
* ```input_hmm```: a file that represents an HMM. Header relays basic data about HMM, followed by delineation of initial state, transition, and emission probabilities. This can be generated using programs in the repository ```hmm```.
* ```test_file```:  Each line is an observation (i.e., a sequence of output symbols). For instance, if you use HMM for POS tagging, an observation will be a sentence (cf. test.word):

Returns: 
* ```output_file```: The format of the output file (cf. sys) is “observation => state seq lgprob”. 

To run: 
```
src/viterbi.sh input/hmmX input/test.word output/sysX
```

```conv_format.sh```: converts the output file of viterbi.sh to a new format. 

Args: 
* ```file1```: the file created by viterbi.sh, and has the format “observation => state seq lgprob”

Returns: 
* ```file2```: has the format “w1/t1 w2/t2 ... wn/tn”. where ti is the second tag of the state that generates wi.

To run: 
```
cat output/file1 | conv src/format.sh > output/file2
```

HW8 OF LING570 (11/27/2021)