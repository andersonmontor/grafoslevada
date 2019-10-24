# -*- coding: utf-8 -*-
import numpy as np 
from sys import maxsize
np.set_printoptions(threshold=maxsize) # Essa setting é alterada permanentemente no sistema, favor voltar pra anterior

# Retorna arestas que começam com origem dada, (origem, _)
def busca_arestas(v_arestas, origem):
	resultado = []
	for a in v_arestas:
		if a[0] == origem:
			resultado.append(a)
	return resultado

# Constroi matriz de transições, considerando escadas e cobras
# m: casas do lado do tabuleiro(m x m)
# arestas_especiais: conjuntos das arestas cobras e escadas
def matrizP_snakesladders(m, arestas_especiais):
	n = m*m
	P = np.zeros((n,n))

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

	return P


# Retorna a matriz pagerank a partir de uma matriz quadrada e fator "a" dados
def matriz_pagerank(m_origem, a):
	m_pagerank = np.copy(m_origem)
	n = len(m_origem[1, :])

	for i in range(n):
		for j in range(n):
			m_pagerank[i][j] = (1. - a) * m_pagerank[i][j] + a * (1./n)

	return m_pagerank
	

# Entradas do enunciado
m = 6
arestas_snakes = (16,3), (19,5), (33,11), (23,15), (31,29)
arestas_ladders = (1,14), (4,6), (8,26), (17,28), (24,34)
k = k_pagerank = 100
a = 0.1

# Opção de escolha personalizada de entradas
escolha_config = None
while escolha_config != 's' and escolha_config != 'n':
	escolha_config = raw_input("Deseja usar o tabuleiro do enunciado?(S/N): ").strip().lower()
	
custom_entradas = (escolha_config != 's')
if custom_entradas:
	arestas_ladders = []
	arestas_snakes = []
	m = input("Quantidade de casas do lado do tabuleiro(n x n), n = ")
	print ("Tabuleiro (%d x %d), casas de 1 a %d, intervalo de arestas cobra/escada: [1, %d]" % (m, m, m*m, m*m-1))
	print ("\nDigite as arestas de cobra no formato: a, b (0 para parar).")
	while True:
		escolha_aresta = input("ARESTA COBRA: ")		
		if escolha_aresta == 0: break		
		if type(escolha_aresta) != type((1,2)):
			print ("Formato incorreto, por favor digite no formato: a, b")
			continue
		
		a, b = escolha_aresta[0], escolha_aresta[1]
		if (a <= b) or (a not in range(1, m*m+1)) or (b not in range(1, m*m+1)):
			print ("Insira no formato: a, b\nOnde a e b pertence a [1, %d] e (a > b), cobras voltam no tabuleiro." % (m*m-1))
		else:
			arestas_snakes.append((a-1, b-1))
	
	print ("\nDigite as arestas de escada no formato: a, b (0 para parar).")
	while True:
		escolha_aresta = input("ARESTA ESCADA: ")		
		if escolha_aresta == 0: break		
		if type(escolha_aresta) != type((1,2)):
			print ("Formato incorreto, por favor digite no formato: a, b")
			continue
		
		a, b = escolha_aresta[0], escolha_aresta[1]
		if (a >= b) or (a not in range(1, m*m)) or (b not in range(1, m*m)):
			print ("Insira no formato: a, b\nOnde a e b pertence a [1, %d] e (a < b), escadas avançam no tabuleiro." % (m*m-1))
		else:
			arestas_ladders.append((a-1, b-1))
			
	k = input("Iteracoes k do power method, k = ")
	a = input("Fator a entre 0 e 1 para matriz pagerank, a = ")
	k_pagerank = input("Iteracoes k do power method na matriz pagerank, k = ")
	
n = m ** 2
arestas_especiais = arestas_ladders + arestas_snakes

# Gera matriz P e probabilidade inicial w0
P = matrizP_snakesladders(m, arestas_especiais)
w0 = np.zeros(n)
w0[0] = 1. # Estado inicial, começa na primeira casa do tabuleiro
	
# Aplicacao do power method para obtenção da distribuição estacionária de P(questão B)
Pk = np.linalg.matrix_power(P, k)
wk = np.dot(w0, Pk)

# Aplicação do power method na matriz pagerank de P(questão C)
P_pagerank = matriz_pagerank(P, a)
Pk_pagerank = np.linalg.matrix_power(P_pagerank, k_pagerank)
wk_pagerank = np.dot(w0, Pk_pagerank)


# Mostra resultados obtidos no terminal
# TO DO: formatação melhor dos dados no terminal
print ("\n(1)Matriz de transicao P(%d x %d):" % (n, n))
print (P)
print ("\n(1)com elementos arredondados:")
print (P.round(3))
print ("\n(2)Distribuicao estacionaria depois de aplicacao do power method para k = %d:" % k)
print (wk)
print ("\n(2)com elementos arredondados:")
print (wk.round(3))

print ("\n(3)Matriz pagerank de P:")
print (P_pagerank)
print ("\n(3)com elementos arredondados:")
print (P_pagerank.round(3))
print ("\n(4)Distribuicao estacionaria da matriz pagerank, k = %d, a = %f:" % (k_pagerank, a))
print (wk_pagerank)
print ("\n(4)com elementos arredondados:")
print (wk_pagerank.round(3))

# TO DO: resultado grafico com NetworkX
# - plotar as transicoes iniciais colocando os vertices em formato de grid, e arestas de transição(só colocar label nas 100%)
# - plotar depois do power method com os labels dos vertices sendo as probabilidades de terminar naquele estado
# - plotar o mesmo que acima pro pagerank

# TO DO: passar um linter no codigo