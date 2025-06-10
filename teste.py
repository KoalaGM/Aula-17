import pandas as pd
import numpy as np

try:
    print("Obtendo dados de estelionato...")

    # URL da base de dados oficial do ISP-RJ
    URL = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

    # Lê os dados com separador ";" e codificação ISO-8859-1
    df = pd.read_csv(URL, sep=';', encoding='iso-8859-1')

    # Seleciona apenas as colunas relevantes
    df_estelionato = df[['munic', 'estelionato']]

    # Agrupa os dados por município, somando os casos de estelionato
    df_total = df_estelionato.groupby('munic').sum(numeric_only=True).reset_index()

    print("\nVisualização inicial dos dados agregados:")
    print(df_total.head())

except Exception as e:
    print(f"Erro ao obter os dados: {e}")
    exit()


try:
    print("\nAnálise estatística dos casos de estelionato...")

    # Convertendo os dados para array NumPy
    array = np.array(df_total['estelionato'])

    # Medidas de tendência central
    media = np.mean(array)
    mediana = np.median(array)
    distancia = abs((media - mediana) / mediana)

    print("\nMedidas de tendência central:")
    print(30 * "-")
    print(f"Média: {media:.2f}")
    print(f"Mediana: {mediana}")
    print(f"Distância relativa entre média e mediana: {distancia:.2%}")

    # Quartis
    q1 = np.quantile(array, 0.25)
    q2 = np.quantile(array, 0.50)
    q3 = np.quantile(array, 0.75)

    print("\nQuartis:")
    print(30 * "-")
    print(f"Q1 (25%): {q1}")
    print(f"Q2 (50% - Mediana): {q2}")
    print(f"Q3 (75%): {q3}")

    # Municípios com menos e mais casos
    menores = df_total[df_total['estelionato'] < q1]
    maiores = df_total[df_total['estelionato'] > q3]

    print("\nMunicípios com menos casos de estelionato:")
    print(menores.sort_values(by='estelionato'))

    print("\nMunicípios com mais casos de estelionato:")
    print(maiores.sort_values(by='estelionato', ascending=False))

    # Cálculo do IQR e limites para outliers
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    print("\nLimites para identificação de outliers:")
    print(f"Limite inferior: {limite_inferior}")
    print(f"Limite superior: {limite_superior}")

    # Identificação de outliers
    outliers_inferiores = df_total[df_total['estelionato'] < limite_inferior]
    outliers_superiores = df_total[df_total['estelionato'] > limite_superior]

    print("\nOutliers inferiores (muito abaixo do esperado):")
    if outliers_inferiores.empty:
        print("Nenhum outlier inferior encontrado.")
    else:
        print(outliers_inferiores.sort_values(by='estelionato'))

    print("\nOutliers superiores (muito acima do esperado):")
    if outliers_superiores.empty:
        print("Nenhum outlier superior encontrado.")
    else:
        print(outliers_superiores.sort_values(by='estelionato', ascending=False))

except Exception as e:
    print(f"Erro na análise estatística: {e}")
