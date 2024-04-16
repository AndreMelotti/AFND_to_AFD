#Função recursiva
def recogWord(AFD, transc, s_automato, i, automato_f):
    # Se já percrremos toda a palavra
    if len(transc) <= i:
        # verificamos se estamos em um estado final do autômato
        for est in automato_f:
            for _est in s_automato:
                # se estamos em um estado final, retornamos Verdadeiro.
                if est == _est.name:
                    return True
        # se não estamos em um estado final, retornamos Falso.
        return False
    
    #Se não percorremos a palavra inteira
    else:
        # percorremos todas as transições do autômato.
        for _trans in AFD:
            # Se a transição atual corresponde ao estado atual e à entrada atual
            if _trans[0] == s_automato and _trans[1] == transc[i]:
                # verificamos se há transições para continuar o processo
                if len(_trans[2]) > 0:
                    # se houver, avançamos para o próximo passo recursivamente
                    return recogWord(AFD, transc, _trans[2], i+1, automato_f)
                else:
                    # se não houver mais transições, a palavra não é reconhecida.
                    return False


# arquivo de saída
saida = "output/saidaPalavra.txt"

# função para processar o texto e verificar se as palavras são aceitas pelo autômato
def funcs(texto, AFD, automato_f):
    # lista para armazenar os resultados de cada palavra
    resultados = []
    # lista para armazenar as palavras do texto
    palavras = []
    
    # abrir o arquivo de texto em modo de leitura
    with open(texto, 'r') as arquivo:

        for linha in arquivo:
            # adicionar a palavra à lista de palavras, rmovendo espaços em branco no início e no final
            palavras.append(linha.strip())
            # inicializar uma lista vazia para armazenar os caracteres da linha atual.
            vetor = []
            # remover espaços em branco no início e no final da linha.
            linha = linha.strip()
            # estender a lista "vetor" com os caracteres da linha atual.
            vetor.extend(list(linha))
            # Chamar a função "recogWord" para verificar se a palavra é aceita pelo autômato e armazenar o resultado na lista "resultados"
            resultados.append(recogWord(AFD, vetor, AFD[0][0], 0, automato_f))

    # abrir o arquivo de saída em modo de escrita
    with open(saida, 'w') as arquivo_saida:
        # para cada índice na lista de palavras
        for i in range(len(palavras)):
            # verificar se a palavra correspondente foi aceita ou rejeitada e escrever no arquivo de saida.
            if resultados[i]:
                arquivo_saida.write(palavras[i] + " aceita\n")
            else:
                arquivo_saida.write(palavras[i] + " rejeita\n")
