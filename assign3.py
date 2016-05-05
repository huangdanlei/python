import csv
import networkx as nx
import string 
from operator import itemgetter, attrgetter 
g = nx.Graph()
h = nx.DiGraph()
edges = open("edges.csv").read()
edge_r = edges.split("\n")
for row in range(len(edge_r)):
	edge_r[row] = edge_r[row].split(";")
h.add_edges_from(edge_r)
nodes = open("nodes.csv").read()
node_r = nodes.split("\n")
for x in range(len(node_r)):
	node_r[x] = node_r[x].split(";")
print node_r
node_dic = dict(node_r)
h.add_nodes_from(node_dic.keys())
h.remove_node("Id")
h.remove_edge("Source","Target")
h.remove_node("Source")
h.remove_node("Target")

indegree = nx.in_degree_centrality(h)
indegree_sort = sorted(indegree.iteritems(), key=itemgetter(1), reverse=True)
indegree_result = indegree_sort[:4]
string = []
for row in indegree_result:
	string.append(row[0])
print "Indegree:"
for row in string:
	print node_dic[row]

outdegree = nx.out_degree_centrality(h)
outdegree_sort = sorted(outdegree.iteritems(), key=itemgetter(1), reverse=True)
outdegree_result = outdegree_sort[:4]
string_out = []
for row in outdegree_result:
	string_out.append(row[0])
print "Outdegree:"
for row in string_out:
	print node_dic[row]

closeness = nx.closeness_centrality(h)
closeness_sort = sorted(closeness.iteritems(), key=itemgetter(1), reverse=True)
closeness_result = closeness_sort[:4]
string_closeness = []
for row in closeness_result:
	string_closeness.append(row[0])
print "Closeness:"
for row in string_closeness:
	print node_dic[row]

betweenness = nx.betweenness_centrality(h)
betweenness_sort = sorted(betweenness.iteritems(), key=itemgetter(1), reverse=True)
betweenness_result = betweenness_sort[:4]
string_betweenness = []
for row in betweenness_result:
	string_betweenness.append(row[0])
print "Betweenness:"
for row in string_betweenness:
	print node_dic[row]

