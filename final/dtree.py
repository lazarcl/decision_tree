
'''
File name: dtree.py
Author username(s): lazarcl
Date: 12/6/16
Submission name: decision tree learning 


'''
import sys
import math
import random


#####################################################################
####################### dtl() and helper funcs ######################
#####################################################################

# input: list of examples to split on, list of attribute indexes that haven't been split yet in current path, list of examples used in previous split
# output: a tree of choicenodes and answernodes that can be used with testing 
#purpose: creates a decision tree of nodes to examine future examples on and predict their outcome
def dtree(examples, attributes, parent_examples):
    if len(examples)==0:
        return AnswerNode(plurality(parent_examples))
    (outcomeBool, outcomeResult) = sameOutcome(examples)
    if outcomeBool:
        return AnswerNode(outcomeResult)
    elif len(attributes) == 0:
        return AnswerNode(plurality(examples))
    else:    #find best attribute to split on, and build node to split on
        attr = best_split_attribute(examples, attributes)
        node = ChoiceNode(attr)
        for value in get_values(examples, attr):  #all possible values of this attribute
            subExamples = get_examples_w_attr_val(examples, attr, value)
            newAttributeList = attributes[:]
            newAttributeList.remove(attr)
            child_tree = dtree(subExamples, newAttributeList, examples)
            node.add_child(value, child_tree)
        return node


#input: list of examples, which are also lists. Last element of each example is the outcome
#output: outcome that is the most likely in given examples
#which outcome is most likely in the given examples
def plurality(examples):
    assert(len(examples)>0)
    #find total amt of outcomes for each possible value of outcome
    outcomes = {} #list to hold all possible outcomes
    for examp in examples:
        if outcomes.get(examp[-1]) == None:
            outcomes[examp[-1]] = 1
        else:
            outcomes[examp[-1]] += 1
    # find which attribute has highest count
    largestOutcome = examples[0][-1] #get a possible attribute val to start comparison
    for i in outcomes:
        if outcomes[i] > outcomes[largestOutcome]:
            largestOutcome = i
    return largestOutcome


#input: list of examples which are lists
#output: tuple of a bool and val. The bool is for checking whether all outcomes in example set are true, val is the val of the outcome
#purpose: to determine if the example set has the same outcome for all examples it contains
def sameOutcome(examples):
    prev = examples[0][-1]
    for examp in examples:
        if examp[-1] != prev:
            return (False, 0)
        prev = examp[-1]
    return (True, prev)


# input: list of examples to examine, an attribute index
# output: a list of possible values for that attribute in given examples
def get_values(examples, attr):
    values = []
    for i in examples:
        if i[attr] not in values:
            values.append(i[attr])
    return values

# input: list of examples, attr index, val for that attribute to count
# output: list of examples that all have the value attribute attr equal to given 'val'
# purpose: find the subset of examples that has a certain value of attribute "attr"
def get_examples_w_attr_val(examples, attr, val):
    subExamples = []
    for examp in examples:
        if examp[attr] == val:
            subExamples.append(examp)
    return subExamples


#input: list of examples in lists, list of attribute indexes to examine 
#output: index of attribute which has the best gain for given example set
#purpose: find best attribute to split on given example set using gain() as determinant
def best_split_attribute(examples, attributes):
    bestGain = 0
    bestAttr = attributes[0]
    for attr in attributes:
        tmpGain = gain(attr, examples)
        if tmpGain > bestGain:
            bestAttr = attr
            bestGain = tmpGain
    return attr


#input: attribute to split on, examples being split 
#output: value of information gained from splitting examples on given attribute
def gain(A, E):
    return h(E, A) - remainder(E, A)


#input: attribute, A, to split examples, E, on
#output: double used in calculation of gain()
def remainder(E, A):
    lenE = len(E)
    #create lists of examples as val of dict, key = possible val of A
    subSets = {}
    for examp in E:
        examp_A_val = examp[A]
        if examp_A_val not in subSets:
            subSets[examp_A_val] = []
            subSets[examp_A_val].append(examp)
        else:
            subSets[examp_A_val].append(examp)
    #sum for each subset, ratio of attribute val * entropy of selecting that var
    subSetLen = len(subSets)
    total = 0.0
    for i in subSets:
        ratio = len(subSets[i])/lenE
        hVal = h(subSets[i], A)
        total += ratio*hVal
    return total


#input: A: pos of attribute to split on in example lists,  E: list of examples being split
#output: entropy value after splitting on that attribute
def h(E, A):
    #find all possible values for attribute A
    attrValues = get_values(E, A)
    #calculate sum of eqn
    total = 0.0
    for i in range(len(attrValues)):
        tmpP = p(A, attrValues[i], E)
        total += tmpP*math.log2(tmpP)
    return total * -1.0


#input: pos of attribute in list: pos, val of attribute being split on: val, and list of examples that will be split by A
#output: probability of outcome V
#last element of each example must be classification attribute
def p(A, val, E): 
    valTotal = 0.0
    grossTotal = 0.0
    for e in E:
        grossTotal += 1
        if e[A] == val:
            valTotal += 1
    return valTotal/grossTotal


class ChoiceNode:
    def __init__(self, attr_name):
        self._attr = attr_name
        self._children = {}

    def add_child(self, attr_val, child_tree):
        self._children[attr_val] = child_tree

    def get_outcome(self, example):
        attr_val = example[self._attr]
        try:
            outcome = self._children[attr_val].get_outcome(example)
            return outcome
        except KeyError as e:
            return "ERROR: tree cannot handle example path"


class AnswerNode:
    def __init__(self, outcome):
        self._outcome = outcome

    def get_outcome(self, example):
        return self._outcome


#####################################################################
####################### testing/reading/running #####################
#####################################################################

#input: none
#output: prints the percent of test set that the tree predicted correctly
def main():
    if len(sys.argv) == 2:
        fname = sys.argv[1]
        (examples, attributes) = read_file(fname)
        (examples, testSet) = create_training_set(examples, 0.06)#decimal is percent of examples to reserve for testing
    elif len(sys.argv) == 3:
        trainFile = sys.argv[1]
        (examples, attributes) = read_file(trainFile)
        testFile = sys.argv[2]
        (testSet, tmp) = read_file(testFile)
    elif len(sys.argv) > 3:
        print("too many arguments. Should be:\n\tpython3 dtree.py trainExamples.csv testExamples.csv")
    tree = dtree(examples, attributes, [])
    (outcome, correctCount, totalCount)= test_tree(tree, testSet)
    print("test set got", outcome, "% correct.")



#input: file name to be read. must be csv with last column as outcome
#output: tuple of example list, and list of attribute indexes for example data
#purpose: helper func to read csv files, and pool attr values if it is iris_data.csv
def read_file(fname):
    try:
        fp = open(fname, 'r')
    except OSError:
        print("invalid file name: ", fname)
        quit()

    # read a single line
    line1 = fp.readline()
    line1Len = len(line1.strip().split(',')) - 1 #-1 to remove outcome col
    attributes = list(range(line1Len)) 
    
    examples = []
    # read the rest of the lines
    if fname == 'iris_train.csv':
        for line in fp:
            # split by commas
            vals = line.strip().split(',')

            # iris translation stuff
            plen = float(vals[0])
            pwid = float(vals[1])
            slen = float(vals[2])
            swid = float(vals[3])
            #set 
            vals[0] = sml(plen, 2.5, 4.9)
            vals[1] = sml(pwid, 1.7, 1.8)
            vals[2] = sml(slen, 6, 7)
            vals[3] = sml(swid, 2, 4)
            examples.append(vals)
    else:
        for line in fp:
            vals = line.strip().split(',')
            examples.append(vals)
    return (examples, attributes)


#input: node of head of tree created with dtree(), set of examples to test in tree
#output: percentage of examples which had the correct outcome in tree, num of accurate outcomes, num of total testexamples
#purpose: calculates the amount of examples in given set which are correct for given tree
def test_tree(tree, testSet):
    assert(len(testSet) > 0)
    assert(tree is not None)
    accurate = 0.0
    total = 0.0
    for i in testSet:
        expectedResult = i[-1]
        treeResult = tree.get_outcome(i)
        if expectedResult == treeResult:
            accurate += 1.0
        total += 1.0
    percent = round((accurate/total)*100, 2)
    return (percent, accurate, total)



#input: list of examples, percent of examples that training set should use in decimal
#output: (trainingset, testSet)  as lists
#randomly selects indexes to remove
def create_training_set(examples, trainingSize):
    if (len(examples) == 0) and (trainingSize < 1.0):
        return ([], [])
    testSet = []
    for i in range(int(len(examples)*trainingSize)):
        randomExampleIndex = random.randint(0,len(examples)-1)
        testSet.append(examples[randomExampleIndex])
        examples.pop(randomExampleIndex)
    return (examples, testSet)


#helper for reading and lumping attribute values in iris_train.csv
def sml(val, sval, mval):
    if val < sval:
        return 'short'
    elif val < mval:
        return 'medium'
    else:
        return 'long'


if __name__ == '__main__':
    main()

