import automato
import leitura

def lerArquivo(nomeArquivo):
    with open(nomeArquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        vetor = [linhas[1].strip()]
        vetor.extend(linhas[2].strip().split())
        return vetor

def menu():
    print("Menu:")
    print("0 - Sair")
    print("1 - Converter AFND para AFD")
    print("2 - Ler palavras e verificar aceitação no AFD")
    print("3 - Converter AFND para AFD e verificar palavras")
    return input("Escolha uma opção: ")

def main():
    nomeArquivo = "input/automato.txt"
    estadosIniciaisFinais = lerArquivo(nomeArquivo)

    with open(nomeArquivo, 'r') as arquivo:
        primeiraLinha = arquivo.readline().strip().split()
    estados = primeiraLinha

    estadosDict = {}
    for estadoNome in estados:
        estadosDict[estadoNome] = automato.Automato(estadoNome)

    transicoes = []
    linhaInicial = 4

    with open(nomeArquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        if 1 <= linhaInicial <= len(linhas):
            for estadoOrigem in estados:
                for estadoDestino in estados:
                    for linha in linhas[linhaInicial - 1:]:
                        trans = linha.strip().split()
                        if trans[0] == estadoDestino:
                            estadosDict[estadoDestino].adicionaTransicao(
                                trans[1], estadosDict[trans[2]])

    while True:
        escolha = menu()
        if escolha == '0':
            print("Encerrando o programa...")
            break
        elif escolha == '1':
            AFD = automato.converterAfndParaAfd(estadosDict[estados[0]])
            print("Feito")
            automato.preenche(AFD, estadosIniciaisFinais)
        elif escolha == '2':
            entrada = "input/palavras.txt"
            saida = "output/saidaPalavra.txt"
            leitura.funcs(entrada, AFD, estadosIniciaisFinais[1:])
        elif escolha == '3':
            AFD = automato.converterAfndParaAfd(estadosDict[estados[0]])
            print("Feito")
            automato.preenche(AFD, estadosIniciaisFinais)
            entrada = "input/palavras.txt"
            saida = "output/saidaPalavra.txt"
            leitura.funcs(entrada, AFD, estadosIniciaisFinais[1:])
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()
