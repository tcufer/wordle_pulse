import streamlit as st
import numpy as np
import pandas as pd
import psycopg2
import yaml
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


# def _lookup(date_col, format=None):
#     dates = {date: pd.to_datetime(date, format=format) for date in date_col.unique()}
#     return date_col.map(dates)

def update_metric_2():
    st.session_state.metric_2 = str(int(np.random.randn(1)[0]*10))

# def date_change():
#     st.session_state.selected_date = str(int(np.random.randn(1)[0]*10))

def main():
    """
        Wordle results
        With Streamlit
    """

    st.title("Wordle results with Streamlit")

    # config = ""
    # with open('../secrets.yml', 'r') as file:
    #     config = yaml.safe_load(file)
    # # Initialize connection.
    # # Uses st.experimental_singleton to only run once.

    # @st.experimental_singleton
    # def init_connection():
    #     return psycopg2.connect(**config["postgres"])

    # conn = init_connection()

    # # Perform query.
    # # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    # @st.experimental_memo(ttl=600)
    # def run_query(query):
    #     with conn.cursor() as cur:
    #         cur.execute(query)
    #         return cur.fetchall()

    # rows = run_query("SELECT * from agg_hourly LIMIT 10;")

    # st.write("Hello World!")
    # # Print results.
    # for row in rows:
    #     st.write(f"{row[0]} has a :{row[1]}:")

    data = pd.read_csv('agg_hourly_tmp.csv')
    df = data[data.index < 48]
    # table
    # st.write(df)
    # AgGrid(df)

    # sidebar
    # options = [row for row in df['hour_window']]
    options = pd.to_datetime(df['hour_window']).dt.strftime('%Y-%m-%d').unique()
    selected_day = st.sidebar.selectbox('Select day', options)

    # slider
    # hours = pd.to_datetime(df['hour_window'])
    st.write(str(selected_day))
    data_for_selected_day = df.loc[pd.to_datetime(df['hour_window']).dt.strftime('%Y-%m-%d') == selected_day]
    hours = data_for_selected_day['hour_window']
    total_counts = data_for_selected_day['results_total_count']
    st.write(hours)

    selected_hour = st.select_slider('Hour', options=hours, key='hour_slider')
    st.session_state.metric_1 = list(df.loc[df['hour_window'] == selected_hour]['results_total_count'])[0]
    st.session_state.metric_2 = list(df.loc[df['hour_window'] == selected_hour]['results_last_hour'])[0]
    st.session_state.metric_3 = list(df.loc[df['hour_window'] == selected_hour]['unique_results_last_hour'])[0]
    # st.text_input('test', key='hourly_stats')  # this is a widget

    st.metric('Results up untill now', str(st.session_state.metric_1), delta=None, delta_color="normal")
    st.metric('Results in last hour', str(st.session_state.metric_2), delta=None, delta_color="normal")
    st.metric('Unique results in last hour', str(st.session_state.metric_3), delta=None, delta_color="normal")

    # chart
    # st.line_chart(df[['results_last_hour', 'unique_results_last_hour']])
    st.header('Total counts per day')
    st.line_chart(total_counts)


main()
