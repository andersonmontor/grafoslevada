# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
inf = 99999999

opcoes_desenho = {
	"node_size": 150,
	"width": 0.2,
	"font_size": 8,
	"font_color": 'b'
}

def dijkstra_multi_raizes(G, v_raizes):
	
	# Inicializacao
	n = G.number_of_nodes()
	
	distancias = [inf] * n
	preds = [None] * n	
	Q = list(G.nodes)[:] # Copia da lista de nodes
	
	# Setta as k raizes como distancia 0
	for r in v_raizes:
		distancias[r] = 0
	
	# Faz o algoritmo padrão de dijkstra, só que com as multiplas raízes
	while len(Q) > 0:
	
		min = inf
		for v in Q:
			if distancias[v] < min:
				min = distancias[v]
				u = v
				
		Q.remove(u)
		
		for v in G.adj[u]:
			alt = distancias[u] + G[u][v]['weight']
			if alt < distancias[v]:
				distancias[v] = alt
				preds[v] = u	
	
	# Gera grafo de caminhos minimos de multiplas raizes(agrupamento)
	G_novo = nx.Graph()
	G_novo.add_nodes_from(G) # Copia os mesmos vertices de G
	
	# Adiciona as novas arestas calculadas pelo algoritmo de Dijkstra
	for v in range(len(preds)):
		if type(preds[v]) != type(None):
			u = preds[v]
			G_novo.add_edge(u, v)
		
	return G_novo
		
		
# Gera grafo a partir de arquivo de matriz de adjacencias e lista de nomes
A = np.loadtxt("wg59_dist.txt")
G = nx.from_numpy_matrix(A)

f = open("wg59_name.txt")
i = 0
nomes = {}
for linha in f.readlines():
	if not linha.startswith('#') and linha.strip() != '':
		nomes[i] = linha.strip()
		i += 1
f.close()

print(("Grafos G de cidades carregado: %d vertices e %d arestas.\n" % (G.number_of_nodes(), G.number_of_edges())))
print ("Desenhando grafo, feche para continuar...")
#Desenha grafo inicial das cidades, antes de agrupar
Gd = nx.relabel_nodes(G, nomes)
nx.draw(Gd, with_labels = True, **opcoes_desenho)
plt.show()

# Computa grafo de agrupamento, com k grupos
Ks = eval(input("Digite valores de k separados por virgula(pra responder questoes do enunciado, seria: 2, 3): "))
for k in Ks:
	v_raizes = eval(input("Digite as %d raizes separado por virgulas: " % k))

	H = dijkstra_multi_raizes(G, v_raizes)
	
	print(("Grafo H de agrupamento com %d grupos computado: %d vertices e %d arestas." % (k, H.number_of_nodes(), H.number_of_edges())))
	for r in v_raizes:
		sub = H.subgraph([r] + list(H.adj[r]))
		print(("\nGrupo de raiz: %d(%s)\nVertices: %d Arestas: %d" % (r, nomes[r], sub.number_of_nodes(), sub.number_of_edges())))
	
	print ("Desenhando grafo, feche para continuar...")
	opcoes_desenho["width"] = 1.0
	Hd = nx.relabel_nodes(H, nomes)
	nx.draw(Hd, with_labels = True, **opcoes_desenho)
	plt.show()