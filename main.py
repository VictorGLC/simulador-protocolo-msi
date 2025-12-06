import argparse

# class MemoriaPrincipal:
#     def __init__(self):
#         pass

class CacheCompartilhada:
    def __init__(self, tamanho_linha: int, num_linhas: int):
        self.cache = [None] * num_linhas
        self.tamanho_linha = tamanho_linha
        
class CachePrivada:
    def __init__(self, id: int, tamanho_linha: int, num_linhas: int):
        self.tamanho_linha = tamanho_linha
        self.cache_instrucao = [(None, "I")] * (num_linhas)
        self.cache_dados = [(None, "I")] * (num_linhas)
        self.id = id

def le_configuracoes(arq_config):    
    tam_linha = int(arq_config.readline().strip())
    n_linhas_cache_compartilhada = int(arq_config.readline().strip())
    n_linhas_cache_privada = int(arq_config.readline().strip())
    n_processadores = int(arq_config.readline().strip())
    politica = arq_config.readline().strip()
    
    return (tam_linha, n_linhas_cache_compartilhada, n_linhas_cache_privada, n_processadores, politica)

def trata_instrucoes(arq_instrucoes):
    instrucoes_lst = []
    for linha in arq_instrucoes:
        partes = linha.strip().split()
        id_processador = int(partes[0])
        operacao = int(partes[1])
        endereco = partes[2]
        instrucoes_lst.append((id_processador, operacao, endereco))
    arq_instrucoes.close()
    return instrucoes_lst

def imprimirCaches(caches_privadas: list[CachePrivada], cache_compartilhada: CacheCompartilhada):
    print("="* 6, "Caches Privadas", "="*6)
    for cache_privada in caches_privadas:
        print(f"\nProcessador {cache_privada.id}:")
        print("-"*5, "Instruções", "-"*5)
        print("\tBloco\tEstado")

        for i in range(len(cache_privada.cache_instrucao)):
            print(f"Linha {i}: {cache_privada.cache_instrucao[i][0]}\t{cache_privada.cache_instrucao[i][1]}")
        print("-"*5, "Dados", "-"*5)
        print("\tBloco\tEstado")

        for i in range(len(cache_privada.cache_dados)):
            print(f"Linha {i} {cache_privada.cache_dados[i][0]}\t{cache_privada.cache_dados[i][1]}")
            
    print("\nCache Compartilhada:")
    for i in range(len(cache_compartilhada.cache)):
        print(f"Linha {i}: {cache_compartilhada.cache[i]}")

def protocolo_msi(instrucoes: list[tuple], caches_privadas: list[CachePrivada], cache_compartilhada: CacheCompartilhada):
    for instrucao in instrucoes:
        id, operacao, endereco = instrucao
        print(f"\nOperação: {id}, {operacao}, {endereco}")
        match operacao:
            case 0:
                print("Leitura de instrução\n")
            case 2:
                print("Leitura de dado\n")
            case 3:
                print("Escrita de dado\n")
            case _:
                raise ValueError("Instrução inválida")
        imprimirCaches(caches_privadas, cache_compartilhada)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-arquivo', help='nome do arquivo de configuração')
    parser.add_argument('-config', help='nome do arquivo de entrada')
    args = parser.parse_args()

    try:
        with open(args.config, 'r') as f:
            (tam_linha, n_linhas_cache_compartilhada, n_linhas_cache_privada, n_processadores, politica) = le_configuracoes(f)
            
            print("Configurações Lidas:")
            print(f"Mapeamento: Associativo")
            print(f"Tamanho linha: {tam_linha}")
            print(f"L2: {n_linhas_cache_compartilhada} linhas")
            print(f"L1: {n_linhas_cache_privada} linhas")
            print(f"Número de processadores: {n_processadores}")
            print(f"Política de substituição: {politica}")
            
    except FileNotFoundError:
        print(f"Erro: Arquivo {args.config} não encontrado.")
        return

    # inicializa caches
    cache_compartilhada = CacheCompartilhada(tam_linha, n_linhas_cache_compartilhada)
    caches_privadas = [CachePrivada(i, tam_linha, n_linhas_cache_privada) for i in range(n_processadores)]

    # le instrucoes
    try:
        with open(args.arquivo, 'r') as f:
            lista_instrucoes = trata_instrucoes(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {args.arquivo} não encontrado.")
        return

    # executa o simulador
    protocolo_msi(lista_instrucoes, caches_privadas, cache_compartilhada)

if __name__ == "__main__":
    main()