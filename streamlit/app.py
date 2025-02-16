# Core Pkgs
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from datetime import datetime
import altair as alt
import os
import sqlite3

# FastAPI endpoint URL
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000/classify")

conn = sqlite3.connect("data.db")
c = conn.cursor()


# Create Table Function
def create_table():
    c.execute(
        "CREATE TABLE IF NOT EXISTS predictionTable(message TEXT, prediction TEXT, probability NUMBER, postdate DATE)"
    )


def add_data(message, prediction, probability, postdate):
    c.execute(
        "INSERT INTO predictionTable(message, prediction, probability, postdate) VALUES (?,?,?,?)",
        (message, prediction, probability, postdate),
    )
    conn.commit()


def view_all_data():
    c.execute("SELECT * FROM predictionTable")
    data = c.fetchall()
    return data


def main():
    menu = ["Home", "Manage", "About"]
    create_table()
    st.title("Scam or Legitimate Text Classification")

    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        with st.form(key="mlform"):
            col1, col2 = st.columns([2, 1])
            with col1:
                message = st.text_area("Enter message for classification")
                submit_message = st.form_submit_button(label="Predict")

            with col2:
                st.write("Scam Detection Model")
                st.write("Classify text as Scam or Legitimate")

        if submit_message:
            # Call FastAPI to classify the text
            response = requests.post(
                FASTAPI_URL, params={"input": message}, verify=False
            )

            if response.status_code == 200:
                result = response.json()
                prediction = result["label"]
                probability = result["score"]
                postdate = datetime.now().isoformat()

                # Add Data to Database
                add_data(message, prediction, probability, postdate)

                st.success("Prediction Submitted")

                # Display the prediction and probability
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.info("Original Text")
                    st.write(message)

                    st.success("Prediction")
                    st.write(prediction)

                with res_col2:
                    st.info("Probability")
                    st.write(probability)

            else:
                st.error("Error with classification API")

    elif choice == "Manage":
        st.subheader("Manage & Monitor Results")
        stored_data = view_all_data()
        new_df = pd.DataFrame(
            stored_data, columns=["message", "prediction", "probability", "postdate"]
        )
        st.dataframe(new_df)

        new_df["postdate"] = pd.to_datetime(new_df["postdate"])

        min_prob = new_df["probability"].min()
        max_prob = new_df["probability"].max()

        # Visualization with Dynamic Y-Axis Range
        chart = (
            alt.Chart(new_df)
            .mark_line()
            .encode(
                x=alt.X("postdate:T", axis=alt.Axis(format="%Y-%m-%d %H:%M:%S")),
                y=alt.Y("probability:Q", scale=alt.Scale(domain=[min_prob, max_prob])),
            )
            .properties(width=800, height=400)
        )
        st.altair_chart(chart)

        with st.expander("Prediction Distribution"):
            fig2 = plt.figure()
            sns.countplot(x="prediction", data=new_df)
            st.pyplot(fig2)

    else:
        st.subheader("About")
        st.write("""
            This is a text classification app that uses a transformer-based model to classify input text as 'Scam' or 'Legitimate'.
            The app communicates with a FastAPI backend to handle classification requests and stores the results in a SQLite database.
        """)


if __name__ == "__main__":
    main()
