import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import plotly.io as pio
import io

import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Tips', page_icon="💸")


st.title(':blue[***Исследуем чаевые***]  :red[за Январь]:dollar:')



# РАЗДЕЛИТЕЛЬ
st.subheader(' ', divider="gray")
st.subheader(' ')


# КЭШИРУЕМ ЗАГРУЗКУ CSV
@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


# ВЫВОДИМ ДАТАСЕТ СО ВСЕЙ ИНФОРМАЦИЕЙ

uploaded_file = st.sidebar.file_uploader(':green[**Загрузи сюда датасет**] 👇', type='csv')

if uploaded_file is not None:
    df = load_csv(uploaded_file)

    # генератор дат 
    date_range = pd.date_range(start='2023-01-01', end='2023-01-31', periods=len(df))

    # генератор массива с количеством секунд в сутках (от 0 до 86400)
    random_seconds = np.random.randint(0, 86400, size=len(date_range))

    # преобразуем секунды в timedelta и добавляем к дате
    datetimes = date_range + pd.to_timedelta(random_seconds, unit='sec')

    # загружаем в наш ДФ
    df["time_order"] = datetimes

else:
    st.stop()

st.subheader(":gray[Загруженный датасет]")
st.write(df)



# РАЗДЕЛИТЕЛЬ
st.subheader(' ', divider="gray")
st.subheader(' ')



# СТРОИМ ГРАФИК ЧАЕВЫХ ЗА ЯНВАРЬ

st.subheader('**📈 График динамики чаевых**')

fig, ax = plt.subplots()
plt.style.use("classic")
sns.lineplot(data=df, x="time_order", y="tip", linewidth=2, color='green', ax=ax)  # Время по X, чаевые по Y

ax.set_ylim(bottom=0, top=df['tip'].max() * 1.1)  # +10% запаса сверху, чтобы видеть все данные по Y


ax.set_xlabel("Дата", color="red")
ax.set_ylabel("Чаевые ($)", color="blue")

ax.grid(True, linestyle='--', alpha=0.7)

max_tip_idx = df['tip'].idxmax() # находим максимально значение чаевых за месяц (индекс строки)

# Аннотация для МАКСИМАЛЬНОГО значения
ax.annotate(f'Макс: {df.loc[max_tip_idx, "tip"]}$',
            xy=(df.loc[max_tip_idx, "time_order"], df.loc[max_tip_idx, "tip"]), # Точка (X, Y)
            xytext=(10, 10), textcoords='offset points',
            arrowprops=dict(arrowstyle='->', color='magenta'))


min_tip_idx = df['tip'].idxmin()

# Аннотация для МИНИМАЛЬНОГО значения (новое)
ax.annotate(f'Мин: {df.loc[min_tip_idx, "tip"]}$',
            xy=(df.loc[min_tip_idx, "time_order"], df.loc[min_tip_idx, "tip"]),
            xytext=(10, -20),  # Размещаем ниже точки
            textcoords='offset points',
            arrowprops=dict(arrowstyle='->', color='magenta'))

plt.xticks(rotation=45)  # Поворот подписей по X, чтобы всё влазило
plt.tight_layout()

st.pyplot(fig)

# Добавим статистику
st.subheader("📘 Статистика по чаевым:")
st.subheader(f"- Среднее: {df['tip'].mean():.2f}$")
st.subheader(f"- Максимум: {df['tip'].max():.2f}$")
st.subheader(f"- Минимум: {df['tip'].min():.2f}$")


# СКАЧИВАЕМ ГРАФИК ПО ЧАЕВЫМ ЧЕРЕЗ КНОПКУ

# сохраняем график с помощью io.BytesIO
buffer = io.BytesIO()
fig.savefig(buffer, format='png')
buffer.seek(0) # перейти в начало потока

st.sidebar.download_button('📘 :green[Скачать график чаевых за январь]', 
                                                data=buffer, 
                                                file_name='tips_per_january.png',
                                                mime='image/png')



# РАЗДЕЛИТЕЛЬ
st.subheader(' ', divider="gray")
st.subheader(' ')



st.subheader('**📊Гистограмма распределения сумм счетов**')
st.subheader('')

chart = alt.Chart(df).mark_bar().encode(alt.X('total_bill', bin=alt.Bin(maxbins=30), title='Сумма заказов'), 
                                        alt.Y('count()', title='Количество заказов')
                                        ).configure_axis(labelColor='red', titleColor='green')

st.altair_chart(chart, use_container_width=True)



# СКАЧИВАЕМ ГРАФИК ГИСТОГРАММЫ ПО СЧЕТАМ

# сохраняем график с помощью io.BytesIO
alt_buffer = io.BytesIO()
chart.save(alt_buffer, format='png')
alt_buffer.seek(0) # перейти в начало потока

st.sidebar.download_button('📊 :green[Скачать гистограмму сумм счетов]', 
                            data=alt_buffer, 
                            file_name='histogram.png',
                            mime='image/png')



# РАЗДЕЛИТЕЛЬ
st.subheader(' ', divider="gray")
st.subheader(' ')



# СТРОИМ ТОЧЕЧНЫЙ ГРАФИК СВЯЗИ СЧЕТА И ЧАЕВЫХ

st.subheader('🔴 **График связи суммы счета к чаевым**')


fig = px.scatter(df, x='total_bill', 
                 y='tip', 
                 size='size', # Количпество человек у счета
                 color='size',
                 color_continuous_scale='Viridis',
                 labels={'total_bill': 'Сумма счета', 'tip': 'Чаевые', 'size': 'Количество человек'},
                 opacity=0.7)

fig.update_traces(
    marker=dict(
        line=dict(width=1, color='black'),  # рамка вокруг точек
        symbol='circle'
    )
)


# цвет и др параметры сетки и подписей осей
fig.update_layout(
    xaxis=dict(
        showgrid=True,
        gridcolor='LightGray',
        gridwidth=2,
        tickfont=dict(color='red'),
        title_font=dict(color='darkred'),
        title_text="Сумма чека"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='LightGray',
        gridwidth=2,
        tickfont=dict(color='blue'),
        title_font=dict(color='darkblue'),
        title_text="Чаевые"
    )
)

st.plotly_chart(fig, use_container_width=True)


# СКАЧИВАЕМ ТОЧЕЧНЫЙ ГРАФИК СВЯЗИ СЧЕТА И ЧАЕВЫХ

# сохраняем график в буфер
px_buffer = io.BytesIO()
pio.write_image(fig, px_buffer, format='png')
px_buffer.seek(0)

st.sidebar.download_button(
    label="🔴 :green[Скачать точечный график счета и чаевых]",
    data=px_buffer,
    file_name="scatter_plot.png",
    mime="image/png"
)