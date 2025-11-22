#%% Bibliotecas
from bcb import sgs
import pandas as pd
import numpy as np
import datetime as dt
from statsmodels.tsa.filters.hp_filter import hpfilter
#%% Criar Dataframe de Selic desde 2010
selic0 = sgs.get(432, "2009-01-01", "2014-12-31")
selic1 = sgs.get(432, "2015-01-01", "2019-12-31")
selic2 = sgs.get(432, "2020-01-01", dt.datetime.today()) 
selic = pd.concat([selic0, selic1, selic2], axis=0)
selic.rename(columns={"432": "Selic"}, inplace= True)
#%% Criar Dataframe de Selic de 12 meses anualizada
selic_dia = ((1 + selic["Selic"]/100) ** (1/360) - 1) * 100 # converte selic em taxa dia porém retorna como pandas series
selic_dia = pd.DataFrame(selic_dia) # transforma pandas series em um Dataframe
selic12m = selic_dia.rolling(window = 360).apply(lambda x:(np.prod(x/100 + 1) - 1) * 100, raw = True).dropna() #encontra a Selic de 12m
selic12m.rename(columns={"Selic": "Selic 12m"}, inplace= True)
#%% Criar dataframe com Selic e selic 12 meses
selic_df = pd.concat([selic, selic12m], axis=1).dropna()
selic_df["Selic"] = selic_df["Selic"].astype(float).round(2)
selic_df["Selic 12m"] = selic_df["Selic 12m"].astype(float).round(2)
#%% Criar Dataframe de IPCA desde 2010
ipca = sgs.get(433, "2009-01-01", dt.datetime.today()) # importa período maior para construção do ipca3m
ipca.rename(columns={"433": "IPCA mensal"}, inplace= True)
#%% Criar Dataframe com IPCA de 3 meses anualizado
ipca3m = ipca.rolling(window = 3).apply(lambda x:(np.prod((x/100) + 1) - 1) * 100, raw = True) #calcula o IPCA de 3m
ipca3m = ipca3m.apply(lambda x:((1 + (x /100)) ** 4 - 1) * 100) # anualiza o IPCA de 3m
ipca3m = pd.DataFrame(ipca3m)
ipca3m.rename(columns={"IPCA mensal": "IPCA 3m Anualizado"}, inplace=True)
#%% Criar Dataframe com IPCA de 12 meses
ipca12m = sgs.get(13522, "2009-01-01", dt.datetime.today())
ipca12m.rename(columns={"13522": "IPCA 12m"}, inplace= True)
#%% Criar Dataframe com núcleo ex alimentos e energia do IPCA
ipca_ex_alim_energia = sgs.get(11427, "2009-01-01", dt.datetime.today())
ipca_ex_alim_energia.rename(columns={"11427": "IPCA (Ex Alim. e Energ.)"}, inplace= True)
#%% Criar Dataframe com núcleo ex alimentos e energia do IPCA de 3 meses anualizado e 12 meses
ipca_ex_alim_energia3m = ipca_ex_alim_energia.rolling(window = 3).apply(lambda x:(np.prod((x/100) + 1) - 1) * 100, raw = True)
ipca_ex_alim_energia3m = ipca_ex_alim_energia3m.apply(lambda x:((1 + (x /100)) ** 4 - 1) * 100)
ipca_ex_alim_energia3m.rename(columns={"IPCA (Ex Alim. e Energ.)": "IPCA (Ex alim. e energ.) 3m Anualizado"}, inplace=True)
ipca_ex_alim_energia3m = pd.DataFrame(ipca_ex_alim_energia3m)
#%% Criar Dataframe com núcleo ex alimentos e energia do IPCA de 12 meses
ipca_ex_alim_energia12m = ipca_ex_alim_energia.rolling(window=12).apply(lambda x:(np.prod((x/100) + 1) - 1) * 100, raw = True)
ipca_ex_alim_energia12m.rename(columns={"IPCA (Ex Alim. e Energ.)": "IPCA (Ex alim. e energ.) 12m"}, inplace=True)
ipca_ex_alim_energia12m = pd.DataFrame(ipca_ex_alim_energia12m)
#%% Criar Dataframe com a difusão do IPCA
difusa = sgs.get(21379, "2009-01-01", dt.datetime.today())
difusa.rename(columns={"21379": "Difusão"}, inplace= True)
#%% Criar Dataframe com a média dos núcleos do IPCA
nucleos = [11427, 16121, 27838, 27839, 11426, 4466, 16122, 28751, 28750]
media_nucleos = sgs.get(nucleos, "2019-01-01", dt.datetime.today())
media_nucleos["Média"] = media_nucleos.mean(axis=1)
media_nucleos = media_nucleos[["Média"]]
#%% Criar um Dataframe unificado de IPCA
ipca_df = pd.concat([ipca, ipca3m, ipca12m, ipca_ex_alim_energia, ipca_ex_alim_energia3m, ipca_ex_alim_energia12m, difusa, media_nucleos], axis=1).dropna()
ipca_df["Bottom Target"] = 1.5
ipca_df["Top Target"] = 4.5
ipca_df["Target"] = 3.0
ipca_df = ipca_df.astype(float).round(2)
# %% Desemprego
desemprego_df = sgs.get(24369, "2020-01-01", dt.datetime.today())
desemprego_df.rename(columns={"24369": "Desemprego"}, inplace= True)
# %% Juro real ex-post
juro_ex_post = selic12m.reindex(ipca12m.index)
juro_ex_post["IPCA 12m"] = ipca12m
juro_ex_post["Juro Real ex-post"] = ((1 + juro_ex_post["Selic 12m"]/100) / (1 + juro_ex_post["IPCA 12m"]/100) - 1) * 100
juro_ex_post_df = juro_ex_post.astype(float).round(2).dropna()
#%% IBC-Br
ibcbr = sgs.get(24364, "2009-01-01", dt.datetime.today())
ibcbr.rename(columns={"24364": "IBC-Br"}, inplace= True)
ibc_agro = sgs.get(29602, "2009-01-01", dt.datetime.today())
ibc_agro.rename(columns={"29602": "IBC-Br Agro"}, inplace= True)
ibc_industria = sgs.get(29604, "2009-01-01", dt.datetime.today())
ibc_industria.rename(columns={"29604": "IBC-Br Indústria"}, inplace= True)
ibc_servicos = sgs.get(29606, "2009-01-01", dt.datetime.today())
ibc_servicos.rename(columns={"29606": "IBC-Br Serviços"}, inplace= True)
ibc_ex_agro = sgs.get(29608, "2009-01-01", dt.datetime.today())
ibc_ex_agro.rename(columns={"29608": "IBC-Br ex Agro"}, inplace= True)
ibc_impostos = sgs.get(29610, "2009-01-01", dt.datetime.today())
ibc_impostos.rename(columns={"29610": "IBC-Br Impostos"}, inplace= True)
ibcbr_df = pd.concat([ibcbr, ibc_agro, ibc_industria, ibc_servicos, ibc_ex_agro, ibc_impostos], axis=1).dropna()
ibcbr_df = ibcbr_df.astype(float).round(2)
#%% Criar dataframe com hiato de produto
PIB_df = sgs.get(4382, start='1996-01-01', end= dt.date.today())
PIB_df.columns = ['PIB']
pib_ciclo, pib_tendencia = hpfilter(PIB_df['PIB'], lamb=129600)
hiato = pib_ciclo / pib_tendencia * 100
PIB_df['Hiato'] = hiato
PIB_df = pd.DataFrame(PIB_df)
