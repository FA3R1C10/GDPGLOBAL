#%% Bibliotecas
import pandas as pd
from pandas_datareader import wb
import datetime as dt
#%% Lista de países
countries = ["ARG","AUS", "BRA", "CAN", "CHN", "DEU", "FRA", "GBR", "IDN", "IND", "ITA", "JPN", "KOR", "MEX", "RUS", "SAU", "TUR", "USA", "ZAF"]
#%% constrói o dataframe da variação do PIB
gdp_df = wb.download(countries, indicator = "NY.GDP.MKTP.KD.ZG", start=2024, end=2024)
gdp_df = gdp_df.reset_index().dropna() #transforma índices em colunas
gdp_df = gdp_df.rename(columns = {"NY.GDP.MKTP.KD.ZG": "GDP Growth (%)"}) # renomeia a coluna
gdp_df["GDP Growth (%)"] = gdp_df["GDP Growth (%)"].astype(float).apply(lambda x: f"{x:.2f}") #transforma texto em número
#%% constrói o dataframe com a taxa de câmbio média em 2024
cambio_medio = wb.download(country= countries, indicator= "PA.NUS.FCRF", start=2024, end= 2024, freq="A")
cambio_medio = cambio_medio.reset_index(drop=False).dropna()
cambio_medio = cambio_medio.rename(columns = {"PA.NUS.FCRF": "Tx média de Câmbio"})
cambio_medio["Tx média de Câmbio"] = cambio_medio["Tx média de Câmbio"].astype(float).apply(lambda x: f"{x:.2f}")
# %% constrói o dataframe com a a taxa de desemprego média de 2024
unemployment = wb.download(country= countries, indicator="SL.UEM.TOTL.ZS", start=2024, end=2024)
unemployment = unemployment.reset_index().dropna()
unemployment = unemployment.rename(columns={"SL.UEM.TOTL.ZS": "Tx de Desocupação"})
unemployment["Tx de Desocupação"] = unemployment["Tx de Desocupação"].astype(float).apply(lambda x: f"{x:.2f}")
# %%
cpi = wb.download(country = countries, indicator= "FP.CPI.TOTL.ZG", start= 2024, end= 2024)
cpi = cpi.reset_index(drop=False).dropna()
cpi = cpi.rename(columns = {"FP.CPI.TOTL.ZG": "CPI"})
cpi["CPI"] = cpi["CPI"].astype(float).apply(lambda x: f"{x:.2f}")
# %%
conta_corrente = wb.download(country = countries, indicator= "BN.CAB.XOKA.GD.ZS", start= 2024, end = 2024)
conta_corrente = conta_corrente.reset_index().dropna()
conta_corrente = conta_corrente.rename(columns= {"BN.CAB.XOKA.GD.ZS": "Conta Corrente (% PIB)"})
conta_corrente["Conta Corrente (% PIB)"] = conta_corrente["Conta Corrente (% PIB)"].astype(float).apply(lambda x: f"{x:.2f}")
