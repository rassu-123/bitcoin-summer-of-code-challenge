# bitcoin-summer-of-code-challenge
#For  solving problem given in sb.README my approach-

 -made a graph for transaction of first 500 rows of csv file (as my laptop froze or programme crashed for more data) \
 -made edges between child and parent\
 -from this graph removed disconnected single node graph as there was no coinbase transaction\
 -made two arrays,both araay's ith index storing total fee and  weight of tansactions  of ith disconnected graph\
 -used code of 0/1 knapsack problem with dynamic programming approach to reach the solution i.e. transactions giving maximum fees to miner with total weight less than 4000000\
 -stored tx_id in block.txt\
 
