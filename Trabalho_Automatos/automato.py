# automato.py
class Automato:
    def __init__(self, name):
        self.name = name
        self.transicoes = [['1'], ['0'], ['e']]

    def __repr__(self):
        return f"{self.name}"

    def transPorVazios(self):
        vazio = []
        calcularVazios(self, vazio)
        for est in vazio:
            for _est in est.transicoes:
                if _est[0] != 'e':
                    for esta in self.transicoes:
                        if esta[0] == _est[0]:
                            for __est in _est[1:]:
                                if __est not in esta:
                                    esta.append(__est)

    def adicionaTransicao(self, transicao, automato):
        for row in self.transicoes:
            if row[0] == transicao:
                calcularVazios(automato, row)
                if automato not in row:
                    row.append(automato)

        self.transPorVazios()


def calcularVazios(automato: Automato, linha):
    # Para cada transição no autômato
    for transicao in automato.transicoes:
        # se a transição for uma transição vazia
        if transicao[0] == 'e':
            # para cada estado alcançável pela transição vazia
            for estado in transicao[1:]:
                # Se o estado não estiver na linha atual
                if estado not in linha:
                    # adiciona o estado na linha atual
                    linha.append(estado)
                    # calcula os estados vazio a partir deste novo estado
                    calcularVazios(estado, linha)


def converterParaAfd(automato: list[Automato], transicao, transicoesAfd, afd):
    novoAfd = []  # lista para armazenar o novo AFD
    transicoes = []  # lista para armazenar as transições encontradas

    novoAfd.append(automato)  # Adiciona o autômato atual ao novo AFD

    # para cada estado no autômato atual
    for estado in automato:
        # para cada transição no estado
        for linha in estado.transicoes:
            # Se a transição iniciar com o símbolo de transição atual
            if linha[0] == transicao:
                # Para cada estado alcançável pela transição
                for transicaoDestino in linha[1:]:
                    # se o estado ainda não foi registrado nas transições
                    if transicaoDestino not in transicoes:
                        # adiciona o estado às transições
                        transicoes.append(transicaoDestino)

    # Se houver estados alcançáveis pela transição
    if len(novoAfd[0]) > 0:
        # Adiciona o símbolo de transição ao novo AFD
        novoAfd.append(transicao)

    # Adiciona as transições encontradas ao novo AFD
    novoAfd.append(transicoes)

    # Se houver estados no novo AFD
    if len(novoAfd[0]) > 0:
        # Adiciona o novo AFD à lista de AFDs
        afd.append(novoAfd)

    # Se as transições encontradas não estiverem na lista de transições do AFD
    if transicoes not in transicoesAfd:
        # Adiciona as transições à lista de transições do AFD
        transicoesAfd.append(transicoes)
        # Converte os estados alcançáveis pelas transições para '1'
        converterParaAfd(transicoes, '1', transicoesAfd, afd)
        # Converte os estados alcançáveis pelas transições para '0'
        converterParaAfd(transicoes, '0', transicoesAfd, afd)


def converterAfndParaAfd(automatoInicial: Automato):
    automatosIniciais = [automatoInicial]  # Lista para armazenar os autômatos iniciais
    transicoesAfd = []  # Lista para armazenar as transições do AFD
    afd = []  # Lista para armazenar o AFD resultante

    # Para cada transição no autômato inicial
    for transicao in automatoInicial.transicoes:
        # Se a transição for uma transição vazia
        if transicao[0] == 'e':
            # Para cada estado alcançável pela transição vazia
            for estado in transicao[1:]:
                # Se o estado não estiver na lista de autômatos iniciais
                if estado not in automatosIniciais:
                    # Adiciona o estado à lista de autômatos iniciais
                    automatosIniciais.append(estado)

    # Converte os estados alcançáveis pelas transições para '1'
    converterParaAfd(automatosIniciais, '1', transicoesAfd, afd)
    # Converte os estados alcançáveis pelas transições para '0'
    converterParaAfd(automatosIniciais, '0', transicoesAfd, afd)

    return afd  # Retorna o AFD resultante

nomeArquivo = "output/saida.txt"

def preenche(AFD, inicialFinais):
    superAutomatos = []
    for n in AFD:
        if n[0] not in superAutomatos:
            superAutomatos.append(n[0])
    with open(nomeArquivo, 'w') as arquivo:
        # Escreve os superestados formatados na primeira linha
        primeiraLinha = ' '.join(set(''.join(map(str, linha[0])) for linha in AFD))
        arquivo.write(f"{primeiraLinha}\n")
        # print(f"{primeira_linha}\n")

        automatosFinais = []
        estIniciais = []
        esFinais = []
        # Itera sobre os superestados
        for n in superAutomatos:
            automatosOrigem = ''.join(([x.name for x in n]))
            # automatos_origem = ''.join(sorted([x.name for x in n]))
            # Verifica se o superestado é um estado inicial/final
            
            for x in n:
                if x.name == inicialFinais[0]:
                    # arquivo.write(f"Inicial - Q{automatos_origem}\n")  # Formata corretamente o superestado inicial
                    estIniciais.append(automatosOrigem)
                elif x.name in inicialFinais[1:] and n not in automatosFinais:
                    automatosFinais.append(n)
                    esFinais.append(automatosOrigem)
                    # arquivo.write(f"Final - Q{automatos_origem} \n")  # Formata corretamente o superestado final
        
        # mylist = list(dict.fromkeys(mylist))
        estIniciais = list(dict.fromkeys(estIniciais))
        esFinais = list(dict.fromkeys(esFinais))

        arquivo.write(f"Inicial - {estIniciais}\n")
        arquivo.write(f"Final - {esFinais}\n")

        arquivo.write("\n")
        
        arquivo.write("\n")
        # print(f"Q{automatos_origem}\n")
        # Escreve as transições no arquivo
        for linha in AFD:
            if len(linha) == 3 and len(linha[2]) > 0:
                linhaFormatada = ' '.join([''.join(map(str, sublista)) for sublista in linha])
                arquivo.write(f"{linhaFormatada}\n")
                # print(f"{linha_formatada}\n")
