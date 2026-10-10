"""Small reusable classification evaluation helpers."""
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

def classification_metrics(y_true, y_pred):
    p,r,f,_ = precision_recall_fscore_support(y_true,y_pred,average="weighted",zero_division=0)
    return {"accuracy":float(accuracy_score(y_true,y_pred)),"precision_weighted":float(p),"recall_weighted":float(r),"f1_weighted":float(f),"confusion_matrix":confusion_matrix(y_true,y_pred).tolist()}
