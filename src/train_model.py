"""Train a baseline model on labelled network-flow CSV data or synthetic demo data."""
from pathlib import Path
import argparse
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from src.demo_data import generate_demo_dataset

def _clean_data(frame, label_column="Label"):
    df = frame.copy()
    labels = next((c for c in df.columns if str(c).strip().lower() == str(label_column).strip().lower()), None)
    if labels is None:
        raise ValueError(f"Label column {label_column!r} was not found.")
    y = df[labels].astype(str).str.strip()
    X = df.drop(columns=[labels]).apply(pd.to_numeric, errors="coerce")
    X = X.replace([float("inf"),float("-inf")],float("nan"))
    keep = y.ne("") & y.notna()
    X,y = X.loc[keep],y.loc[keep]
    X = X.loc[:,X.notna().any()]
    if X.empty or y.nunique()<2:
        raise ValueError("Training requires numeric features and at least two label classes.")
    return X,y,df,labels

def _train_mode(X,y,mode,output_dir,label_source="CSV",label_column="Label",seed=42,test_size=.2,*args):
    if mode not in {"binary","multiclass"}:
        raise ValueError("mode must be binary or multiclass")
    yfit = y.map(lambda v:"BENIGN" if str(v).strip().upper()=="BENIGN" else "ATTACK") if mode=="binary" else y
    X_train,X_test,y_train,y_test=train_test_split(X,yfit,test_size=test_size,random_state=seed,stratify=yfit)
    model=make_pipeline(SimpleImputer(strategy="median",keep_empty_features=True),RandomForestClassifier(n_estimators=120,random_state=seed,class_weight="balanced",n_jobs=-1))
    model.fit(X_train,y_train)
    metrics={"accuracy":float(accuracy_score(y_test,model.predict(X_test))),"report":classification_report(y_test,model.predict(X_test),output_dict=True,zero_division=0),"demo_or_data":label_source}
    bundle={"model":model,"features":list(X.columns),"metadata":{"mode":mode,"label_column":label_column,"metrics":metrics,"label_source":label_source}}
    Path(output_dir).mkdir(parents=True,exist_ok=True)
    joblib.dump(bundle,Path(output_dir)/f"{mode}_model.joblib")
    return bundle

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--demo",action="store_true")
    p.add_argument("--data",default="data")
    p.add_argument("--mode",choices=["binary","multiclass","both"],default="both")
    p.add_argument("--label-column",default="Label")
    p.add_argument("--sample-size",type=int,default=0)
    p.add_argument("--output-dir",default="models")
    args=p.parse_args()
    if args.demo:
        df=generate_demo_dataset(3000)
        source="SYNTHETIC DEMO DATA — not real-world validation"
    else:
        paths=list(Path(args.data).rglob("*.csv"))
        if not paths: raise SystemExit(f"No CSV files found under {args.data}. Use --demo to test the workflow.")
        df=pd.concat([pd.read_csv(path,low_memory=False) for path in paths],ignore_index=True)
        if args.sample_size and len(df)>args.sample_size: df=df.sample(args.sample_size,random_state=42)
        source="user-provided labelled CSV data"
    X,y,_,label=_clean_data(df,args.label_column)
    for mode in (["binary","multiclass"] if args.mode=="both" else [args.mode]):
        bundle=_train_mode(X,y,mode,args.output_dir,source,label,42,.2)
        print(f"{mode}: held-out accuracy={bundle['metadata']['metrics']['accuracy']:.3f} ({source})")
if __name__=="__main__": main()
