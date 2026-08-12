import json

import pandas as pd
from dotenv import load_dotenv
import requests
import streamlit as st

load_dotenv()


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="📊",
    layout="wide",
)

import os

DEFAULT_API_URL =  os.getenv("API_URL", "http://localhost:8000")


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def get_headers(api_key: str) -> dict:
    """Build headers for authenticated API requests."""
    if not api_key:
        return {}

    return {
        "X-API-Key": api_key,
    }


def handle_response(response: requests.Response):
    """Return JSON response or show an API error."""
    if response.ok:
        try:
            return response.json()
        except ValueError:
            return response.text

    try:
        error = response.json()
    except ValueError:
        error = response.text

    st.error(
        f"API request failed ({response.status_code}): "
        f"{error}"
    )
    return None


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.title("⚙️ Configuration")

api_url = st.sidebar.text_input(
    "API Base URL",
    value=DEFAULT_API_URL,
).rstrip("/")

api_key = st.sidebar.text_input(
    "API Key",
    type="password",
)

headers = get_headers(api_key)


# ---------------------------------------------------------
# Main title
# ---------------------------------------------------------

st.title("📊 Customer Analytics Dashboard")
st.caption("Streamlit frontend for the Customer API")


# ---------------------------------------------------------
# Navigation
# ---------------------------------------------------------

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Health",
        "👥 Customers",
        "📈 KPIs",
        "🤖 Predict",
        "📊 Model Metrics",
    ],
)


# =========================================================
# HEALTH
# =========================================================

if page == "🏠 Health":
    st.header("API Health")

    if st.button("Check API Health", type="primary"):
        try:
            response = requests.get(
                f"{api_url}/health",
                timeout=10,
            )

            data = handle_response(response)

            if data is not None:
                if data.get("status") == "ok":
                    st.success("API is healthy ✅")
                else:
                    st.warning("API responded, but status is not OK.")

                st.json(data)

        except requests.RequestException as exc:
            st.error(f"Could not connect to API: {exc}")


# =========================================================
# CUSTOMERS
# =========================================================

elif page == "👥 Customers":
    st.header("Customers")

    col1, col2 = st.columns(2)

    with col1:
        page_number = st.number_input(
            "Page number",
            min_value=0,
            value=0,
            step=1,
        )

    with col2:
        page_size = st.number_input(
            "Page size",
            min_value=1,
            value=100,
            step=10,
        )

    st.caption(
        f"Request: `/customers?page={page_number}&size={page_size}`"
    )

    if st.button("Load Customers", type="primary"):
        try:
            response = requests.get(
                f"{api_url}/customers",
                params={
                    "page": page_number,
                    "size": page_size,
                },
                headers=headers,
                timeout=30,
            )

            data = handle_response(response)

            if data is not None:
                if isinstance(data, list):
                    st.success(
                        f"Loaded {len(data)} customers"
                    )

                    if data:
                        df = pd.DataFrame(data)

                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True,
                        )

                        # Download button
                        csv = df.to_csv(index=False)

                        st.download_button(
                            "⬇️ Download CSV",
                            data=csv,
                            file_name=f"customers_page_{page_number}.csv",
                            mime="text/csv",
                        )
                    else:
                        st.info("No customers found for this page.")
                else:
                    st.json(data)

        except requests.RequestException as exc:
            st.error(f"Could not connect to API: {exc}")


# =========================================================
# KPIs
# =========================================================

elif page == "📈 KPIs":
    st.header("Key Performance Indicators")

    if st.button("Load KPIs", type="primary"):
        try:
            response = requests.get(
                f"{api_url}/kpis",
                headers=headers,
                timeout=30,
            )

            data = handle_response(response)

            if data is not None:
                st.subheader("KPI Summary")

                if isinstance(data, dict):
                    # Display numeric KPIs as metrics
                    numeric_items = {
                        key: value
                        for key, value in data.items()
                        if isinstance(value, (int, float))
                    }

                    if numeric_items:
                        columns = st.columns(
                            min(len(numeric_items), 4)
                        )

                        for index, (key, value) in enumerate(
                            numeric_items.items()
                        ):
                            columns[index % len(columns)].metric(
                                label=key.replace("_", " ").title(),
                                value=value,
                            )

                    st.divider()

                with st.expander("Raw API Response"):
                    st.json(data)

        except requests.RequestException as exc:
            st.error(f"Could not connect to API: {exc}")


# =========================================================
# PREDICTION
# =========================================================

elif page == "🤖 Predict":
    st.header("Customer Churn Prediction")

    st.info(
        "Enter the fields required by CustomerPredictionRequest. "
        "The JSON below is sent directly to POST /predict."
    )

    default_prediction = {
        # Replace these with the actual fields from
        # CustomerPredictionRequest.
        #
        # Example:
        # "tenure": 12,
        # "monthly_charges": 75.50,
        # "contract": "Month-to-month",
    }

    prediction_json = st.text_area(
        "Prediction Request JSON",
        value=json.dumps(
            default_prediction,
            indent=2,
        ),
        height=300,
    )

    if st.button("Run Prediction", type="primary"):
        try:
            payload = json.loads(prediction_json)

        except json.JSONDecodeError as exc:
            st.error(f"Invalid JSON: {exc}")
            st.stop()

        try:
            response = requests.post(
                f"{api_url}/predict",
                json=payload,
                headers=headers,
                timeout=60,
            )

            data = handle_response(response)

            if data is not None:
                st.subheader("Prediction Result")

                if isinstance(data, dict):
                    probability = data.get(
                        "churn_probability"
                    )

                    prediction = data.get(
                        "churn_prediction"
                    )

                    if probability is not None:
                        try:
                            probability_float = float(
                                probability
                            )

                            st.metric(
                                "Churn Probability",
                                f"{probability_float:.2%}",
                            )

                            st.progress(
                                min(
                                    max(
                                        probability_float,
                                        0.0,
                                    ),
                                    1.0,
                                )
                            )

                        except (ValueError, TypeError):
                            st.write(
                                "Churn Probability:",
                                probability,
                            )

                    if prediction is not None:
                        if prediction:
                            st.error(
                                "⚠️ Customer predicted to churn"
                            )
                        else:
                            st.success(
                                "✅ Customer predicted not to churn"
                            )

                    st.divider()

                st.json(data)

        except requests.RequestException as exc:
            st.error(f"Could not connect to API: {exc}")


# =========================================================
# MODEL METRICS
# =========================================================

elif page == "📊 Model Metrics":
    st.header("Model Metrics")

    if st.button("Load Model Metrics", type="primary"):
        try:
            response = requests.get(
                f"{api_url}/model-metrics",
                headers=headers,
                timeout=30,
            )

            data = handle_response(response)

            if data is not None:
                if isinstance(data, dict):
                    columns = st.columns(
                        min(len(data), 4)
                    )

                    for index, (key, value) in enumerate(
                        data.items()
                    ):
                        columns[index % len(columns)].metric(
                            label=key.replace(
                                "_",
                                " ",
                            ).title(),
                            value=(
                                f"{value:.4f}"
                                if isinstance(
                                    value,
                                    float,
                                )
                                else value
                            ),
                        )

                    st.divider()

                st.subheader("Raw Metrics")
                st.json(data)

        except requests.RequestException as exc:
            st.error(f"Could not connect to API: {exc}")


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.sidebar.divider()
st.sidebar.caption(
    "Customer Analytics • FastAPI + Streamlit"
)