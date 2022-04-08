import streamlit as st
import psycopg2
import yaml


def main():
    """
        Wordle results
        With Streamlit
    """

    st.title("Wordle results with Streamlit")

    config = ""
    with open('../secrets.yml', 'r') as file:
        config = yaml.safe_load(file)
    # Initialize connection.
    # Uses st.experimental_singleton to only run once.

    @st.experimental_singleton
    def init_connection():
        return psycopg2.connect(**config["postgres"])

    conn = init_connection()

    # Perform query.
    # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.experimental_memo(ttl=600)
    def run_query(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    rows = run_query("SELECT * from tweets_v2 LIMIT 10;")

    st.write("Hello World!")
    # Print results.
    for row in rows:
        st.write(f"{row[0]} has a :{row[1]}:")


main()
