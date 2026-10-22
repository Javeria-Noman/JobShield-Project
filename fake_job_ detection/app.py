import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
sys.path.append(str(ROOT / "src"))
from feature_engineering import add_features
from data_preprocessing import ALL_FEATURES

st.set_page_config(page_title="Fake Job Posting Detector", layout="wide")
NONE = "(not specified)"


@st.cache_resource
def load_model():
    return joblib.load(ROOT / "models" / "job_svm.joblib")


@st.cache_data
def load_options():
    df = pd.read_csv(ROOT / "data" / "processed" / "train_fe.csv")
    cols = ["employment_type", "required_experience", "required_education",
            "industry", "function"]
    return {c: [NONE] + sorted(df[c].dropna().unique().tolist()) for c in cols}


def analyse(row, bundle):
    pipe = bundle["pipeline"]
    X = add_features(row)[ALL_FEATURES]
    score = float(pipe.decision_function(X)[0])
    if score >= bundle["hi"]:
        tier = "Potentially Fraudulent"
    elif score <= bundle["lo"]:
        tier = "Likely Legitimate"
    else:
        tier = "Uncertain / Requires Manual Verification"

    prep, clf = pipe.named_steps["prep"], pipe.named_steps["clf"]
    xv = prep.transform(X)
    xv = xv.toarray()[0] if hasattr(xv, "toarray") else xv[0]
    contrib = xv * clf.coef_[0]
    names = prep.get_feature_names_out()
    order = np.argsort(contrib)
    up = [(names[i], contrib[i]) for i in order[::-1][:8] if contrib[i] > 0]
    down = [(names[i], contrib[i]) for i in order[:8] if contrib[i] < 0]
    return score, tier, up, down


def show_signals(title, items):
    st.markdown(f"**{title}**")
    if items:
        st.table(pd.DataFrame(items, columns=["signal", "effect"]).round(3))
    else:
        st.write("None")


page = st.sidebar.radio("Page", ["Home", "Job Posting Analysis",
                                 "Model Performance", "Limitations"])

if page == "Home":
    st.title("Fake Job Posting Detector")
    st.write("A machine-learning screening tool trained on the EMSCAD job-posting "
             "dataset (Kaggle version). It gives a **risk assessment**, not a verdict.")
    st.info("Phase 1 (job postings) is implemented. SMS and URL analysis are planned for Phase 2.")

elif page == "Job Posting Analysis":
    st.title("Job Posting Analysis")
    st.caption("Your text is only passed to the model. No links are opened or fetched.")
    opts = load_options()
    bundle = load_model()

    title = st.text_input("Job title")
    company_profile = st.text_area("Company profile (leave empty if not given)")
    description = st.text_area("Job description", height=200)
    requirements = st.text_area("Requirements")
    benefits = st.text_area("Benefits")
    salary_range = st.text_input("Salary range (leave empty if not given)")

    c1, c2, c3 = st.columns(3)
    telecommuting = c1.checkbox("Remote / telecommuting")
    has_logo = c2.checkbox("Company logo present")
    has_questions = c3.checkbox("Screening questions present")

    cats = {c: st.selectbox(c, opts[c]) for c in opts}

    if st.button("Analyse"):
        if not description.strip():
            st.warning("Please enter a job description.")
        else:
            def val(v):
                return v if str(v).strip() and v != NONE else np.nan

            row = pd.DataFrame([{
                "title": val(title), "company_profile": val(company_profile),
                "description": val(description), "requirements": val(requirements),
                "benefits": val(benefits), "salary_range": val(salary_range),
                "telecommuting": int(telecommuting),
                "has_company_logo": int(has_logo),
                "has_questions": int(has_questions),
                **{c: val(v) for c, v in cats.items()},
            }])
            score, tier, up, down = analyse(row, bundle)

            if tier == "Potentially Fraudulent":
                st.error(f"Result: {tier}")
            elif tier == "Likely Legitimate":
                st.success(f"Result: {tier}")
            else:
                st.warning(f"Result: {tier}")
            st.write(f"Model score: {score:.3f} "
                     f"(thresholds: legitimate <= {bundle['lo']:.3f}, fraudulent >= {bundle['hi']:.3f}). "
                     "This is a score, not a probability.")
            a, b = st.columns(2)
            with a:
                show_signals("Pushed towards fraud", up)
            with b:
                show_signals("Pushed towards legitimate", down)
            st.caption("These are model-based associations learned from the dataset. "
                       "They are not verified facts and do not prove fraud.")

elif page == "Model Performance":
    st.title("Model Performance (held-out test set)")
    res = ROOT / "reports" / "test_results.csv"
    if res.exists():
        st.dataframe(pd.read_csv(res))
    else:
        st.info("Run the notebook cell that saves reports/test_results.csv.")
    tc = ROOT / "reports" / "tier_crosstab.csv"
    if tc.exists():
        st.subheader("Three-tier outcome vs actual label")
        st.dataframe(pd.read_csv(tc))
    st.caption("Accuracy alone is misleading here because only about 5% of postings are fake.")

else:
    st.title("Disclaimer and Limitations")
    st.write(
        "- A prediction never guarantees a job is real or fake.\n"
        "- Missing information alone is not proof of fraud.\n"
        "- The model learned patterns from one older dataset; new scams may look different.\n"
        "- Some top words reflect dataset artifacts, not real scam signals.\n"
        "- Even 'Likely Legitimate' results can be wrong; verify employers independently.\n"
        "- Phone numbers, websites and companies are not verified by this tool."
    )