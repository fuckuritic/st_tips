import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Apple Stock', page_icon="🍎")


# Заголовок
st.title(
    ":blue[_Данные о котировках компании_] :red[_Apple_] :iphone: :computer: :headphones:"
)

# Тикер компании
tickerSymbol = "AAPL"

# Загрузка данных с помощью yfinance
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period="1d", start="2025-1-01", end="2025-6-16")

# Добавляем запятых для читаемости Рыночной капитализации
market_cap = tickerData.info['marketCap'] 
formatted_cap = f'{market_cap:,}'

# Информация о компании
st.sidebar.header(":blue[**Основная информация о компании**]")
st.sidebar.write(f":green[***Тикер***] :red[**{tickerSymbol}**]")
st.sidebar.write(
    f":green[***Рыночная капитализация:***] :red[**{formatted_cap} $**]"
)
st.sidebar.write(f":green[***Сектор:***] :red[**{tickerData.info['sector']}**]")
st.sidebar.write(f":green[***Отрасль:***] :red[**{tickerData.info['industry']}**]")

# Визуализация графиков
st.subheader(":gray[График закрытия торгов]", divider="gray")
fig, ax = plt.subplots()
plt.style.use("classic")
ax.plot(tickerDf.Close, label="Цена закрытия")
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_xlabel("Дата", color="red")
ax.set_ylabel("Цена закрытия ($)", color="blue")


st.pyplot(fig)

# Визуализация графиков
st.subheader(":gray[График обьема торгов]", divider="gray")
st.line_chart(tickerDf.Volume)


