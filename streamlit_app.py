# streamlit_app.py

import streamlit as st
import requests
import time
import pandas as pd

# Constants
API_URL = "https://medoxz543-hate-endpoint.hf.space/check-text"
HEADERS = {"Content-Type": "application/json"}

# App setup
st.set_page_config(page_title="Hate Speech Detector", page_icon="🧠", layout="wide")
st.title("🧠 Hate Speech Detector")

# Define columns layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Input Texts")
    user_input = st.text_area(
        label="Enter one sentence per line:",
        height=400,
        placeholder="Example:\n- Jews are killers. We should kill them all\n- Have a nice day!"
    )

    detect_button = st.button("🚀 Run Detection")

with col2:
    st.subheader("📊 Prediction Results")
    if detect_button:
        if not user_input.strip():
            st.warning("⚠️ Please enter at least one sentence.")
        else:
            texts = [line.strip() for line in user_input.split("\n") if line.strip()]
            payload = {"texts": texts}

            start_time = time.time()
            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload)
                response.raise_for_status()
                data = response.json()
                elapsed = time.time() - start_time

                st.success(f"✅ Inference completed in {elapsed:.2f} seconds")
                st.markdown(f"🕒 Timestamp: `{data.get('timestamp', 'N/A')}`")

                results_df = pd.DataFrame({
                    "Input": texts,
                    "Score": [round(item["score"], 3) for item in data["results"]],
                    "Prediction": ["🔥 Hateful" if item["blur"] else "✅ Non-Hateful" for item in data["results"]]
                })

                st.dataframe(results_df, use_container_width=True)

            except requests.exceptions.RequestException as e:
                elapsed = time.time() - start_time
                st.error("❌ Failed to reach the API.")
                st.code(str(e), language="text")
                st.write(f"⏱️ Elapsed Time: {elapsed:.2f} seconds")
