# -*- coding: utf-8 -*-
import numpy as np 

# Retorna arestas que começam com origem dada, (origem, _)
def busca_arestas(v_arestas, origem):
	resultado = []
	for a in v_arestas:
		if a[0] == origem:
			resultado.append(a)
	return resultado

# Retorna a matriz pagerank a partir de uma matriz e fator "a" dados
def matriz_pagerank(m_origem, a):
	m_pagerank = np.copy(m_origem)
	n = len(m_origem[1, :])

	for i in range(n):
		for j in range(n):
			m_pagerank[i][j] = (1. - a) * m_pagerank[i][j] + a * (1./n)

	return m_pagerank

m = 6
n = m ** 2
P = np.zeros((n,n))

# Arestas de escadas e cobras obtidas do diagrama
arestas_snakes = (16,3), (19,5), (33,11), (23,15), (31,29)
arestas_ladders = (1,14), (4,6), (8,26), (17,28), (24,34)
arestas_especiais = arestas_ladders + arestas_snakes

# Constroi matriz de transições, considerando escadas e cobras
for i in range(n-2):
	for j in range(1,3): # j = 1 e 2
		especial = busca_arestas(arestas_especiais, i + j)
		dest = i + j
		if especial:
			dest = especial[0][1]

		P[i][dest] = 0.5
		
# Como penultima casa só pode avançar pra ultima, tem probabilidade 100%
P[n-2][n-1] = 1.
# Ultima casa é absorvente, ou seja, transita 100% pra ele mesmo
P[n-1][n-1] = 1.

w0 = np.zeros(n)
w0[0] = 1. # Estado inicial, começa na primeira casa do tabuleiro
k = 100
# Aplicacao do power method para obtenção da distribuição estacionária de P(questão B)
Pk = np.linalg.matrix_power(P, k)
wk = np.dot(w0, Pk)

# Aplicação do power method na matriz pagerank de P, com fator a = 0.1(questão C)
P_pagerank = matriz_pagerank(P, 0.1)
Pk_pagerank = np.linalg.matrix_power(P_pagerank, k)
wk_pagerank = np.dot(w0, Pk_pagerank)


# Mostra resultados obtidos
print ("\nDistribuicao estacionaria depois de aplicação do power method para k = 100:")
print (wk)
print ("\nCom elementos arredondados:")
print (wk.round(2))

print ("\nDistribuicao estacionaria da matriz pagerank, k = 100, a = 0.1:")
print (wk_pagerank)
print ("\nCom elementos arredondados:")
print (wk_pagerank.round(2))