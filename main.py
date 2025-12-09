import argparse
import math

# class MemoriaPrincipal:
#     def __init__(self):
#         pass

class CacheCompartilhada:
    def __init__(self, tamanho_linha: int, num_linhas: int):
        self.cache = [None] * num_linhas
        self.tamanho_linha = tamanho_linha
        self.hit = 0
        self.miss = 0

    def alocar(self, tag: str):
        """aloca uma nova tag na cache compartilhada"""

        if tag in self.cache:
            return  # já está na cache

        for i in range(len(self.cache)):
            if self.cache[i] is None:
                self.cache[i] = tag
                return

        # implementar politica de substituicao
        
class CachePrivada:
    def __init__(self, id: int, tamanho_linha: int, num_linhas: int):
        self.tamanho_linha = tamanho_linha
        self.cache_instrucao = [(None, "I") for _ in range(num_linhas)]
        self.cache_dados = [(None, "I") for _ in range(num_linhas)]
        self.hit_instrucao = 0
        self.miss_instrucao = 0
        self.hit_dados = 0
        self.miss_dados = 0
        self.id = id

    def _get_cache(self, operacao: int):
        """retorna a cache de instrucao ou de dados baseada na operação"""

        match operacao:
            case 0: # leitura de Instrução
                return self.cache_instrucao
            case 2 | 3: # operacoes de dados (leitura/escrita)
                return self.cache_dados
            case _:
                raise ValueError("Operação inválida")

    def buscar(self, operacao: int, endereco: str) -> str:
        """retorna o estado da linha se encontrar (Hit), senão retorna None (Miss)"""

        cache = self._get_cache(operacao)
        for bloco, estado in cache:
            if estado != 'I' and bloco == endereco:
                return estado # retorna 'S' ou 'M'
        return None # miss

    def atualizar_linha(self, operacao: int, tag: str, novo_estado: str):
        """insere uma nova tag ou atualiza o estado de uma existente"""

        cache = self._get_cache(operacao)
        
        # se existe apenas atualiza o estado
        for i in range(len(cache)):
            if cache[i][0] == tag:
                cache[i] = (tag, novo_estado)
                return

        # se não existe procura estado invalido
        for i in range(len(cache)):
            if cache[i][1] == 'I':
                cache[i] = (tag, novo_estado)
                return

        # implementar politica de substituicao

def calcular_tag(endereco_hex: str, tamanho_linha: int) -> str:
    """retorna a tag do endereco removendo os bits de offset baseados no tamanho da linha"""

    endereco_int = int(endereco_hex, 16)
    bits_offset = int(math.log2(tamanho_linha))
    tag = endereco_int >> bits_offset
    
    return hex(tag)[2:]

def le_configuracoes(arq_config):
    """lê as configurações do arquivo e retorna uma tupla com os valores""" 
    try:
        arq_linhas = arq_config.readlines()
        linhas = [line.strip() for line in arq_linhas if line.strip()]

        if len(linhas) < 5:
            raise ValueError(f"O arquivo deve ter 5 parâmetros. Encontrados apenas {len(linhas)}.")
        
        tam_linha = int(linhas[0])
        n_linhas_cache_compartilhada = int(linhas[1])
        n_linhas_cache_privada = int(linhas[2])
        n_processadores = int(linhas[3])
        politica = linhas[4].lower()

        if tam_linha <= 0:
            raise ValueError(f"O tamanho da linha ({tam_linha}) deve ser maior que zero.")
        if n_linhas_cache_compartilhada <= 0:
            raise ValueError(f"O número de linhas da L2 ({n_linhas_cache_compartilhada}) deve ser maior que zero.")
        if n_linhas_cache_privada <= 0:
            raise ValueError(f"O número de linhas da L1 ({n_linhas_cache_privada}) deve ser maior que zero.")
        if n_processadores <= 0:
            raise ValueError(f"O número de processadores ({n_processadores}) deve ser maior que zero.")

        if n_linhas_cache_privada >= n_linhas_cache_compartilhada:
            raise ValueError(f"Violação de Hierarquia de Memória: A L1 deve ser estritamente menor que a L2.\n")

        if politica not in ['lru', 'fifo']:
            raise ValueError(f"Aviso: Política '{politica}' desconhecida.")

        return (tam_linha, n_linhas_cache_compartilhada, n_linhas_cache_privada, n_processadores, politica)
    except Exception as e:
        raise ValueError(f"Erro inesperado na leitura do arquivo: {e}")

def trata_instrucoes(arq_instrucoes):
    """lê as instruções do arquivo e retorna uma lista de tuplas (id_processador, operacao, endereco)"""

    instrucoes_lst = []
    for linha in arq_instrucoes:
        partes = linha.strip().split()
        if len(partes) != 3:
            raise ValueError(f"Aviso: Formato inválido na linha: {linha.strip()}")
        try:
            id_processador = int(partes[0])
            operacao = int(partes[1])
            endereco = partes[2]
            instrucoes_lst.append((id_processador, operacao, endereco))
        except ValueError:
            raise ValueError(f"Aviso: Valores inválidos na linha: {linha.strip()}")
    return instrucoes_lst

def imprimirCaches(caches_privadas: list[CachePrivada], cache_compartilhada: CacheCompartilhada, arquivo_saida):
    """escreve o estado das caches no arquivo de log com formatação tabular alinhada."""
    
    # define larguras fixas para as colunas
    W_LINHA = 8
    W_BLOCO = 20
    W_ESTADO = 8

    arquivo_saida.write("\n" + "="*27 + " Cache Compartilhada " + "="*27 + "\n")
    arquivo_saida.write(f"{'Linha':<{W_LINHA}} {'Bloco':<{W_BLOCO}}\n")
    
    for i in range(len(cache_compartilhada.cache)):
        linha = cache_compartilhada.cache[i]
        bloco_str = str(linha) if linha is not None else ""
        
        arquivo_saida.write(f"{i:<{W_LINHA}} {bloco_str:<{W_BLOCO}}\n")

    arquivo_saida.write("\n" + "="*30 + " Caches Privadas " + "="*30 + "\n")
    
    for vizinho in caches_privadas:
        arquivo_saida.write(f"\n[ Processador {vizinho.id} ]\n")
        
        # instrucoes
        arquivo_saida.write(f"{'-'*10} Instruções {'-'*10}\n")
        arquivo_saida.write(f"{'Linha':<{W_LINHA}} {'Bloco':<{W_BLOCO}} {'Estado':<{W_ESTADO}}\n")
        
        for i in range(len(vizinho.cache_instrucao)):
            linha = vizinho.cache_instrucao[i][0]
            bloco_str = str(linha) if linha is not None else ""
            estado = vizinho.cache_instrucao[i][1]
            
            # formatacao da linha de dados
            arquivo_saida.write(f"{i:<{W_LINHA}} {bloco_str:<{W_BLOCO}} {estado:<{W_ESTADO}}\n")
            
        # dados 
        arquivo_saida.write(f"\n{'-'*12} Dados {'-'*13}\n")
        arquivo_saida.write(f"{'Linha':<{W_LINHA}} {'Bloco':<{W_BLOCO}} {'Estado':<{W_ESTADO}}\n")

        for i in range(len(vizinho.cache_dados)):
            linha = vizinho.cache_dados[i][0]
            bloco_str = str(linha) if linha is not None else ""
            estado = vizinho.cache_dados[i][1]
            
            arquivo_saida.write(f"{i:<{W_LINHA}} {bloco_str:<{W_BLOCO}} {estado:<{W_ESTADO}}\n")

def protocolo_msi(instrucoes: list[tuple[int, int, str]], caches_privadas: list[CachePrivada], cache_compartilhada: CacheCompartilhada, arquivo_saida):
    for instrucao in instrucoes:
        processador, operacao, endereco = instrucao

        tag = calcular_tag(endereco, caches_privadas[processador].tamanho_linha) # calcula tag do endereco

        arquivo_saida.write(f"\nOperação: {processador} {operacao} {endereco} (Bloco/Tag: {tag})\n")
        match operacao:
            case 0:
                arquivo_saida.write(f"Processador {processador} lê instrução em {endereco}\n")
                
                if caches_privadas[processador].buscar(operacao, tag) is not None: # busca na l1 de instrucao
                    caches_privadas[processador].atualizar_linha(operacao, tag, 'S') # atualiza estado para 'S'
                    caches_privadas[processador].hit_instrucao += 1
                else:
                    caches_privadas[processador].miss_instrucao += 1
                    
                    # busca direto na cache compartilhada
                    if tag in cache_compartilhada.cache:
                        cache_compartilhada.hit += 1 # hit na cache compartilhada
                    else:
                        cache_compartilhada.miss += 1 # miss na cache compartilhada
                        cache_compartilhada.alocar(tag) # insere na cache compartilhada, simula trazer da memória principal

                    caches_privadas[processador].atualizar_linha(operacao, tag, 'S') # insere na cache de instrucao
                    
            case 2:
                arquivo_saida.write(f"Processador {processador} lê dado em {endereco}\n")

                if caches_privadas[processador].buscar(operacao, tag) is not None: # busca na l1 de dados
                    caches_privadas[processador].atualizar_linha(operacao, tag, 'S')
                    caches_privadas[processador].hit_dados += 1
                else:
                    caches_privadas[processador].miss_dados += 1

                    veio_do_vizinho = False
                    for vizinho in caches_privadas:
                        if vizinho.id != processador:
                            estado = vizinho.buscar(operacao, tag) # busca na l1 de dados do vizinho
                            
                            if estado == 'M': # se for M precisa fazer write-back na l2
                                cache_compartilhada.alocar(tag) # vizinho faz write-back na l2
                                vizinho.atualizar_linha(operacao, tag, 'S') # vizinho vira shared
                                veio_do_vizinho = True
                                arquivo_saida.write(f"Snooping: Vizinho {vizinho.id} 'M' -> 'S'\n")
                    
                    # busca na cache compartilhada
                    if not veio_do_vizinho:
                        if tag in cache_compartilhada.cache:
                            cache_compartilhada.hit += 1
                        else:
                            cache_compartilhada.miss += 1
                            cache_compartilhada.alocar(tag)

                    caches_privadas[processador].atualizar_linha(operacao, tag, 'S')
            case 3:
                arquivo_saida.write(f"Processador {processador} escreve dado em {endereco}\n")

                if caches_privadas[processador].buscar(operacao, tag) is not None:
                    caches_privadas[processador].hit_dados += 1
                else:
                    caches_privadas[processador].miss_dados += 1

                # snooping (invalidate)
                for vizinho in caches_privadas:
                    if vizinho.id != processador:
                        estado_vizinho = vizinho.buscar(operacao, tag)
                        if estado_vizinho is not None:
                            if estado_vizinho == 'M': # se vizinho tinha dado modificado, precisa salvar na l2 antes de invalidar
                                cache_compartilhada.alocar(tag) # write-back na l2
                                arquivo_saida.write(f"SNOOP: Vizinho {vizinho.id} tinha 'M' -> Fez Flush antes de Invalidar\n")
                            
                            vizinho.atualizar_linha(operacao, tag, 'I') 
                            arquivo_saida.write(f"SNOOP: Invalidando cópia do processador {vizinho.id}\n")

                if caches_privadas[processador].buscar(operacao, tag) is None:
                    if tag not in cache_compartilhada.cache:
                         cache_compartilhada.miss += 1
                         cache_compartilhada.alocar(tag)
                    else:
                         cache_compartilhada.hit += 1

                caches_privadas[processador].atualizar_linha(operacao, tag, 'M')
            case _:
                raise ValueError("Instrução inválida")
        imprimirCaches(caches_privadas, cache_compartilhada, arquivo_saida)

    for cache_privada in caches_privadas:
        arquivo_saida.write(f"\n[ Processador {cache_privada.id} ]\n")
        arquivo_saida.write(f"Instrução - Hits: {cache_privada.hit_instrucao}, Misses: {cache_privada.miss_instrucao}\n")
        arquivo_saida.write(f"Dados     - Hits: {cache_privada.hit_dados}, Misses: {cache_privada.miss_dados}\n")
    
    arquivo_saida.write(f"\n[ Cache Compartilhada ]\n")
    arquivo_saida.write(f"Hits: {cache_compartilhada.hit}, Misses: {cache_compartilhada.miss}\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-arquivo', help='nome do arquivo de entrada')
    parser.add_argument('-config', help='nome do arquivo de configuração')
    parser.add_argument('-o', '--output', default='logs.txt', help='nome do arquivo de saída (log)')
    args = parser.parse_args()

    try:
        log = open(args.output, 'w', encoding='utf-8')
    except IOError as e:
        print(f"Erro ao criar arquivo de log: {e}")
        return

    try:
        with open(args.config, 'r') as f:
            (tam_linha, n_linhas_cache_compartilhada, n_linhas_vizinho, n_processadores, politica) = le_configuracoes(f)
            
            log.write("Configurações Lidas\n")
            log.write(f"Mapeamento Associativo\n")
            log.write(f"Tamanho linha: {tam_linha}\n")
            log.write(f"L2: {n_linhas_cache_compartilhada} linhas\n")
            log.write(f"L1: {n_linhas_vizinho} linhas\n")
            log.write(f"Número de processadores: {n_processadores}\n")
            log.write(f"Política de substituição: {politica}\n")
            
    except FileNotFoundError:
        print(f"Erro: Arquivo {args.config} não encontrado.")
        return

    # inicializa caches
    cache_compartilhada = CacheCompartilhada(tam_linha, n_linhas_cache_compartilhada)
    caches_privadas = [CachePrivada(i, tam_linha, n_linhas_vizinho) for i in range(n_processadores)]

    # le instrucoes
    try:
        with open(args.arquivo, 'r') as f:
            lista_instrucoes = trata_instrucoes(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {args.arquivo} não encontrado.")
        return

    # executa o simulador
    protocolo_msi(lista_instrucoes, caches_privadas, cache_compartilhada, log)

    log.close()

if __name__ == "__main__":
    main()