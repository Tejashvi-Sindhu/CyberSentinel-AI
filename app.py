"""CyberSentinel AI — educational network-flow analysis dashboard."""
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from src.demo_data import generate_demo_dataset
from src.data_loader import read_csv_safe, DataValidationError
from src.predict import load_bundle, predict_dataframe, DetectionSettings

st.set_page_config(page_title="CyberSentinel AI",page_icon="🛡️",layout="wide")
st.title("🛡️ CyberSentinel AI")
st.caption("AI-assisted network-flow triage · Educational project")
st.warning("Demo mode uses synthetic data. Model outputs are triage suggestions, not proof of compromise or real-world accuracy.")
with st.sidebar:
    st.header("Analysis settings")
    mode=st.selectbox("Model type",["binary","multiclass"])
    demo=st.toggle("Use synthetic demo traffic",value=True)
    st.caption("Train models from the VS Code terminal before analysing traffic.")
@st.cache_data
def demo_frame():
    return generate_demo_dataset(2000)
@st.cache_resource
def bundle(mode):
    return load_bundle(mode)
df=None
if demo:
    df=demo_frame().drop(columns=["Label"])
    st.info("Showing synthetic traffic generated for workflow demonstration.")
else:
    upload=st.file_uploader("Upload network-flow CSV",type=["csv"])
    if upload is not None:
        try: df=read_csv_safe(upload)
        except DataValidationError as exc: st.error(str(exc))
if df is not None:
    st.subheader("Traffic preview")
    st.dataframe(df.head(10),use_container_width=True)
    try:
        model=bundle(mode)
        output=predict_dataframe(df,model,DetectionSettings())
        result=pd.concat([df.reset_index(drop=True),output.results.reset_index(drop=True)],axis=1)
        benign=int((result["status"]=="BENIGN").sum())
        attacks=int((result["status"]=="ATTACK").sum())
        c1,c2,c3=st.columns(3)
        c1.metric("Records analysed",f"{len(result):,}")
        c2.metric("Predicted attacks",f"{attacks:,}")
        c3.metric("Predicted benign",f"{benign:,}")
        st.subheader("Prediction distribution")
        counts=result["status"].value_counts().rename_axis("status").reset_index(name="records")
        st.plotly_chart(px.bar(counts,x="status",y="records",color="status",title="Predicted classes"),use_container_width=True)
        st.subheader("Records for review")
        st.dataframe(result.sort_values("risk_score",ascending=False),use_container_width=True)
        st.download_button("Download analysis CSV",result.to_csv(index=False).encode("utf-8"),file_name="cybersentinel_analysis.csv",mime="text/csv")
    except FileNotFoundError:
        st.error("No trained model found. Open the VS Code terminal in the project folder and run: python -m src.train_model --demo --mode both")
    except ValueError as exc:
        st.error(f"Input data does not match the model feature schema: {exc}")
st.divider()
st.caption("CyberSentinel AI is a student project. Validate findings against authorised, representative traffic and independent evidence.")
