#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 22:20:51 2019

@AUTHOR: Gopi Miyani    10437266

PURPOSE OF PROGRAM: To process the given input file and identify triads.

PROGRAM SPECIFICATIONS:
  
    Accept a filename from the user. This can be done either by use of an argument list or by prompting the user
    for the information.
    eg: python3 triads.py --filename myfile
    or: *** Enter the file name: (user input)
    
    Process the input file and your output should contain the following:
    1. Number of edges in the network
    2. Number of self-loops
    3. Number of edges used to identify triads (referred to as TotEdges) [ this should be a. – b. ]
    4. Number of positive (trust) edges (ignore self-loops)
    5. Number of negative (distrust) edges (ignore self-loops)
    6. Probability p that an edge will be positive: (number of positive edges) / TotEdges
    7. Probability that an edge will be negative: 1 – p
    8. Expected distribution of triad types ( based on p and 1 – p applied to the number of triangles in the
    graph). Show number and percent.
    a. Trust-Trust-Trust
    b. Trust-Trust-Distrust
    c. Trust- Distrust -Distrust
    d. Distrust- Distrust- Distrust
    e. Total
    9. Actual distribution of triad types. Show number and percent.
    a. Trust-Trust-Trust
    b. Trust-Trust-Distrust
    c. Trust- Distrust -Distrust
    d. Distrust- Distrust- Distrust
    e. Total
    
RUN INSTRUCTIONS:
# to run from terminal window:  
#      python3 GopiMiyani_Assignment06.py --filename myfile
#  where:  myfile = csv file name that you want to process

    
 --------   FOR ME::: ---------
 
"""


import pandas as pd    #  need for reading csv file as dataframe
import networkx as nx  #  need for creation and manipulation of complex network
import argparse        #  need for parsing the arguments in the command line
from itertools import combinations as comb   # need for getting possible combinations


def get_triangles(g):
    nodes = g.nodes()
    print("Hi..")
    print(nodes)
    
    for n1 in nodes:
        neighbors1 = set(g[n1])
    for n2 in filter(lambda x: x>n1, nodes):
        neighbors2 = set(g[n2])
        common = neighbors1 & neighbors2
    for n3 in filter(lambda x: x>n2, common):
        print(n1,n2,n3)
        #yield n1, n2, n3


def process_graph_data(data):
    
    # Create an empty graph
    g=nx.Graph()
    
    # Iterate over data of csv
    for index, row in data.iterrows():
        # Set reviewer, reviewee and trust values
        reviewer=row['reviewer']
        reviewee=row['reviewee']
        trust=row['trust']
        
        # add nodes and edge between nodes in graph
        g.add_node(reviewer)
        g.add_node(reviewee)
        g.add_edge(reviewer,reviewee,weight=trust)
       
    # Number of nodes
    count_nodes=g.number_of_nodes()
    print("\nNodes in the network: ",count_nodes)
  
    # 1. Number of edges in the network
    count_edges=g.number_of_edges()
    print("Edges in the network: ",count_edges)

    
    # 2. Number of self-loops
    count_self_loops=0
    for n in g.nodes_with_selfloops():
        count_self_loops=count_self_loops+1
    print("Self-loops: ",count_self_loops)
  
    # 3. Number of edges used to identify triads (referred to as TotEdges) [ It is 1. – 2. ]
    count_totedges=count_edges-count_self_loops
    print("Edges used - TotEdges: ", count_totedges)
    
    # 4. Number of positive (trust) edges (ignore self-loops) and
    # 5. Number of negative (distrust) edges (ignore self-loops)
    count_pos_edges=0
    count_neg_edges=0
    for reviewer,reviewee,trust in g.edges(data=True):
        if trust['weight'] == 1:
            count_pos_edges=count_pos_edges+1
        if trust['weight'] == -1:
            count_neg_edges=count_neg_edges+1
    print("Trust edges: ",count_pos_edges)
    print("Distrust edges: ",count_neg_edges)
    
    
    # 6. Probability p that an edge will be positive: (number of positive edges) / TotEdges
    p_pos_edge=count_pos_edges/count_totedges
    print("Probability p (an edge will be positive): ",round(p_pos_edge,2))
    
    # 7. Probability that an edge will be negative: 1 – p
    p_neg_edge=1 - p_pos_edge
    print("Probability 1 - p (an edge will be negative): ",round(p_neg_edge,2))
    
    # Count total number of triangles
    triangles = nx.triangles(g) 
    count_triangles = sum(triangles.values())/3     # When computing triangles for the entire graph each triangle is counted three times
    print("Numer of Triangles: ",count_triangles)
    
    # 8. Expected distribution of triad types ( based on p and 1 – p applied to the number of triangles in the
    # graph). Show number and percent.
    # a. Trust-Trust-Trust
    # b. Trust-Trust-Distrust
    # c. Trust- Distrust -Distrust
    # d. Distrust- Distrust- Distrust
    # e. Total
    print("\nExpected Distribution:")
    print("Type\tpercent\tnumber")
    
    TTT_percent= round((p_pos_edge ** 3) * 100,1)
    TTT_num= round((count_triangles * TTT_percent)/100,1)
    print("TTT\t" + str(TTT_percent) + "\t" + str(TTT_num))
    
    TTD_percent= round((p_pos_edge ** 2 * p_neg_edge * 3) * 100,1)
    TTD_num= round((count_triangles * TTD_percent)/100,1)
    print("TTD\t" + str(TTD_percent) + "\t" + str(TTD_num))
    
    TDD_percent= round((p_pos_edge * (p_neg_edge ** 2) * 3) * 100,1)
    TDD_num= round((count_triangles * TDD_percent)/100,1)
    print("TDD\t" + str(TDD_percent) + "\t" + str(TDD_num))
    
    
    DDD_percent= round((p_neg_edge ** 3) * 100,1)
    DDD_num= round((count_triangles * DDD_percent)/100,1)
    print("DDD\t" + str(DDD_percent) + "\t" + str(DDD_num))
    
    print("Total\t" + str(100) + "\t" + str(count_triangles))
    
    # 9. Actual distribution of triad types. Show number and percent.
    # a. Trust-Trust-Trust
    # b. Trust-Trust-Distrust
    # c. Trust- Distrust -Distrust
    # d. Distrust- Distrust- Distrust
    # e. Total
   
    print('\nTriads that are found:')
    weight = nx.get_edge_attributes(g, 'weight')
    # Get triangles
    Triads = [edge for edge in nx.enumerate_all_cliques(g)if len(edge) == 3]
    #Get triads list with each combination of nodes and respective weight of edge
    triads_list = list(map(lambda edge: list(map(lambda edge: (edge, weight[edge]), comb(edge, 2))), Triads))
    count_TTT=0
    count_TTD=0
    count_TDD=0
    count_DDD=0
    # Loop throgh all triangles
    for triad in triads_list:
        e1_weight=triad[0][1]
        e2_weight=triad[1][1]
        e3_weight=triad[2][1]
    
        # Check for edge_weight, determine type of triad and calcualate total triads of each type
        if(e1_weight==1 and e2_weight==1 and e3_weight==1):
            triad_type="TTT"
            count_TTT = count_TTT +1
        if(e1_weight==1 and e2_weight==1 and e3_weight==-1) or (e1_weight==-1 and e2_weight==1 and e3_weight==1) or (e1_weight==1 and e2_weight==-1 and e3_weight==1):
            triad_type="TTD"
            count_TTD=count_TTD+1
        if(e1_weight==-1 and e2_weight==-1 and e3_weight==1) or (e1_weight==1 and e2_weight==-1 and e3_weight==-1) or (e1_weight==-1 and e2_weight==1 and e3_weight==-1):
            triad_type="TDD"
            count_TDD =count_TDD + 1
        if(e1_weight==-1 and e2_weight==-1 and e3_weight==-1):
            triad_type="DDD"
            count_DDD=count_DDD+1
        print(triad_type + "\t" + str(triad[0]) + "\t" + str(triad[1]) + "\t" + str(triad[2]))
    
    # Calculate percentage of each triad  type
    TTT_percent=round((count_TTT *100)/count_triangles,1)
    TTD_percent=round((count_TTD *100)/count_triangles,1)
    TDD_percent=round((count_TDD *100)/count_triangles,1)
    DDD_percent=round((count_DDD *100)/count_triangles,1)
    print("\nActual Distribution:")
    print("Type\tpercent\tnumber")
    print("TTT\t" + str(TTT_percent) + "\t" + str(count_TTT))
    print("TTD\t" + str(TTD_percent) + "\t" + str(count_TTD))
    print("TDD\t" + str(TDD_percent) + "\t" + str(count_TDD))
    print("DDD\t" + str(DDD_percent) + "\t" + str(count_DDD))
    print("Total\t" + str(100) + "\t" + str(count_triangles))
    
    
    
# main routine
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YouTube Search')
    parser.add_argument("--filename", default="epinions96.csv")
    args = parser.parse_args()
    graph_data= pd.read_csv(args.filename, names=["reviewer", "reviewee", "trust"])
    process_graph_data(graph_data)













