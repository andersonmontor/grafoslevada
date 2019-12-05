import networkx as nx 
from networkx.algorithms import bipartite
import numpy as np
import queue
import matplotlib.pyplot as plt



def tem_aresta(lista, aresta):
	a, b = aresta
	
	if (a,b) in lista:
		return (a,b)
	elif (b,a) in lista:
		return (b,a)
	else:
		return False
		
		
# Modificação de BFS pra achar caminho alternado
def caminho_alternado(G, M, x0, y):

	Q = queue.Queue()
	descoberto = [x0]
	Q.put([x0, False])
	
	T = nx.Graph()
	
	while not Q.empty():
		u, turno = Q.get()
		if u == y:
			return nx.shortest_path(T, x0, u)
		
		for v in list(G.adj[u]):			
			if v not in descoberto and (turno == bool(tem_aresta(M, (u,v)))):
				descoberto.append(v)
				T.add_edge(u, v)
				Q.put([v, not turno])

# Retorna array de cores
def pintar_arestas(G, M):
	colors = []
	edges = G.edges()
	for a, b in edges:
		if tem_aresta(M, (a,b)):
			colors.append('r')
		else:
			colors.append('k')
			
	return colors
	
	
# Desenha grafo bipartido e pinta arestas emparelhadas, se houver
def desenhar_bipartido(G, M = []):
	
	X, Y = bipartite.sets(G)
	pos = dict()
	pos.update((n, (1, i)) for i, n in enumerate(X))
	pos.update((n, (2, i)) for i, n in enumerate(Y))
	cores = pintar_arestas(G, M)
	nx.draw(G, with_labels = True, edge_color = cores, pos=pos)
	plt.show()
	
	
def algoritmo_hungaro(G, emp_inicial):

	M = emp_inicial
	X, Y = bipartite.sets(G)
	X = list(sorted(X))
	Y = list(sorted(Y))

	assert (nx.is_connected(G))

	iter = 1
	while True:

		vertices_emparelhados = [x for x,y in M] + [y for x,y in M]
		X_saturados = []

		for v in X:
			if v in vertices_emparelhados:
				X_saturados.append(v)

		X_saturados = sorted(X_saturados)
		
		# 1: Checa se M satura G
		if X == X_saturados:
			return (True, M) # Encontrou o emparelhamento, retornando o emparelhamento...

		
		x0 = None
		for v in X:
			if v not in X_saturados:
				x0 = v
				break

		assert (x0 != None)

		S = [x0]
		T = []

		# 2: Checa se N(S) == T
		while True:
			vertices_emparelhados = [x for x,y in M] + [y for x,y in M]
			Y_saturados = []
			for v in Y:
				if v in vertices_emparelhados:
					Y_saturados.append(v)
			Y_saturados = sorted(Y_saturados)
			
			neighbors_S = []
			for v in S:
				for neigh in list(G.adj[v]):
					if neigh not in neighbors_S:
						neighbors_S.append(neigh)
				
			neighbors_S = sorted(neighbors_S)
			T = sorted(T)
			S = sorted(S)

			if neighbors_S == T:
				return (False, S) #Nao é possivel emparelhar, retornando...

			y = None
			for v in neighbors_S:
				if v not in T:
					y = v
					break
				
			assert(y != None)
			
			# 3: Checa se y é saturado ou não-saturado

			z = None
			if y in Y_saturados:
				for a,b in M:
					if y == a:
						z = b
						break
					elif y == b:
						z = a 
						break
						
				S.append(z)
				T.append(y)
			else:
				caminho = caminho_alternado(G, M, x0, y)
				
				# Faz a transformação de acordo com as arestas no caminho P
				for i in range(len(caminho)-1):
					aresta = (caminho[i], caminho[i+1])
					aresta_emparelhada = tem_aresta(M, aresta)
					if aresta_emparelhada:
						M.remove(aresta_emparelhada)
					else:
						M.append(aresta)
						
					M = sorted(M, key = lambda x : x[0])			
				
				iter += 1
				
				break
				
				
if __name__ == "__main__":	
	G = nx.Graph()
	arestas = list(nx.read_edgelist('bipartidoA.txt').edges())	
	nodes = [str(x) for x in range(20)]
	nodesX = nodes[:10]
	nodesY = nodes[10:]
	G.add_nodes_from(nodesX, bipartite=0)
	G.add_nodes_from(nodesY, bipartite=1)
	G.add_edges_from(arestas)
	
	print ("Desenhando grafo inicial, sem nenhum emparelhamento...")
	desenhar_bipartido(G)
	
	escolha = input("Deseja usar o emparelhamento inicial da questão((0,11); (1,13))? (S/N): ").strip().lower() == 's'
	if not escolha:
		M_inicial = []
		print("Digite as arestas para adicionar ao emparelhamento inicial, separado por espaços(ex: 0 11), só ENTER para terminar...")
		while True:
			escolha_aresta = input(">> ")
			if not escolha_aresta:
				break
			else:
				a, b = escolha_aresta.strip().split()
				M_inicial.append((a,b))
	else:
		M_inicial = [('0','11'), ('1','13')]	
		
	print("Desenhando grafo com emparelhamento inicial...")
	desenhar_bipartido(G, M_inicial)
	
	encontrado, vetor = algoritmo_hungaro(G, M_inicial)
	if encontrado:
		print("Foi encontrado um emparelhamento máximo:", vetor)
		print("Desenhando grafo de emparelhamento máximo...")
		desenhar_bipartido(G, vetor)
	else:
		print("NÃO foi encontrado um emparelhamento máximo, retornando lista S no criterio de parada...")
		print("S:", vetor)
	
	