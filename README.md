# viterbi
```viterbi.sh```: implements the Viterbi algorithm. 

Args: 
* input_hmm: a file that represents an HMM. Header relays basic data about HMM, followed by delineation of initial state, transition, and emission probabilities.
* test_file:  Each line is an observation (i.e., a sequence of output symbols). For instance, if you use HMM for POS tagging, an observation will be a sentence (cf. test.word):

Returns: 
* output_file: The format of the output file (cf. sys) is “observ => state seq lgprob”. 

To run: 
```
viterbi.sh input_hmm test_file output_file
```

```conv_format.sh```: converts the output file of viterbi.sh to a new format. 

Args: 
* file1: the file created by viterbi.sh, and has the format “observ => state seq lgprob”

Returns: 
* file2: has the format “w1/t1 w2/t2 ... wn/tn”. where ti is the second tag of the state that generates wi.

To run: 
```
cat file1 | conv format.sh > file2
```

HW8 OF LING570 (11/27/2021)