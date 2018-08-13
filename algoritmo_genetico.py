from random import random


class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor


class Individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.geracao = geracao
        self.nota_avaliacao = 0
        self.espaco_utilizado = 0
        self.cromossomo = []

        for i in range(len(espacos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")

    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                soma_espacos += self.espacos[i]

        if soma_espacos > self.limite_espacos:
            nota = 1

        self.nota_avaliacao = nota
        self.espaco_utilizado = soma_espacos

    def crossover(self, outro_indivio):
        corte = round(random() * len(self.cromossomo))

        filho1 = outro_indivio.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_indivio.cromossomo[corte::]

        filhos = [
            Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
            Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
        ]

        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2

        return filhos

    def mutacao(self, taxa):
        for i in range(len(self.cromossomo)):
            if random() < taxa:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'

        return self


class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0

    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))

        self.melhor_solucao = self.populacao[0]


    def ordena_populacao(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.nota_avaliacao, reverse=True)

    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao

        return soma

    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sortado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sortado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1

        return pai

    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print('Geracao %s -> Valor: %s Espaco: %s Cromossomo: %s' % (melhor.geracao, melhor.nota_avaliacao, melhor.espaco_utilizado, melhor.cromossomo))

    def avaliar_populacao(self):
        for individuo in self.populacao:
            individuo.avaliacao()

    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        self.inicializa_populacao(espacos, valores, limite_espacos)

        self.avaliar_populacao()

        self.ordena_populacao()

        self.visualiza_geracao()

        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []

            for individuos_gerados in range(0, ag.tamanho_populacao, 2):
                pai = self.seleciona_pai(soma_avaliacao)
                mae = self.seleciona_pai(soma_avaliacao)
                filhos = self.populacao[pai].crossover(self.populacao[mae])

                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            self.populacao = list(nova_populacao)
            self.avaliar_populacao()
            self.ordena_populacao()
            self.visualiza_geracao()
            melhor = self.populacao[0]
            self.melhor_individuo(melhor)

        print("\nMelhor solução -> G: %s Valor: %s Espaço: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_utilizado,
               self.melhor_solucao.cromossomo))

        return self.melhor_solucao.cromossomo


if __name__ == '__main__':
    lista_produtos = [
        Produto("Geladeira Dako", 0.751, 999.90), Produto("Iphone 6", 0.0000899, 2911.12),
        Produto("TV 55' ", 0.400, 4346.99), Produto("TV 50' ", 0.290, 3999.90),
        Produto("TV 42' ", 0.200, 2999.00), Produto("Notebook Dell", 0.00350, 2499.90),
        Produto("Ventilador Panasonic", 0.496, 199.90), Produto("Microondas Electrolux", 0.0424, 308.66),
        Produto("Microondas LG", 0.0544, 429.90), Produto("Microondas Panasonic", 0.0319, 299.29),
        Produto("Geladeira Brastemp", 0.635, 849.00), Produto("Geladeira Consul", 0.870, 1199.89),
        Produto("Notebook Lenovo", 0.498, 1999.90), Produto("Notebook Asus", 0.527, 3999.00)
    ]

    espacos = []
    valores = []
    nomes = []

    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 3
    tamanho_populacao = 20
    taxa_mutacao = 0.01
    numero_geracoes = 100

    ag = AlgoritmoGenetico(tamanho_populacao)
    ag.inicializa_populacao(espacos, valores, limite)

    for individuo in ag.populacao:
        individuo.avaliacao()

    ag.ordena_populacao()
    ag.melhor_individuo(ag.populacao[0])
    soma = ag.soma_avaliacoes()
    nova_populacao = []
    probabilidade_mutacao = 0.01
    for individuos_gerados in range(0, ag.tamanho_populacao, 2):
        pai = ag.seleciona_pai(soma)
        mae = ag.seleciona_pai(soma)
        filhos = ag.populacao[pai].crossover(ag.populacao[mae])

        nova_populacao.append(filhos[0].mutacao(probabilidade_mutacao))
        nova_populacao.append(filhos[1].mutacao(probabilidade_mutacao))

    ag.populacao = list(nova_populacao)
    for individuo in ag.populacao:
        individuo.avaliacao()

    ag.ordena_populacao()
    ag.melhor_individuo(ag.populacao[0])
    soma = ag.soma_avaliacoes()
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                       lista_produtos[i].valor))

