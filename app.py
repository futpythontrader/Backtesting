import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


@st.cache
def load_base():
    url = "https://github.com/futpythontrader/YouTube/blob/main/x_FutPythonTrader_Base_de_Dados_Temporada_Anterior_x.xlsx?raw=true"
    data_jogos = pd.read_excel(url)

    return data_jogos

df = load_base()

df.loc[(df['FT_Goals_H'] >  df['FT_Goals_A']), 'Profit'] = df['FT_Odds_H'] - 1
df.loc[(df['FT_Goals_H'] <= df['FT_Goals_A']), 'Profit'] = -1

# Caixa de texto para filtrar Odd Home
min_H = st.sidebar.number_input("FT_Odds_H", min_value=0, max_value=10, value=0)
max_H = st.sidebar.number_input("FT_Odds_H", min_value=0, max_value=10, value=10)

# Caixa de texto para filtrar Odd Draw
min_D = st.sidebar.number_input("FT_Odds_D", min_value=0, max_value=10, value=0)
max_D = st.sidebar.number_input("FT_Odds_D", min_value=0, max_value=10, value=10)

# Caixa de texto para filtrar Odd Away
min_A = st.sidebar.number_input("FT_Odds_A", min_value=0, max_value=10, value=0)
max_A = st.sidebar.number_input("FT_Odds_A", min_value=0, max_value=10, value=10)

# Caixa de texto para filtrar Odd Over 25
min_Over25 = st.sidebar.number_input("FT_Odds_Over25", min_value=0, max_value=10, value=0)
max_Over25 = st.sidebar.number_input("FT_Odds_Over25", min_value=0, max_value=10, value=10)

# Caixa de texto para filtrar Odd BTTS
min_BTTS = st.sidebar.number_input("Odds_BTTS_Yes", min_value=0, max_value=10, value=0)
max_BTTS = st.sidebar.number_input("Odds_BTTS_Yes", min_value=0, max_value=10, value=10)

# Filtre o dataframe pelos valores mínimos e máximos de cada coluna
df_filtrado = df[(df['FT_Odds_H'] >= min_H) & (df['FT_Odds_H'] <= max_H) &
                 (df['FT_Odds_D'] >= min_D) & (df['FT_Odds_D'] <= max_D) &
                 (df['FT_Odds_A'] >= min_A) & (df['FT_Odds_A'] <= max_A) &
                 (df['FT_Odds_Over25'] >= min_Over25) & (df['FT_Odds_Over25'] <= max_Over25) &
                 (df['Odds_BTTS_Yes'] >= min_BTTS) & (df['Odds_BTTS_Yes'] <= max_BTTS)]

# Crie uma nova coluna no dataframe filtrado com o profit acumulado
df_filtrado['Profit_acu'] = df_filtrado.Profit.cumsum()
profit = round(df_filtrado.Profit_acu.tail(1).item(),2)
ROI = round((df_filtrado.Profit_acu.tail(1)/len(df_filtrado)*100).item(),2)
df_filtrado.Profit_acu.plot(title="Back Home", xlabel='Entradas', ylabel='Stakes')
print("Profit:",profit,"stakes em", len(df_filtrado),"jogos")
print("ROI:",ROI,"%")

# Plote o gráfico com o profit acumulado do dataframe filtrado
plt.plot(df_filtrado['Profit_acu'])
st.pyplot()
