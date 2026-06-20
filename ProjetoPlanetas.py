import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

#
#  -- CONTROLLER(TRATAMENTO DOS DADOS)

# DEFININDO CARACTERÍSTICAS GERAIS DA TERRA COM BASE EM ESTUDOS CIENTÍFICOS DE PROFISSIONAIS DA NASA 

# CARACTERÍSTICAS DO PLANETA TERRA

DENSIDADE_DA_TERRA = 5.513

# GRAVIDADE
GRAVIDADE_DA_SUPERFICIE_DA_TERRA = 4.44   # o logaritimo da gravidade da Terra no ponto logg é aproximadamente 4.44 em cgs (centimetro por segundo ao quadrado) ou em m/s² aproximadamente 9.80665
UNIDADE_PARSEC = 3.26156

# MARGEM DE RADIAÇÃO 
MARGEM_ERRO_RADIACAO = 0.1
RADIACAO_RECEBIDA_PELA_TERRA = 1.0
LIMITE_SUPERIOR_DE_RADIACAO = RADIACAO_RECEBIDA_PELA_TERRA + MARGEM_ERRO_RADIACAO
LIMITE_INFERIOR_DE_RADIACAO = RADIACAO_RECEBIDA_PELA_TERRA - MARGEM_ERRO_RADIACAO


# MASSA
margem_massa = 0.2
MASSA_DA_TERRA = 1.0
LIMITE_INFERIOR_DA_MASSA_DA_TERRA = 0.8
LIMITE_SUPERIOR_DA_MASSA_DA_TERRA = 1.2


# CARACTERÍSTICAS GRAVITACIONAIS
margem_de_erro_gravitacional = 0.1
limite_inferior = GRAVIDADE_DA_SUPERFICIE_DA_TERRA - margem_de_erro_gravitacional
limite_superior = GRAVIDADE_DA_SUPERFICIE_DA_TERRA + margem_de_erro_gravitacional

# CARACTERÍSTICAS ESTRUTURAIS
MARGEM_DE_ERRO_RAIO = 0.35
RAIO_DA_TERRA = 1.15
LIMITE_INFERIOR_RAIO = 0.8
LIMITE_SUPERIOR_RAIO = 1.5


df = pd.read_csv(
    'TodosOsPlanetas.csv',
    sep=',',
    encoding='utf-8',
    na_values=['N/A', '-']
)

#print(df.head(10))

# SÉRIE DE FILTROS ISOLADOS QUE VERIFICAM A FUNCIONALIDADE DE CADA FILTRO APLICADO AO DATABASE

#FILTRO 2 - DISTANCIA EM ANOS LUZ
df['distancia_anos_luz'] = df['sy_dist'] * UNIDADE_PARSEC

# UTILIZAMOS UM FILTRO PARA CALCULAR O PLANETA COM A DISTANCIA MENOR QUE 200 ANOS LUZ EM RELAÇÃO A TERRA:
filtro1_distancia = df[df['distancia_anos_luz'] <= 200].sort_values(by='distancia_anos_luz', ascending=True).head(10)
print('=' * 50)
print('10 PLANETAS COM DISTÂNCIA MENOR QUE 200 ANOS LUZ DA TERRA EM ORDEM CRESCENTE:\n\n')
print(filtro1_distancia[['pl_name', 'distancia_anos_luz']])


# FILTRO 2
# FILTRAMOS OS PLANETAS QUE TEM UM LOGG DENTRO DA FAIXA DE ACEITABILIDADE
planetas_gravidade_similar = df[df['st_logg'].between(limite_inferior, limite_superior)]

print('=' * 50)
print('PLANETAS COM GRAVIDADE SIMILAR À DA TERRA:')
print(planetas_gravidade_similar[['pl_name', 'st_logg']])


# FILTRO 3 - MASSA IGUAL A DO PLANETA TERRA 
filtro3_massa = df[df['pl_bmasse'].between(LIMITE_INFERIOR_DA_MASSA_DA_TERRA, LIMITE_SUPERIOR_DA_MASSA_DA_TERRA)].sort_values(by='pl_bmasse', ascending=False)
print('=' * 50)
print("MASSA DOS PLANETAS COM MASSA PRÓXIMA A DO PLANETA TERRA:\n\n")
print(filtro3_massa[['pl_name', 'pl_bmasse']])


# FILTRO 4 - RAIOS SIMILARES AO DA TERRA
filtro4_raio = df[df['pl_rade'].between(LIMITE_INFERIOR_RAIO, LIMITE_SUPERIOR_RAIO)].sort_values(by='pl_rade')

raio_mediano = filtro4_raio['pl_rade'].median()
print(f"O raio mediano da lista dos planetas com raio similar é: {raio_mediano} (Raios Terrestres).")

planeta_mediano = filtro4_raio.iloc[(filtro4_raio['pl_rade'] - 1.0).abs().argsort()[:1]]
print('=' * 50)
print("O PLANETA COM RAIO MAIS PRÓXIMO AO DA TERRA:\n\n")
print(planeta_mediano[['pl_name', 'pl_rade']])


# VERIFICAR PLANETAS COM RADIAÇÃO SIMILAR A DA TERRA COM UMA MARGEM DE ERRO DE 0.1 PONTOS
filtro5_radiacao = df[df['pl_insol'].between(LIMITE_INFERIOR_DE_RADIACAO, LIMITE_SUPERIOR_DE_RADIACAO)].sort_values(by='pl_insol')
radiacao_media = filtro5_radiacao['pl_insol'].median()

planeta_radiacao_media = filtro5_radiacao.iloc[(filtro5_radiacao['pl_insol'] - 1.0).abs().argsort()[:1]]

print("PLANETAS COM INSOLAÇÃO/RADIAÇÃO SIMILARES A DA TERRA:\n\n")
print(planeta_radiacao_media[['pl_name', 'pl_insol']])


filtro_magnetico_real = df[
    df['pl_dens'].between(4.0, 6.5) & 
    (df['pl_rade'] <= 1.5)
].sort_values(by='pl_dens')

print("PLANETAS ROCHOSOS COM POTENCIAL CAMPO MAGNÉTICO (PRECISO):\n")
print(filtro_magnetico_real[['pl_name', 'pl_dens', 'pl_rade']])


valor_mediana = filtro_magnetico_real['pl_dens'].median()
planeta_medio_magnetico = filtro_magnetico_real.iloc[
    (filtro_magnetico_real['pl_dens'] - valor_mediana).abs().argsort()[:1]
]

print("PLANETA COM DENSIDADE MÉDIA ENCONTRADO:\n")
print(planeta_medio_magnetico[['pl_name', 'pl_dens', 'pl_rade']])


# Buscando o planeta que tem a menor distância combinada para o Raio (1.0) e a Densidade (5.51) da Terra
df_filtrado = df[df['pl_dens'].between(4.0, 6.5) & (df['pl_rade'] <= 1.5)].dropna(subset=['pl_dens', 'pl_rade'])

# Calculamos a diferença para os valores da Terra
df_filtrado['distancia_da_terra'] = ((df_filtrado['pl_dens'] - 5.51)**2 + (df_filtrado['pl_rade'] - 1.0)**2)**0.5

# Pegamos o mais próximo de zero
gemeo_estrutural = df_filtrado.sort_values(by='distancia_da_terra').head(1)

print("O SEU VENCEDOR: GÊMEO ROCHOSO E MAGNÉTIÇO MAIS PRÓXIMO DA TERRA:\n")
print(gemeo_estrutural[['pl_name', 'pl_dens', 'pl_rade']])


# CRUZAMOS TODOS OS FILTROS
condicao_final = (
    (df['distancia_anos_luz'] <= 200) &                               # Filtro 1: Perto
    #(df['st_logg'].between(limite_inferior, limite_superior)) &       # Filtro 2: Gravidade da Estrela similar
    (df['pl_bmasse'].between(LIMITE_INFERIOR_DA_MASSA_DA_TERRA, LIMITE_SUPERIOR_DA_MASSA_DA_TERRA)) & # Filtro 3: Massa
    (df['pl_rade'].between(LIMITE_INFERIOR_RAIO, LIMITE_SUPERIOR_RAIO)) & # Filtro 4: Raio
    (df['pl_insol'].between(LIMITE_INFERIOR_DE_RADIACAO, LIMITE_SUPERIOR_DE_RADIACAO)) & # Filtro 5: Radiação
    (df['pl_dens'].between(4.0, 6.5))                                 # Filtro Extra: Potencial Magnético
)

# Aplicando o super-filtro no DataFrame original
planetas_perfeitos = df[condicao_final]

print('=' * 50)
print(f"TOTAL DE PLANETAS QUE PASSARAM EM TODOS OS FILTROS JUNTOS: {len(planetas_perfeitos)}\n")

if not planetas_perfeitos.empty:
    print("LISTA DOS PLANETAS MAIS SIMILARES À TERRA EM TUDO:\n\n")
    print("=" * 70)
    print(planetas_perfeitos[['pl_name', 'distancia_anos_luz', 'pl_bmasse', 'pl_rade', 'pl_insol', 'pl_dens']])
    print("=" * 70)    
else:
    print("NENHUM PLANETA PASSOU EM 100% DOS FILTROS SIMULTANEAMENTE!")
    print("Dica: A combinação de todos os filtros ao mesmo tempo é extremamente rigorosa na biologia planetária real.")


#
#   VIEW (VISUALIZAÇÃO DOS DADOS)
# 


# Criando um gráfico comparando Raio vs Densidade
plt.figure(figsize=(10, 6))

# Plota todos os planetas rochosos em cinza
plt.scatter(df_filtrado['pl_rade'], df_filtrado['pl_dens'], color='lightgray', alpha=0.5, label='Outros Exoplanetas')

# Plota o nosso grande vencedor em destaque (Vermelho)
plt.scatter(1.05, 5.51, color='red', s=150, edgecolor='black', zorder=5, label="Teegarden's Star b")

# Plota a posição teórica da Terra como referência (Azul)
plt.scatter(1.0, 5.51, color='blue', s=150, marker='X', edgecolor='black', zorder=5, label='Planeta Terra')

plt.title("Onde está a nossa Nova Terra? (Raio vs Densidade)")
plt.xlabel("Raio (Em Raios Terrestres)")
plt.ylabel("Densidade (g/cm³)")
plt.axvline(1.0, color='blue', linestyle='--', alpha=0.3)
plt.axhline(5.51, color='blue', linestyle='--', alpha=0.3)
plt.legend()
plt.grid(True, alpha=0.2)

plt.savefig('resultado_final_exoplanetas.png')
print("\nGráfico gerado e salvo com sucesso como 'resultado_final_exoplanetas.png'!")
plt.show()