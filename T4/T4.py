import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
inf = 99999999


# Retorna vertice minimo que está em Q
def min_vertice(Q, dist_dict):
	min = inf 
	min_v = None
	
	for v in dist_dict:
		if dist_dict[v] < min and v in Q:
			min = dist_dict[v]
			min_v = v 
	
	return min_v
	
def listaAmenosB(A, B):

	for v in A:
		if v in B:
			A.remove(v)
			
	return A

def MST_prim(G):
	
	dist = {}
	pred = {}
	
	# Inicialização
	for v in G.nodes:
		dist[v] = inf
		pred[v] = None
		
	Q = list(G.nodes)
	x0 = list(G.nodes)[0]
	
	dist[x0] = 0

	while len(Q) > 0:
		u = min_vertice(Q, dist)
		Q.remove(u)
		
		for v in G.adj[u]:
			if (v in Q) and (dist[v] > G[u][v]["weight"]):
				dist[v] = G[u][v]["weight"]
				pred[v] = u
	
	T = nx.Graph()
	for v in pred:
		T.add_edge(v, pred[v])
		
	return T
	
	
if __name__ == "__main__":

	# Gera grafo a partir de arquivo de matriz de adjacencias e lista de nomes
	A = np.loadtxt("ha30_dist.txt")

	f = open("ha30_name.txt")
	i = 0
	nomes = {}
	for linha in f.readlines():
		if not linha.startswith('#') and linha.strip() != '':
			nomes[i] = linha.strip()
			i += 1
	f.close()
	
	G = nx.from_numpy_matrix(A)
	G = nx.relabel_nodes(G, nomes)
	
	T = MST_prim(G)

	print ("Desenhando o grafo de entrada...")
	nx.draw(G, with_labels = True)
	plt.show()
	print ("Desenhando a arvore geradora mínima, gerada pelo algoritmo de Prim...")
	nx.draw(T, with_labels = True)
	plt.show()
					
			
	