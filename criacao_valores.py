import pandas as pd
import random
import numpy as np

class cria_valores:
    
    # --------------------------------------------------------------------------------------------------------------------- #
    # Função: parametros
    #
    # Descrição: Encontra Outliers em cada atributo do dataset, calcula média, desvio padrão e verifica o quanto eles tomam conta do dataset\
    #            Se forem maior que a porcentagem aceitável passado, o calculo da média e do desvio padrão é realizado sem os outliers\
    #            Se forem menor que a porcentagem aceitavel passado, o calculo da média e do desvio padrãoe é realizado com os outliers\
    #            Retorna dataframe com as colunas do df inical, em valores e suas respectivas médias, desvios padrões, máximos e mínimos
    #
    # Parâmetros: 1) dataframe = dataframe com dados formatados pela tipagem e por indicadores
    #             2) porc_aceitavel = porcentagem do dataframe que será analisado para escolher se as métricas serão calculadas com ou sem eles
    #
    # Quem procurar: Otávio Augusto Iasbeck
    # -------------------------------------------------------------------------------------------------------------------------- #
    def parametros(df, porc_aceitavel):
        
        '''
        Parametros: df = Seu dataset,
                    porc_aceitavel = Quantos porcento da base pode possuir outliers?,
                    
        '''
        
        ## Explicita listas para utilização no decorrer do código
        df_temp = df.copy()
        media = []
        desvio_padrao = []
        maior_valor = []
        menor_valor = []
        coluna = []

        
        
        ## Percorro as colunas
        for col in df_temp.columns:
            q1 = df_temp[col].quantile(0.25) ## Pego o primeiro quartil
            q3 = df_temp[col].quantile(0.75) ## Pego o terceiro quartil
            medida_inter_quartil = q3-q1 ## Acho o intervalo entre os quartis

            ## Crio os limites
            limite_sup = (q1 - (1.8 * medida_inter_quartil))
            limite_inf = (q1 + (1.8 * medida_inter_quartil))

            ## Acho tudo que está fora desse limite
            outliers = df_temp[(df_temp[col] < limite_sup) | (df_temp[col] > limite_inf)]

            proporcao_coluna = ((len(outliers)/len(df_temp[col])) * 100)

            ## Verifico se a quantidade de outliers para/com a base está maior que o valor aceitável, passado como parâmetro
            if int(proporcao_coluna) > porc_aceitavel:
                ## Nego a condição que tu que for diferente de estar fora dos limites, ou seja, que está dentro do limite
                media.append(df_temp[~((df_temp[col] < limite_sup)) | (df_temp[col] > limite_inf)][col].mean())
                ## Faço a mesma coisa para calcular o desvio padrão
                desvio_padrao.append(df_temp[~((df_temp[col] < limite_sup)) | (df_temp[col] > limite_inf)][col].std())
                ## Pego a coluna que está no loop
                coluna.append(col)
                ## Pego o maior valor da coluna que está no loop
                maior_valor.append(df_temp[col].max())
                ## Pego o menor valor que está no loop
                menor_valor.append(df_temp[col].min())
                print(f"O calculo da coluna {col} foi realizado SEM os outliers, pelo fato da quantidade de outliers ser maior que a permitida, de acordo com a regra passada!")

            ## Se a quantidade de outliers para/com a base está dentro do aceitável
            else:
                ## Pego a média da coluna
                media.append(df_temp[col].mean())
                ## Pego o desvio padrão da coluna
                desvio_padrao.append(df_temp[col].std())
                ## Pego a coluna que está no loop
                coluna.append(col)
                ## Pego o maior valor da coluna que está no loop
                maior_valor.append(df_temp[col].max())
                ## Pego o menor valor da coluna que está no loop
                menor_valor.append(df_temp[col].min())
                print(f"O calculo da coluna {col} foi realizado COM os outliers, pelo fato da quantidade de outliers ser menor ou igual que a permitida, de acordo com a regra passada!")
                
        ## Aloco os valores todos em dataframe e o retorno
        df_return = pd.DataFrame(index = None, data = {'atributos': coluna, 'media': media, 'desvio_padrao': desvio_padrao, 'max': maior_valor, 'min': menor_valor} 
        )
                
        return df_return
    
    
    # --------------------------------------------------------------------------------------------------------------------- #
    # Função: calculo_valores
    #
    # Descrição: Responsável por realizar o calculo que cria valores baseados em suas médias e desvios padrões\
    #            Chama a função de outliers acima para pegar as médias e desvios necessários de cada coluna do dataframe\
    #            Retorna dataframe com novos dados ;D   
    #
    # Parâmetros: 1) dataframe = dataframe com dados formatados pela tipagem e por indicadores
    #             2) porc_aceitavel = porcentagem do dataframe que será analisado para escolher se as métricas serão calculadas com ou sem eles
    #             3) qtd = Quantidade de dados que você quer criar
    #
    # Quem procurar: Otávio Augusto Iasbeck
    # -------------------------------------------------------------------------------------------------------------------------- #
    def calculo_valores(df, porc_aceitavel, qtd = 15):
        
        '''
        Parametros: df = Seu dataset,
                    porc_aceitavel = Qual porcentagem da base pode possuir outliers?,
                    qtd = Quantidade de valores a serem criados
                    
        '''
        
        ## Explicito o dicionário que será usado para armazenar os dados
        dic_novos_valores = {}
        
        ## Chamo a função acima
        df_return = cria_valores.parametros(df, porc_aceitavel)
        
        print("Realizando calculos...")
        ## Percorro a coluna de atributos (que estão alocados as colunas como valores)
        for coluna in df_return['atributos']:
            novos_valores = []
            aux = 0
            
            ## Se a quantidade de valores passado como parâmetro for negativo ou igual a zero executo erro
            if qtd <= 0:
                raise Exception(f"A quantidade de valores gerados não pode ser menor que 0!, o parâmetro passado foi: {qtd}")

                
            else:
                ## Enquanto menor que a quantidade passada
                while aux < qtd:
                    
                    ## Cria peso aleatório para o calculo
                    peso_aleatorio = random.uniform(-1, 1)
                    
                    ## Calculo criado por mim, baseado em: Vozes da minha cabeça (calculo = media + (desvio_padrao * peso_aleatorio))
                    calculo = np.around(((df_return[df_return['atributos'] == coluna]['media'] + (df_return[df_return['atributos'] == coluna]['desvio_padrao'] * peso_aleatorio)).iloc[0]), 4)
                    
                    ## Se o valor calculado for maior que o maior valor da coluna do dataframe, ou se for menor que o menor valor do dataframe, ignora o loop
                    if (calculo > df_return[df_return['atributos'] == coluna]['max'].iloc[0]) or (calculo < df_return[df_return['atributos'] == coluna]['min'].iloc[0]):
                        aux = aux + 0 
                
                    else:
                        aux = aux + 1
                        novos_valores.append(calculo)
                
            ## Aloco em dicionário (que está dentro do primeiro loop)
            dic_novos_valores[coluna] = novos_valores
            
        print("Dados criados!")
        ## Passo o dicionário para dataframe :D
        novos_valores = pd.DataFrame(dic_novos_valores)
            
        return df_return, novos_valores