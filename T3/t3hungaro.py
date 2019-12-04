import networkx as nx 
from networkx.algorithms import bipartite






def algoritmo_hungaro(G, emp_inicial):

	M = emp_inicial
	X, Y = bipartite.sets(G)

	assert (nx.is_connected(G))

	while True:

		vertices_emparelhados = [x for x,y in M] + [y for x,y in M]
		X_saturados = []
		Y_saturados = []

		for v in list(X.nodes):
			if v in vertices_emparelhados:
				X_saturados.append(v)

		for v in list(Y.nodes):
			if v in vertices_emparelhados:
				Y_saturados.append(v)


		# Checa se M satura G
		if sorted(list(X.nodes)) == sorted(X_saturados):
			return (True, M) # Encontrou o emparelhamento, retornando o emparelhamento...

		
		x0 = None
		for v in list(X.nodes):
			if v not in X_saturados:
				x0 = v
				break

		assert (x0 != None)

		S = [x0]
		T = []

		while True:
			vertices_emparelhados = [x for x,y in M] + [y for x,y in M]
			neighbors_S = []
			for v in S:
				neighbors_S += list(X.adj[v])

			if sorted(neighbors_S) == sorted(T):
				return (False, S) #Nao é possivel emparelhar, retornando...

			y = None
			for v in neighbors_S:
				if v not in T:
					y = v

			assert(y != None)

			z = None
			if y in Y_saturados:
				for a,b in M:
					if y == a:
						z = b
					elif y == b:
						z = a 

			assert(z != None)

			S.append(z)
			T.append(y)