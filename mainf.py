from csv import reader
import pandas as pd
from io import StringIO
import csv
import networkx as nx
from tqdm import tqdm
import itertools
# Python3 code for Dynamic Programming
# based solution for 0-1 Knapsack problem

# Prints the items which are put in a
# knapsack of capacity W
def printknapSack(G,W, wt, val, n,ans):
  K = [[0 for w in range(W + 1)]for i in range(n + 1)]
  
# initialize the spaces with 0’s with 
# the help of list comprehensions

  
  for i in range(n + 1):
    for w in range(W + 1):
      if i == 0 or w == 0:
        K[i][w] = 0
      elif wt[i - 1] <= w:
        K[i][w] = max(val[i - 1]+ K[i - 1][w - wt[i - 1]],K[i - 1][w])
      else:
        K[i][w] = K[i - 1][w]

	# stores the result of Knapsack
  res = K[n][W]
	
	
  w = W
  for i in range(n, 0, -1):
    if res <= 0:
      break
    if res == K[i - 1][w]:
      continue
    else:

      ans[i-1]=1
      res = res - val[i - 1]
      w = w - wt[i - 1]


# G is network graph
G = nx.Graph()
with open('mempool.csv', 'r') as f:
     data = csv.reader(f)
     #data = data.head(20)
     headers = next(data)
     #for row in itertools.islice(tqdm(data),59):
     for row in tqdm(data):
	#making node and with fee ,weight and parents as it's attribute
        G.add_node(row[0],fee=row[1],weigh=row[2],parent=row[3]) 
        # if parent exists make edge between these two nodes with fee and weight i.e. child and parent 
        if row[3]!="":  
         # if there are more than one parent for a tx_id
         parents = row[3].split(';')
         for parent in parents:
           
            G.add_edge(row[0], parent,fee=row[1],weight=row[2])
# as there is no coinbase transaction so removing single nodes from graph
G.remove_nodes_from(list(nx.isolates(G)))
# for visualising graph
nx.draw_networkx(G, node_size=3,with_labels =False)
# N is the number of disconnected graphs in graph G
N=nx.number_connected_components(G)
# making two arrays FEE and WEIGHT to store total FEE and WEIGHT of ith disconnected graph in ith index
FEE = [0 for n in range(N + 1)]
WEIGHT = [0 for n in range(N + 1)]
# d is collection of all disconnected graphs of G
d =(G.subgraph(c) for c in nx.connected_components(G))

for i,sg in enumerate(d):
       
    
     
      ne=sg.number_of_edges()
    
      f=0
      wt=0
# iterating through all edges using depth first search to get total fee and total weight of subgraph sg 
      for edge in nx.dfs_edges(sg,depth_limit=ne):
          f=f+int(sg.get_edge_data(edge[0],edge[1])['fee'])
          wt=wt+int(sg.get_edge_data(edge[0],edge[1])['weight'])
         
      FEE[i]=f;
      WEIGHT[i]=wt;

W=4000000
# using 0/1 knapsack method to get subgraphs that will give maximum fees possible with weight less than W (4000000)
ans=[]
ans= [0 for x in range(N)]	
printknapSack(G,W,FEE,WEIGHT, N,ans)
d =(G.subgraph(c) for c in nx.connected_components(G))
fh = open('block.txt','w')
# printing output
for i,sg in enumerate(d):
  if(ans[i]==1):
    ne=sg.number_of_edges()
    for edge in nx.dfs_edges(sg,depth_limit=ne):
     
      L=str(edge[0])
      fh.write(L)
      fh.write('\n')
      L=str(edge[1])
      fh.write(L)
      fh.write('\n')
      print("next")
  fh.write('\n\ntx_id of next required chain\n\n')
fh.close()
