'''
UNIVERSIDADE FEDERAL DO AMAZONAS
ENGENHARIA DE SOFTWARE
ALGORITMO E ESTRUTURA DE DADOS 2
DOGO

JOHNATAS PHILIPE RODRIGUES DA SILVA
PEDRO HENRIQUE SOUZA DOS SANTOS

'''

class Estado:
    def __init__(self, coordenada, proibidos, passos, m, n, estado_anterior=None):
        self.linha = coordenada[0]
        self.coluna = coordenada[1]
        self.destinoLinha = m - 1
        self.destinoColuna = n - 1
        self.proibidos = proibidos
        self.estado_anterior = estado_anterior
        self.g = passos
        self.h = abs(self.destinoLinha - self.linha) + abs(self.destinoColuna - self.coluna)
        self.f = self.g + self.h

    def transicoes(self):
        saida = []
        if 0 <= self.coluna + 1 <= self.destinoColuna:
            direita = (self.linha, self.coluna + 1)
            if direita not in self.proibidos:
                possivelTransicao = Estado(direita, self.proibidos, self.g + 1, m, n, self)
                saida.append(possivelTransicao)

        if 0 <= self.linha + 1 <= self.destinoLinha:
            baixo = (self.linha + 1, self.coluna)
            if baixo not in self.proibidos:
                possivelTransicao = Estado(baixo, self.proibidos, self.g + 1, m, n, self)
                saida.append(possivelTransicao)
        if 0 <= self.coluna - 1 <= self.destinoColuna:
            esquerda = (self.linha, self.coluna - 1)
            if esquerda not in self.proibidos:
                possivelTransicao = Estado(esquerda, self.proibidos, self.g + 1, m, n, self)
                saida.append(possivelTransicao)
        if 0 <= self.linha - 1 <= self.destinoLinha:
            cima = (self.linha - 1, self.coluna)
            if cima not in self.proibidos:
                possivelTransicao = Estado(cima, self.proibidos, self.g + 1, m, n, self)
                saida.append(possivelTransicao)

        return saida

    def caminho_perdido(self):
        caminho = [self]
        estado_atual = self
        while estado_atual.estado_anterior:
            caminho.insert(0, estado_atual.estado_anterior)
            estado_atual = estado_atual.estado_anterior
        return caminho

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return "({},{})".format(self.linha, self.coluna)


def inserirEstado(heap, estado):
    ultimo = len(heap)
    heap.append(estado)
    pai = (ultimo - 1) // 2
    while pai >= 0 and heap[ultimo] < heap[pai]:
        heap[pai], heap[ultimo] = heap[ultimo], heap[pai]
        ultimo = pai
        pai = (ultimo - 1) // 2
    return heap


def min_heapify(semiHeap, tamanho, raiz):
    menor = raiz
    esquerda = 2 * raiz + 1
    if esquerda < tamanho and semiHeap[menor] > semiHeap[esquerda]:
        menor = esquerda

    direita = (2 * raiz) + 2
    if direita < tamanho and semiHeap[menor] > semiHeap[direita]:
        menor = direita

    if menor != raiz:
        semiHeap[raiz], semiHeap[menor] = semiHeap[menor], semiHeap[raiz]
        min_heapify(semiHeap, tamanho, menor)

    return semiHeap


def redimensionar_heap(heap, tamanho):
    return heap[:tamanho]


def removerEstado(heap, tam):
    heap[0], heap[tam - 1] = heap[tam - 1], heap[0]
    novaHeap = redimensionar_heap(heap, tam - 1)
    min_heapify(novaHeap, tam - 1, 0)
    return novaHeap


def buscaInformada(estadoInicial):
    agenda = []
    estadosPassados = set()
    estado = estadoInicial
    agenda.append(estado)
    estadosPassados.add((estado.linha, estado.coluna))
    while agenda:
        estado = agenda[0]
        agenda = removerEstado(agenda, len(agenda))
        if estado.linha == estado.destinoLinha and estado.coluna == estado.destinoColuna:
            return estado
        transicao = estado.transicoes()

        for opcao in transicao:
            proximo = opcao
            if (proximo.linha, proximo.coluna) not in estadosPassados:
                inserirEstado(agenda, proximo)
                estadosPassados.add((proximo.linha, proximo.coluna))

    return -1


# Obter as dimensões da matriz do usuário
m = int(input("Digite o número de linhas: "))
n = int(input("Digite o número de colunas: "))

# Inicializar a matriz com valores de coordenadas

def imprimir_matriz(m, n, matriz):
    for i in range(m):
        for j in range(n):
            print(f' {matriz[i][j]:^9} ', end='')  
            if j < n - 1:
                print('|', end='')  
        print()
        if i < m - 1:
            print('-' * (9 * n - 1))

    print()

def regiao_proibida(x, y, obstaculos, matriz, m, n):
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i >= 0 and i < m) and not(i == 0 and j == 0) and not(i == m - 1 and j == n - 1) and (j >= 0 and j < n):  
                if (i, j) not in obstaculos:
                    obstaculos.append((i, j))

    return obstaculos

# Matriz inicial sem objetos
matriz = []
for i in range(m):
    linha = []
    for j in range(n):
        if (i, j) == (0, 0):
            linha.append("Dogo")
        elif (i, j) == (m-1, n-1):
            linha.append("Racao")
        else:
            coordenada = f'({i}, {j})'
            linha.append(coordenada)
    matriz.append(linha)

imprimir_matriz(m, n, matriz)

qt_obstaculos = int(input("Insira a quantidade de obstaculos: "))
obstaculos = []
objetos = []
for i in range(qt_obstaculos):
    coordenada = input("Digite as coordenadas (separadas por vírgula): ")
    x, y = map(int, coordenada.split(','))
    obstaculos = regiao_proibida(x, y, obstaculos, matriz, m, n)
    objetos.append((x, y))

print(obstaculos)
# Matriz com obstaculos
for i in range(m):
    linha = []
    for j in range(n):
        if (i, j) in objetos:
            matriz[i][j] = "Objeto"
        elif (i, j) in obstaculos:
            matriz[i][j] = "X"

imprimir_matriz(m, n, matriz)

dogoLinha = 0
dogoColuna = 0

while True:
    dogo = Estado((dogoLinha, dogoColuna), obstaculos, 0, m, n)
    print()
    print("-----------------------------------------------")
    print("Teclas de funcionamento")
    print("w --> ir pra cima")
    print("a --> ir para esquerda")
    print("s --> ir para baixo")
    print("d --> ir para direita")
    print("r --> resolver o jogo, se possivel")
    print("-----------------------------------------------")
    linhaAnterior = dogoLinha
    colunaAnterior = dogoColuna
    entrada = input()
    if entrada == "s" and dogoLinha + 1 < m:
        dogoLinha += 1
    elif entrada == "a" and dogoColuna - 1 >= 0:
        dogoColuna -= 1
    elif entrada == "w" and dogoLinha - 1 >= 0:
        dogoLinha -= 1       
    elif entrada == "d" and dogoColuna + 1 < n:
        dogoColuna += 1
        
    elif entrada == "r":
        resultado = buscaInformada(dogo)
        if resultado == -1:
            print("Nao e possivel chegar na racao")
            break
        else:
            rota = resultado.caminho_perdido()
            linhaAnt = 0
            colunaAnt = 0
            for item in rota:
                matriz[linhaAnt][colunaAnt] = f'({linhaAnt}, {colunaAnt})'  
                matriz[item.linha][item.coluna] = "Dogo"
                linhaAnt = item.linha
                colunaAnt = item.coluna
                imprimir_matriz(m, n, matriz)
                print()
            break
    
    matriz[linhaAnterior][colunaAnterior] = f'({linhaAnterior}, {colunaAnterior})'   
    matriz[dogoLinha][dogoColuna] = "Dogo"

    if dogoLinha == m - 1 and dogoColuna == n - 1:
        print("Chegou na racao")
        break
    if (dogoLinha, dogoColuna) in obstaculos:
        print("Dogo ficou com medo e morreu")
        break
    
    imprimir_matriz(m, n, matriz)
    print()