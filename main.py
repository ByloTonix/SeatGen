import streamlit as st
import plotly.graph_objects as go

rows = 10
cols = 12

seats_x = []
seats_y = []
labels = []
for row in range(rows):
    for col in range(cols):
        seats_x.append(col)
        seats_y.append(-row)
        labels.append(f"Ряд {row+1}, Место {col+1}")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=seats_x, 
    y=seats_y, 
    mode='markers',
    marker=dict(size=10, color='blue'),
    text=labels,
    hoverinfo='text'
))

fig.update_layout(
    title="Карта рассадки студентов",
    xaxis=dict(title="Места", tickmode='array', tickvals=list(range(cols)), showgrid=False),
    yaxis=dict(title="Ряды", tickmode='array', tickvals=[-i for i in range(rows)], ticktext=[str(i+1) for i in range(rows)], showgrid=False),
    plot_bgcolor='white'
)

st.title("Интерактивная карта рассадки студентов")
st.plotly_chart(fig)
