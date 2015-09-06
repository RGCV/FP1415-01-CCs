# 81045 - Rui Ventura

##
## Definicao de constantes
##

# Informacao sobre os cartoes de credito compilada em tuplos (estilo tabela, o
# indice mais externo corresponde a uma linha, o seguinte a uma coluna. Certas
# colunas tem mais "linhas", embora sejam da mesma categoria, havendo entao uma
# terceira seccao no interior da coluna)
T_INFO_CARTOES = (
    ## Exemplo generico
    #('Abreviatura',
    # 'Rede Emissora',
    # ('prefixo-1','prefixo-2',...,'prefixo-n'),
    # (comp-1, comp-2,...,comp-n)),
    
    ## American Express
    ('AE',
     'American Express',
     ('34', '37'),
     (15,)),
    
    ## Diners Club International
    ('DCI',
     'Diners Club International',
     ('309', '36', '38', '39'),
     (14,)),
    
    ## Discover Card
    ('DC',
     'Discover Card',
     ('65',),
     (16,)),
    
    ## Maestro
    ('M',
     'Maestro',
     ('5018', '5020', '5038'),
     (13, 19)),
    
    ## Master Card
    ('MC',
     'Master Card',
     ('19', '50', '51', '52', '53', '54'),
     (16,)),
    
    ## Visa Electron
    ('VE',
     'Visa Electron',
     ('4026', '426', '4405', '4508'),
     (16,)),
    
    ## Visa
    ('V',
     'Visa',
     ('4024', '4532', '4556'),
     (13, 16))
)

# Dependendo do digito inicial, este menos 1 sera o indice para cada uma das
# categorias. Por ex.: Digito inicial = 1 => indice = 0
T_CATEGORIAS = (
    'Companhias aereas',
    'Companhias aereas e outras atribuicoes futuras da industria',
    'Viagens e entretenimento e bancario / financeiro',
    'Servicos bancarios e financeiros',
    'Servicos bancarios e financeiros',
    'Merchandising e bancario / financeiro',
    'Petroleo e outras atribuicoes futuras da industria',
    'Saude, telecomunicacoes e outras atribuicoes futuras da industria',
    'Atribuicao nacional'
    )

# Indices dos diferentes tipos de informacao
INT_ABREVIATURA   = 0
INT_REDE_EMISSORA = 1
INT_DIGITOS_IIN   = 2
INT_COMPRIMENTO   = 3

##
## Funcoes auxiliares
##

def calc_soma(str_cad):
    """ Executa as instrucoes 2 - 4 (sem digito de verificacao) do Algoritmo de Luhn sobre str_cad
    Recebe: (String) 'Numero de CC (sem verificacao)' str_cad
    Devolve: (Int) 'Soma do Numero Processado' int_soma"""
    str_num_cc_inverso = ''
    
    for char_digito in str_cad:
        str_num_cc_inverso = char_digito + str_num_cc_inverso
    
    int_soma = 0
    for i in range(len(str_num_cc_inverso)):
        int_num = eval(str_num_cc_inverso[i])
        
        if i % 2 == 0:
            int_num = int_num * 2
            if int_num > 9:
                int_num = int_num - 9
        int_soma = int_soma + int_num
    return int_soma

def luhn_verifica(str_cad):
    """ Verifica se o numero passa o algoritmo de Luhn
    Recebe: (String) 'Numero de CC' str_cad
    Devolve: (Bool) """
    str_num_ver = eval(str_cad) % 10
    str_num_cc_sem_ver = eval(str_cad) // 10
    return (calc_soma(str(str_num_cc_sem_ver)) + str_num_ver) % 10 == 0

def comeca_por(str_cad1, str_cad2):
    """ Verificar se str_cad1 se inicia por str_cad2
    Recebe: (String) 'Numero de CC' str_cad1;
            (String) 'Digitos Iniciais' str_cad2
    Devolve: (Bool)"""
    int_diferenca = len(str_cad1) - len(str_cad2)
    
    # Ao dividir por 10 ** diferenca entre comprimentos, vai reduzir a cadeia a
    # comparar ao comprimento da cadeia a qual esta a ser comparada
    return str(eval(str_cad1) // (10 ** int_diferenca)) == str_cad2

def comeca_por_um(str_cad, t_cads):
    """ Verificar se str_cad se inicia por alguma das cadeias em t_cads
    Recebe: (String) 'Numero de CC' str_cad
    Devolve: (Bool) """
    for c in t_cads:
        if comeca_por(str_cad, c):
            return True
    return False

def valida_iin(str_cad):
    """ Verifica o numero correspondente a str_cad, validando os digitos iin e o seu comprimento
    Recebe: (String) 'Numero de CC' str_cad
    Devolve: (String) 'Rede Emissora' """
    int_len_cad = len(str_cad)
    bool_digitos_iin, bool_comp_cad = False, False
    
    # Procura pelo tuplo com a informacao sobre a rede emissora correspondente aos digitos iin
    for t_info_cc in T_INFO_CARTOES:
        # Verifica os, se tal, varios prefixos. 
        for iin in t_info_cc[INT_DIGITOS_IIN]:
            if (not isinstance(iin, str) and comeca_por_um(str_cad, iin)) \
                or comeca_por(str_cad, iin):
                bool_digitos_iin = True
                # Semelhante aos prefixos, agora com o comprimento
                for comp in t_info_cc[INT_COMPRIMENTO]:
                    if int_len_cad == comp:
                        bool_comp_cad = True
            if bool_digitos_iin and bool_comp_cad:
                return t_info_cc[INT_REDE_EMISSORA]
    return ''

def categoria(str_cad):
    """ Devolve a categoria do cartao com o numero correspondente a str_cad
    Recebe: (String) 'Numero de CC' str_cad
    Devolve: (String) 'Categoria do CC' """
    # Obtém o digito mais significativo dividindo (div. inteira) o inteiro por
    # 10 elevado ao comprimento da cadeia menos 1
    return T_CATEGORIAS[eval(str_cad) // 10 ** (len(str_cad) - 1) - 1]

def digito_verificacao(str_cad):
    """ Calcula o digito de verificacao do numero do cartao
    Recebe: (String) 'Numero de CC' str_cad
    Devolve: (String) 'Digito de Verificacao' """
    # Complementa a soma com o digito que tornara a soma final num multiplo de 10
    int_digito_ver = (10 - (calc_soma(str_cad) % 10))
    if int_digito_ver != 10:
        return str(int_digito_ver % 10)
    return '0'

##
## Funcoes principais
##

from random import random

def verifica_cc(int_num_cc):
    """ Verifica se num_cc e um numero valido de cartao de credito
    Recebe: (Int) 'Numero de CC' int_num_cc
    Devolve: (Tuplo) 'Categoria e Rede Emissora' ou (String) 'Invalido' """
    str_num_cc = str(int_num_cc)
    if luhn_verifica(str_num_cc) and valida_iin(str_num_cc) != '':
        return (categoria(str_num_cc), valida_iin(str_num_cc))
    return 'cartao invalido'

def gera_num_cc(str_abrev_cc):
    """ Gera um numero de cc aleatoriamente com base na abreviatura dada
    Recebe: (String) 'Abreviatura da Rede' str_abrev_cc
    Devolve: (Int) 'Numero de CC' """
    t_info_cc = ()
    
    # Escolhera, se encontrar, o tuplo com a rede correspondente a abreviatura
    for i in range(len(T_INFO_CARTOES)):
        if str_abrev_cc == T_INFO_CARTOES[i][INT_ABREVIATURA]:
            t_info_cc = T_INFO_CARTOES[i]
    if len(t_info_cc) == 0:
        return 'Abreviatura invalida'
    
    # Escolher um dos prefixos aleatoriamente com base nos que existem, se forem
    # mais que um
    int_len_iin = len(t_info_cc[INT_DIGITOS_IIN])
    str_iin_cc = t_info_cc[INT_DIGITOS_IIN][int(int_len_iin * random())]
    
    # O mesmo com os comprimentos
    int_len_comps = len(t_info_cc[INT_COMPRIMENTO])
    int_comp_cc = t_info_cc[INT_COMPRIMENTO][int(int_len_comps * random())]
    
    str_num_cc = str(str_iin_cc)
    int_comp_cc = int_comp_cc - (len(str_iin_cc) + 1)
    
    for n in range(int_comp_cc):
        str_num_cc = str_num_cc + str(int(10 * random()))
    
    return int(str_num_cc + digito_verificacao(str_num_cc))