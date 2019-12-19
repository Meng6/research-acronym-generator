from nltk.corpus import wordnet as wn
from nltk.corpus import words
import itertools



def getSynWords(sent):
    # input: string (eg. word1 word2 ... wordk)
    # output: [word1_syn_dict, word2_syn_dict, ..., wordk_syn_dict]
    #          word1_syn_dict: {char: list of syn words}
    syn_sent = []
    for word in sent:
        syn_words = wn.synsets(word)
        syn_sent_X = {}
        for syn_word in syn_words:
            syn_sent_X[word[0]] = [word]
            syn_word_lemmas = syn_word.lemma_names()
            for syn_word_lemma in syn_word_lemmas:
                first_char = syn_word_lemma[0]
                if first_char not in syn_sent_X:
                    syn_sent_X[first_char] = [syn_word_lemma]
                else:
                    syn_sent_X[first_char] = syn_sent_X[first_char]+[syn_word_lemma]
        syn_sent.append(syn_sent_X)
    return syn_sent

def checkStrIsWord(str):
    if str in words.words():
        # print
        print("*******************************************************\n" + str)
        # write
        fout.write("*******************************************************\n" + str + "\n")
        return True
    else:
        return False

def getCandidateStr(syn_sent):
    chars = []
    for syn_word in syn_sent:
        chars.append(list(syn_word.keys())+[""])
    return list(itertools.product(*chars))


fout = open("candidate_words.txt", "w", encoding = "utf-8")

sent = "survivorship health interventions and exercise lifestyle data".split(" ")
syn_sent = getSynWords(sent)
candidate_strs = getCandidateStr(syn_sent)
already_considered_str = set()
print("Total " + str(len(candidate_strs)))
for _, candidate_tuple in enumerate(candidate_strs):
    if _ % 100 == 0:
        print("*******************************************************")
        print(str(_) + " / " + str(len(candidate_strs)) + " was done")
        print("*******************************************************")
    candidate_str = "".join(candidate_tuple)
    if candidate_str in already_considered_str:
        continue
    else:
        already_considered_str.add(candidate_str)
    if len(candidate_str) <= 3:
        continue
    if checkStrIsWord(candidate_str):
        for idx, char in enumerate(candidate_tuple):
            if char != "":
                # print
                print(char+": "+", ".join(syn_sent[idx][char]))
                # write
                fout.write(char+": "+", ".join(syn_sent[idx][char]) + "\n")
fout.close()