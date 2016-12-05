
import sys
import math

def dtree(examples, attributes, parent_examples):
    if len(examples)==0:
        node = AnswerNode(plurality(parent_examples))
        return node
    elif examples all have same outcome:
        return AnswerNode(calculated outcome)
    elif len(attributes) == 0:
        return AnswerNode(plurality(examples))
    else:    #find best attribute to split on, and build node to split on
        attr = best_split_attribute(examples, attributes)
        node = ChoiceNode(attr)
        for value in attr.get_values():  #all possible values of this attribute
            subexamples = [all examples where attr has value]
            child_tree = DTL(subexamples, attributes-attr, examples)
            add child_tree to node
        return node


def plurality(examples):
    pass


#input: attribute to split on, examples being split 
#output: value of information gained from splitting examples on given attribute
def gain(A, E):
    return h(A, E) - remainder(A,E)

#input: A: attribute to split on,  E: list of examples being split
#output: entropy value after splitting on that attribute
def h(A, E):
    #find all possible values for attribute A
    attrValues = []
    for i in range(len(E)):
        if E[i][A] not in attrValues:
            attrValues.append(E[i][A])
    #calculate sum of eqn
    total = 0.0
    for i in range(len(attrValues)):
        tmpP = p(attrValues[i])
        total += tmpP*math.log2(tmpP)
    return total * -1

#input: attribute, A, to split examples, E, on
#output: double used in calculation of gain()
def remainder(A, E):
    rangeE = range(len(E))
    #find all possible values for attribute A
    attrValues = []
    for i in rangeE:
        if E[i][A] not in attrValues:
            attrValues.append(E[i][A])
    subSets = [[0 for x in range(len(E[0][0]))] for y in range(len(attrValues))] 
    for i in rangeE:


#input: attribute to split on: V, and list of examples that will be split by A
#output: probability of outcome V
#last element of each example must be classification attribute
def p(A, E): 
    trueTotal = 0.0
    grossTotal = 0.0
    for e in E:
        grossTotal += 1
        if e[-1] == V:
            trueTotal += 1
    return trueTotal/grossTotal

def check_example():
    crappydtree = sample_tree()
    new_example = { 'patrons': 'full', 'hungry':'no', 'willwait':'no' }
    outcome = crappydtree.get_outcome(new_example)
    print('expected %s, got %s' % (new_example['willwait'], outcome))
    new_example2 = { 'patrons': 'full', 'hungry':'yes', 'willwait':'no' }
    outcome = crappydtree.get_outcome(new_example2)
    print('expected %s, got %s' % (new_example2['willwait'], outcome))



class ChoiceNode:
    def __init__(self, attr_name):
        self._attr = attr_name
        self._children = {}

    def add_child(self, attr_val, child_tree):
        self._children[attr_val] = child_tree

    def get_outcome(self, example):
        attr_val = example[self._attr]
        return self._children[attr_val].get_outcome(example)

class AnswerNode:
    def __init__(self, outcome):
        self._outcome = outcome

    def get_outcome(self, example):
        return self._outcome

def main():
    print(sys.argv[0])
    if len(sys.argv) > 1:
        print(sys.argv[1])
        fname = sys.argv[1]
        fp = open(fname, 'r')
        
        # read a single line
        fp.readline()
        
        # read the rest of the lines
        for line in fp:
            print(line.strip().split(','))
        
    check_example()

if __name__ == '__main__':
    main()
