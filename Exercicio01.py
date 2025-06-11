import pandas as pd
import numpy as np

try:
    print("Obtendo e processando dados de estelionato...")
    url = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df = pd.read_csv(url, sep=';', encoding='iso-8859-1')[['munic', 'estelionato']]
    df_total = df.groupby('munic', as_index=False).sum(numeric_only=True)

    print("\nResumo dos dados agregados:")
    print(df_total.head())

    array = df_total['estelionato'].values
    media, mediana = np.mean(array), np.median(array)
    distancia = abs((media - mediana) / mediana)

    print("\nTendência central:")
    print(f"Média: {media:.2f}, Mediana: {mediana}, Distância relativa: {distancia:.2f}")

    q1, q2, q3 = np.quantile(array, [0.25, 0.5, 0.75])
    print(f"\nQuartis:\nQ1: {q1}, Q2: {q2}, Q3: {q3}")

    print("\nMenores casos:")
    print(df_total[df_total['estelionato'] < q1].sort_values('estelionato'))

    print("\nMaiores casos:")
    print(df_total[df_total['estelionato'] > q3].sort_values('estelionato', ascending=False))

    iqr = q3 - q1
    li, ls = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    print(f"\nOutliers:\nLimite inferior: {li}, Limite superior: {ls}")

    out_inf = df_total[df_total['estelionato'] < li].sort_values('estelionato', ascending=False)
    out_sup = df_total[df_total['estelionato'] > ls].sort_values('estelionato', ascending=False)

    print("\nOutliers inferiores:")
    print(out_inf if not out_inf.empty else "Nenhum encontrado.")

    print("\nOutliers superiores:")
    print(out_sup if not out_sup.empty else "Nenhum encontrado.")

except Exception as e:
    print(f"Erro: {e}")
