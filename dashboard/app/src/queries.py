import streamlit as st


@st.cache
def get_days_with_stats():
    return """
        SELECT min(hour_window::date) as min_date, max(hour_window::date) as max_date
        FROM stats_hourly
        """


@st.cache
def get_data_for_day(day):
    return f"""
      SELECT *
      FROM stats_hourly
      WHERE hour_window::date = '{day}'
      ORDER BY hour_window
      """


@st.cache
def get_most_common_results_per_hour(hour):
    return f"""
      SELECT *
      FROM stats_hourly_most_common_results
      WHERE hour_window = '{hour}'
      """


@st.cache
def get_results_distribution(day):
    return f"""
      SELECT *
      FROM stats_hourly_results_distribution
      WHERE hour_window::date = '{day}'
      """
