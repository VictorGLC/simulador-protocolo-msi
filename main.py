import argparse

# class MemoriaPrincipal:
#     def __init__(self):
#         pass

class CacheCompartilhada:
    def __init__(self, tamanho_linha: int, num_linhas: int):
        self.cache = [None] * num_linhas
        self.tamanho_linha = tamanho_linha
        
class CachePrivada:
    def __init__(self, tamanho_linha: int, num_linhas: int):
        self.tamanho_linha = tamanho_linha
        self.cache_instrucao = [None] * (num_linhas // 2)
        self.cache_dados = [None] * (num_linhas // 2)
        self.id = id

    def seleciona_instrucao(self, instrucao: int, endereco: str):
        match instrucao:
            case 0:
                pass
            case 2:
                pass
            case 3:
                pass
            case _:
                raise ValueError("Instrução inválida")

    def leitura_instrucao(endereco)

def le_configuracoes(arq_config):
    tam_linhas_cache = int(arq_config.readline().strip())
    num_linhas_cache_compartilhada = int(arq_config.readline().strip())
    num_linhas_cache_privada = int(arq_config.readline().strip())
    num_processadores = int(arq_config.readline().strip())
    politica = arq_config.readline().strip()
    arq_config.close()
    
    return tam_linhas_cache, num_linhas_cache_compartilhada, num_linhas_cache_privada, num_processadores, politica

def trata_instrucoes(arq_instrucoes):
    instrucoes_lst = []
    for linha in instrucoes:
        partes = linha.strip().split()
        id_processador = int(partes[0])
        operacao = int(partes[1])
        endereco = partes[2]
        instrucoes_lst.append((id_processador, operacao, endereco))
    instrucoes.close()
    return instrucoes_lst

def protocolo_msi(instrucoes: list[tuple(int, int, str)], caches_privadas: list[CachePrivada], cache_compartilhada: CacheCompartilhada):
    for instrucao in instrucoes:
        id, operacao, endereco = instrucao
        cache_privada = caches_privadas[id]
        match operacao:
            case 0:
                pass

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-arquivo', dest='arq_entrada', help='nome do arquivo de entrada')
        parser.add_argument('-config', dest='arq_config', help='nome do arquivo de configuração')
        args = parser.parse_args()
        arquivo_entrada = args.arq_entrada
        arquivo_config = args.arq_config

        instrucoes = open(arquivo_entrada, 'r')
        instrucoes_lst = trata_instrucoes(instrucoes)

        try:
            configuracoes = open(arquivo_config, 'r')
            tam_linhas_cache, num_linhas_cache_compartilhada, num_linhas_cache_privada, num_processadores, politica = le_configuracoes(configuracoes)
        except FileNotFoundError:
            print("Arquivo de configuração não encontrado.")
            return

    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")
        return

if __name__ == "__main__":
    main()