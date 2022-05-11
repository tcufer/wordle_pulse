import streamlit as st
import altair as alt
import psycopg2
import pandas.io.sql as sqlio
from src.queries import get_days_with_stats, get_data_for_day, get_most_common_results_per_hour, get_results_distribution
from src.utils import parse_wordle_result
from src.constants import DB_CONN_STRING


def _prepare_distribution_chart():
    """
    Prepares bar chart for distribution of results based on score
    """

    bars = alt.Chart(st.session_state.metric_6).mark_bar().encode(
        x=alt.X('score:O', axis=alt.Axis(title='Score', labelFontSize=15, titleFontSize=20)),
        y=alt.Y('score_total_count:Q', axis=alt.Axis(title='Count', labelFontSize=15, titleFontSize=20))
    )

    text = bars.mark_text(
        dy=-10,
        size=20
    ).encode(
        text='score_total_count:Q'
    )
    return (bars + text)


def _prepare_daily_totals_chart(source):
    """
    Prepares stacked bar char for All vs Unique result counts comparison
    """

    base = alt.Chart(source).encode(
        x=alt.X('hour_window', axis=alt.Axis(title='Hour', labelFontSize=15, titleFontSize=20))
        )

    bar = base.mark_bar().encode(
        y=alt.Y('results_total_count:Q', axis=alt.Axis(title='Total count', labelFontSize=15, titleFontSize=20))
        )

    line = base.mark_bar(color='orange').encode(
        y=alt.Y('unique_results_total_count:Q', axis=alt.Axis(title='Unique count'))
    )

    return (bar + line).properties(width=600)


def main():
    """
    Dashboard for Wordle results
    """

    st.set_page_config(layout="wide")
    st.title("Wordle Pulse dashboard")
    col1, col2 = st.columns([1, 1])

    @st.experimental_singleton
    def init_connection():
        return psycopg2.connect(DB_CONN_STRING)

    conn = init_connection()

    all_dates = sqlio.read_sql_query(get_days_with_stats(), conn)

    # day picker in sidebar
    selected_day = st.sidebar.date_input(
     "Select date",
     value=all_dates['min_date'][0],
     min_value=all_dates['min_date'][0],
     max_value=all_dates['max_date'][0],
     )

    data_for_selected_day = sqlio.read_sql_query(get_data_for_day(selected_day), conn)

    hours = data_for_selected_day['hour_window']
    daily_totals = data_for_selected_day[['hour_window', 'results_total_count', 'unique_results_total_count']]
    daily_totals['hour_window'] = daily_totals['hour_window'].dt.strftime("%H:%M:%S")

    col1.header('Result counts by hour')
    selected_hour = col1.select_slider('Hour', options=hours, key='hour_slider')
    most_common_results = sqlio.read_sql_query(get_most_common_results_per_hour(selected_hour), conn)

    most_common_results['result'] = most_common_results['result'].apply(parse_wordle_result)

    st.session_state.metric_1 = list(data_for_selected_day.loc[data_for_selected_day['hour_window'] == selected_hour]['results_total_count'])[0]
    st.session_state.metric_2 = list(data_for_selected_day.loc[data_for_selected_day['hour_window'] == selected_hour]['results_last_hour'])[0]
    st.session_state.metric_3 = list(data_for_selected_day.loc[data_for_selected_day['hour_window'] == selected_hour]['unique_results_last_hour'])[0]

    st.session_state.metric_4 = list(data_for_selected_day.loc[data_for_selected_day['hour_window'] == selected_hour]['unique_results_total_count'])[0]

    col1.metric('All results today', str(st.session_state.metric_1),)
    col1.metric('Unique results today', str(st.session_state.metric_4))
    col1.metric('Results in last hour', str(st.session_state.metric_2))
    col1.metric('Unique results in last hour', str(st.session_state.metric_3))

    col1.subheader("Most common results in the last hour")
    st.session_state.metric_5 = most_common_results[(most_common_results['hour_window'] == selected_hour)]
    for idx, row in st.session_state.metric_5.iterrows():
        col1.write(f"Count: {row['total_count']}")
        col1.markdown(row['result'])

    # results distribution chart
    distribution_data = sqlio.read_sql_query(get_results_distribution(selected_day), conn)
    st.session_state.metric_6 = distribution_data[distribution_data['hour_window'] == selected_hour]
    col2.header('Result distribution in last hour')
    col2.altair_chart(_prepare_distribution_chart(), use_container_width=True)

    col2.header('All vs Unique results through day')
    col2.altair_chart(_prepare_daily_totals_chart(daily_totals), use_container_width=True)


main()
