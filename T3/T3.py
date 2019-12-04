import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
INF = 99999999

opcoes_desenho = {
	"node_size": 150,
	"width": 0.2,
	"font_size": 8,
	"font_color": 'b'
}

def nearest_neighbor_tour(G, start_node = None):
	
	if start_node == None:
		start_node = random.choice(list(G.nodes))
		
	H = [start_node]
	n = G.number_of_nodes()
	
	while len(H) < n:
		u = H[-1]
		neighbors = G.adj[u]
		min_e = INF
		for nb in neighbors:
			if (G[u][nb]['weight'] < min_e) and (nb not in H):
				min_e = G[u][nb]['weight']
				min_v = nb
		H.append(min_v)
		
	H.append(start_node)
	
	return H
	
# def two_optimal_tour(G, start_tour = None):

	# if start_tour == None:
		# start_tour = nearest_neighbor_tour(G)
		
	# T = start_tour[:]
	# n = G.number_of_nodes()
	
	# for i in range(0, n): 
		# for j in range(i+2, n):
			# Tn = T[:]
			# Tn
			
# def twice_around_tour(G, start_tour = None):
	
	# H = []
	# T = 
	
def tour_graph(tour_list):	
	G = nx.Graph()
	
	i = 0
	while i < len(tour_list)-1:
		G.add_edge(tour_list[i], tour_list[i+1])		
		i += 1
	
	return G
	
A = np.loadtxt("ha30_dist.txt")
G = nx.from_numpy_matrix(A)

f = open("ha30_name.txt")
i = 0
nomes = {}
for linha in f.readlines():
	if not linha.startswith('#') and linha.strip() != '':
		nomes[i] = linha.strip()
		i += 1
f.close()

print(("Grafos G de cidades carregado: %d vertices e %d arestas.\n" % (G.number_of_nodes(), G.number_of_edges())))
print ("Desenhando grafo, feche para continuar...")

#Desenha grafo inicial das cidades

#Gd = nx.relabel_nodes(G, nomes)
#nx.draw(Gd, with_labels = True, **opcoes_desenho)
#plt.show()

tour = nearest_neighbor_tour(G)
Gtour = tour_graph(tour)
print(tour)
print(Gtour.nodes)
Gd = nx.relabel_nodes(Gtour, nomes)
nx.draw(Gd, with_labels = True, **opcoes_desenho)
plt.show()
