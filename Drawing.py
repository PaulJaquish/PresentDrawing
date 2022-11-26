# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 10:56:43 2022

@author: Paul
"""

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
from random import seed, shuffle
from copy import deepcopy

seed_value = 42

"""
The keys in this dictionary are the names that identify each participant. The 
values represent the families of the participants. People in the same family 
are never matched in the present drawing, since it is assumed that they are 
already giving each other presents.
"""
participants_and_families = {"Marty": 1,
                            "Janet": 1,
                            "Margaret": 2,
                            "Harold": 2,
                            "Bob": 2,
                            "Gary": 2,
                            "Stanley": 2,
                            "Eugene": 3,
                            "Pearl": 3,
                            "Alan": 3,
                            "Betsy": 3,
                            "Sandy": 4,}


participants = [i for i in participants_and_families.keys()]
families = [i for i in participants_and_families.values()]

participants_giving = deepcopy(participants)
participants_receiving = deepcopy(participants)


"""
Randomizing the givers and receivers separately makes sure that they are
ordered differently. This prevents everyone buying a gift for the person who is
buying them a gift. In practice, we preferred having a chain of gifts instead
of a series of pairs.
"""
seed(seed_value)
shuffle(participants_giving)
shuffle(participants_receiving)

participant_count = len(participants)


"""
In a nutshell, we're creating a flow diagram with n nodes in the first layer 
and n nodes in the second layer. The n nodes in the first layer are numbered 
0 to n-1 and represent the possible present givers. The n nodes in the second
layer are numbered n to 2n-1 and represent the possible present receivers. All
connections at this point are between a giving node and a receiving node. A 
connection is established if the possible giver and receiver are in different 
families. The flow diagram is directed - each connection goes from the node
given by the row and to the node given by the column.
"""
row = []
col = []
data = []

for giver in participants_giving:
    for receiver in participants_receiving:
        if (participants_and_families[giver] != 
            participants_and_families[receiver]):
            row.append(participants_giving.index(giver))
            col.append\
                (participants_receiving.index(receiver)+participant_count)
            data.append(1)
            
"""
The last step is to create a source and sink node for the flow diagram. The 
source node is numbered 2n and links to each node in the first layer. The sink
node is numbered 2n+1 and links from each node in the second layer.
"""
source = 2*participant_count
sink = 2*participant_count+1

for i in range(participant_count):
    """
    Link the source node.
    """
    row.append(source) #number of source node
    col.append(i) #iterates through all nodes in the first layer
    data.append(1)
    """
    Link the sink node.
    """
    row.append(i+participant_count) #iterates through all second layer nodes
    col.append(sink) #number of sink node
    data.append(1)
    
"""
Now, we use our lists to create to a csr_matrix, run the maximum_flow
algorithm and output the results. With nodes numbered from 0 to 2n+1, we have 
2n+2 nodes to pass to the flow matrix.
"""

dim = 2*participant_count+2

"""
The maximum_flow function requires a csr_matrix as an input.
"""
flow_graph = csr_matrix((data, (row, col)), shape=(dim, dim))
"""
The maximum_flow function returns a MaximumFlowResult object, of which we are
only interested in the flow attribute. The flow attribute is in the form of a
csr_matrix, which is then immediately converted to a numpy ndarray for 
convenience
"""
max_flow = maximum_flow(flow_graph, source, sink).flow.toarray()

"""
First, the ndarray is reduced to only the relevant portion - the n by n matrix
showing which nodes in the first layer connect to which nodes in the second.
Then, the nonzero function reduces the two-dimensional array into two 
one-dimensional arrays, having the row numbers and column numbers of the 
entries that are not 0 (i.e., the connections).
"""
row_out, col_out = max_flow[0:participant_count, \
                            participant_count:2*participant_count].nonzero()
    
for i in range(len(row_out)):
    row_number = row_out[i]
    col_number = col_out[i]
    print("{} buys for {}".format(participants_giving[row_number], \
                                      participants_receiving[col_number]))
    




