import streamlit as st
import plotly.graph_objects as go
import json
import pandas as pd

# Загрузка данных
with open("students.json", "r", encoding="utf-8") as f:
    students_data = json.load(f)

with open("room_layouts.json", "r", encoding="utf-8") as f:
    room_layouts = json.load(f)

# Получение списка всех кабинетов
rooms = sorted(set(s["room"] for s in students_data))

# Настройка темы
streamlit_theme = st.get_option("theme.base")
plotly_template = "plotly_dark" if streamlit_theme == "dark" else "plotly"

# Функция для отрисовки плана комнаты
def draw_room_layout(fig, room_data, taken_seats, room_name):
    if "top" in room_data:
        top_rows = room_data["top"]["rows"]
        top_cols = room_data["top"]["cols"]
        top_offset = room_data["top"].get("offset", 0)
        for row in range(top_rows):
            for col in range(top_cols):
                fig.add_trace(go.Scatter(
                    x=[col + top_offset],
                    y=[row + 11],
                    mode='markers',
                    marker=dict(size=20, color="gray" if (row, col) not in taken_seats else "pink"),
                    text=[f"Row {row+1}, Seat {col+1} (Available)" if (row, col) not in taken_seats else f"{taken_seats[(row, col)]}\nRow {row+1}, Seat {col+1}"],
                    hoverinfo='text',
                    showlegend=False
                ))

    main_rows = room_data["main"]["rows"]
    main_cols = room_data["main"]["cols"]
    for row in range(main_rows):
        for col in range(main_cols):
            fig.add_trace(go.Scatter(
                x=[col],
                y=[row + (top_rows if "top" in room_data else 0)],
                mode='markers',
                marker=dict(size=20, color="gray" if (row, col) not in taken_seats else "pink"),
                text=[f"Row {row+1}, Seat {col+1} (Available)" if (row, col) not in taken_seats else f"{taken_seats[(row, col)]}\nRow {row+1}, Seat {col+1}"],
                hoverinfo='text',
                showlegend=False
            ))

    fig.update_layout(
        title=f"Student Seating Map for Room {room_name}",
        xaxis=dict(
            title="Seats", 
            tickmode='array', 
            tickvals=list(range(main_cols)), 
            ticktext=[str(i+1) for i in range(main_cols)], 
            showgrid=False, 
            zeroline=False,
            fixedrange=True
        ),
        yaxis=dict(
            title="Rows", 
            tickmode='array', 
            tickvals=[i for i in range(main_rows + (top_rows if "top" in room_data else 0))], 
            ticktext=[str(i+1) for i in range(main_rows + (top_rows if "top" in room_data else 0))], 
            showgrid=False, 
            zeroline=False,
            fixedrange=True
        ),
        template=plotly_template,
        dragmode=False
    )

for room in rooms:
    st.subheader(f"Room {room}")
    room_seats = [s for s in students_data if s["room"] == room]
    taken_seats = {(s["row"] - 1, s["col"] - 1): s["name"] for s in room_seats}

    fig = go.Figure()
    room_key = f"R{room}"
    draw_room_layout(fig, room_layouts[room_key], taken_seats, room)
    st.plotly_chart(fig, config={"scrollZoom": False, "displayModeBar": False})

    st.write("### Student List for Room", room)
    table_data = []
    for student in room_seats:
        table_data.append({
            "Name": student["name"],
            "Room": student["room"],
            "Row": student["row"],
            "Seat": student["col"]
        })
    
    df = pd.DataFrame(table_data)
    st.table(df)