import pandas as pd
import pytest
from src.demo_data import generate_demo_dataset
from src.preprocessing import normalize_frame_columns, align_features, find_missing_features
from src.risk_assessment import assess_risk
from src.train_model import _clean_data, _train_mode
from src.predict import predict_dataframe, DetectionSettings

def test_demo_data_has_expected_columns():
    frame=generate_demo_dataset(100,seed=7)
    assert len(frame)==100
    assert "Label" in frame
    assert set(frame["Label"]).issubset({"BENIGN","DoS"})

def test_normalize_and_align_features():
    frame=pd.DataFrame({" Flow Duration ":[1,float("inf"),"bad"]})
    assert normalize_frame_columns(frame).columns.tolist()==["flow_duration"]
    assert find_missing_features(frame,["flow_duration"])==[]
    aligned=align_features(frame,["flow_duration"])
    assert aligned["flow_duration"].isna().sum()==2

def test_missing_features_raise():
    with pytest.raises(ValueError):
        align_features(pd.DataFrame({"wrong":[1]}),["flow_duration"])

def test_risk_score_is_bounded():
    score,level=assess_risk("DoS",0.9,0.8,True)
    assert 0<=score<=100
    assert level in {"LOW","MEDIUM","HIGH","CRITICAL"}

def test_train_and_predict(tmp_path):
    frame=generate_demo_dataset(300,seed=13)
    X,y,_,label=_clean_data(frame,"Label")
    bundle=_train_mode(X,y,"binary",tmp_path,"synthetic test",label,42,.2)
    result=predict_dataframe(frame.drop(columns=["Label"]).head(10),bundle,DetectionSettings())
    assert len(result.results)==10
    assert set(result.results["status"]).issubset({"BENIGN","ATTACK"})
