import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# FreightRisk V2 Portfolio App
# Capstone Summary + Client View
# ============================================================

st.set_page_config(
    page_title="FreightRisk V2",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# Styling
# ------------------------------------------------------------

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: Georgia, "Times New Roman", serif;
        color: #211713;
        font-size: 20px;
    }

    .stApp {
        background: #F4E9DD;
    }

    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 4rem;
        max-width: 1320px;
    }

    h1, h2, h3 {
        letter-spacing: -0.025em;
        color: #211713;
        font-family: Georgia, "Times New Roman", serif;
    }

    p, li, div {
        font-size: 1.02rem;
    }

    .hero {
        width: 100%;
        padding: 44px 46px;
        border-radius: 0px;
        background: #4A2A1F;
        color: #FFF8F0;
        margin-bottom: 38px;
        border: none;
        box-shadow: none;
        animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(12px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .hero-kicker {
        text-transform: uppercase;
        font-size: 0.82rem;
        letter-spacing: 0.18em;
        color: #E7C3A6;
        margin-bottom: 14px;
        font-weight: 700;
    }

    .hero-title {
        font-size: 3.25rem;
        line-height: 1.05;
        font-weight: 700;
        letter-spacing: -0.045em;
        margin-bottom: 18px;
        color: #FFF8F0;
        font-family: Georgia, "Times New Roman", serif;
    }

    .hero-copy {
        font-size: 1.16rem;
        line-height: 1.75;
        max-width: 1050px;
        color: #FBE7D2;
        margin-bottom: 26px;
    }

    .hero-badges {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 12px;
    }

    .badge {
        padding: 9px 13px;
        border-radius: 0px;
        background: #6B3F2F;
        color: #FFF8F0;
        border: none;
        font-size: 0.90rem;
        font-weight: 600;
    }

    .section-card {
        width: 100%;
        background: #FFF8F0;
        border-top: 2px solid #4A2A1F;
        border-bottom: 1px solid rgba(74, 42, 31, 0.22);
        border-left: none;
        border-right: none;
        border-radius: 0px;
        padding: 34px 8px 38px 8px;
        box-shadow: none;
        margin: 0 0 44px 0;
        animation: revealOnScroll linear both;
        animation-timeline: view();
        animation-range: entry 0% cover 30%;
    }

    @keyframes revealOnScroll {
        from {
            opacity: 0;
            transform: translateY(24px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .mini-title {
        font-size: 0.86rem;
        color: #7C432D;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .callout {
        border-radius: 0px;
        padding: 18px 20px;
        margin: 22px 0;
        font-size: 1.02rem;
        line-height: 1.65;
        border-left: 5px solid #7C432D;
        border-top: none;
        border-right: none;
        border-bottom: none;
        box-shadow: none;
        background: #EFE0D2;
        color: #2E201A;
    }

    .callout-dark {
        background: #4A2A1F;
        color: #FFF8F0;
        border-left: 5px solid #C89A75;
    }

    .callout-label {
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-weight: 700;
        margin-bottom: 8px;
        color: #7C432D;
    }

    .callout-dark .callout-label {
        color: #E7C3A6;
    }

    [data-testid="stMetric"] {
        background: #FFF8F0;
        padding: 10px 5px;
        border-radius: 0px;
        border: 1px solid rgba(74, 42, 31, 0.20);
        box-shadow: none;
    }

    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #5E463B;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.95rem;
        font-weight: 700;
        color: #2E201A;
        font-family: Georgia, "Times New Roman", serif;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 0px;
        overflow: hidden;
        border: 1px solid rgba(74, 42, 31, 0.18);
    }

    section[data-testid="stSidebar"] {
        background: #EFE0D2;
        border-right: 1px solid rgba(74, 42, 31, 0.18);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(74, 42, 31, 0.25);
    }

    .stTabs [data-baseweb="tab"] {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.02rem;
        padding: 12px 16px;
    }

    .footer-note {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

FINAL_V2_FOLDER = Path("finalv2_outputs")
TABLE_FOLDER = FINAL_V2_FOLDER / "tables"

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def callout(label, text, dark=False):
    class_name = "callout callout-dark" if dark else "callout"
    st.markdown(
        f"""
        <div class="{class_name}">
            <div class="callout-label">{label}</div>
            <div>{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def style_plot(fig):
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="rgba(255,248,240,0)",
        paper_bgcolor="rgba(255,248,240,0)",
        font=dict(family='Georgia, "Times New Roman", serif', color="#211713", size=15),
        title_font=dict(color="#211713", size=20),
        legend_title_font=dict(color="#211713"),
        legend_font=dict(color="#211713"),
        xaxis=dict(
            title_font=dict(color="#211713", size=16),
            tickfont=dict(color="#5E463B", size=14),
            gridcolor="rgba(74,42,31,0.14)"
        ),
        yaxis=dict(
            title_font=dict(color="#211713", size=16),
            tickfont=dict(color="#5E463B", size=14),
            gridcolor="rgba(74,42,31,0.14)"
        ),
        margin=dict(l=20, r=20, t=62, b=34)
    )
    return fig


def read_csv_required(file_name):
    path = TABLE_FOLDER / file_name
    if not path.exists():
        st.error(f"Missing required file: {path}")
        st.stop()
    return pd.read_csv(path)


def find_column(df, options):
    for col in options:
        if col in df.columns:
            return col
    return None


# ------------------------------------------------------------
# Load final V2 exported outputs
# ------------------------------------------------------------

model_comparison = read_csv_required("website_model_comparison.csv")
ensemble_comparison = read_csv_required("website_ensemble_comparison.csv")
risk_band_summary = read_csv_required("website_risk_band_summary.csv")
sample_scored_orders = read_csv_required("website_sample_scored_orders.csv")

if "test_f1" not in model_comparison.columns and (TABLE_FOLDER / "model_comparison_final.csv").exists():
    model_comparison = read_csv_required("model_comparison_final.csv")

if "test_f1" not in ensemble_comparison.columns and (TABLE_FOLDER / "ensemble_comparison_summary.csv").exists():
    ensemble_comparison = read_csv_required("ensemble_comparison_summary.csv")


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

st.sidebar.markdown("## FreightRisk")
st.sidebar.caption("Capstone summary + client demo")

view_mode = st.sidebar.radio(
    "Display mode",
    ["Capstone Summary", "Client View"],
    index=0
)

# ------------------------------------------------------------
# Hero
# ------------------------------------------------------------

if view_mode == "Capstone Summary":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Capstone Summary</div>
            <div class="hero-title">FreightRisk: Freight Risk Modeling and Decision Support</div>
            <div class="hero-copy">
                FreightRisk turns supply chain logistics data into a constraint-aware freight risk model.
                It includes EDA-driven target creation, 9+ model families, threshold tuning, voting ensembles,
                stacking, final model selection, and risk-band interpretation.
            </div>
            
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Client-Facing Product Demo</div>
            <div class="hero-title">FreightRisk: Prioritize Freight Exceptions Before They Ship</div>
            <div class="hero-copy">
                FreightRisk scores order-level freight risk and turns model predictions into a planner-ready review queue.
                It helps teams focus on Critical and High-risk orders instead of manually checking everything.
            </div>
            <div class="hero-badges">
                <div class="badge">Planner review queue</div>
                <div class="badge">Critical order detection</div>
                <div class="badge">KPI summary</div>
                <div class="badge">Business-friendly risk bands</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# Capstone Summary
# ------------------------------------------------------------

if view_mode == "Capstone Summary":

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Motivation + EDA",
        "Model Comparison",
        "Ensembles",
        "Final Selection",
        "Risk Bands"
    ])

    with tab1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="mini-title">Problem Framing</div>', unsafe_allow_html=True)

        st.write(
            """
            The dataset is a single-day supply chain snapshot, so the project is not framed as time-series forecasting.
            Instead, FreightRisk predicts whether an order is freight-infeasible or likely to require freight review.
            """
        )

        callout(
            "Target definition",
            "1 = freight infeasible or high-risk. 0 = freight feasible.",
            dark=True
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Orders analyzed", "9,215")
        c2.metric("Infeasible orders", "2,224")
        c3.metric("Infeasible rate", "24.13%")
        c4.metric("Known issues explained", "99.73%")

        st.write(
            """
            EDA showed that freight infeasibility was not random. It was concentrated in specific freight coverage
            problems and plant-route constraints. This shaped the final project into a freight risk and routing
            decision-support system.
            """
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="mini-title">All Model Results</div>', unsafe_allow_html=True)

        st.write(
            """
            Models are ranked by held-out test F1 for the infeasible freight class.
            F1 is used because the project needs to balance false alarms against missed freight failures.
            """
        )

        model_ranked = model_comparison.sort_values("test_f1", ascending=False).reset_index(drop=True)
        st.dataframe(model_ranked, use_container_width=True, hide_index=True)

        fig = px.bar(
            model_ranked.sort_values("test_f1", ascending=True),
            x="test_f1",
            y="model_name",
            orientation="h",
            title="Model Comparison by Held-Out Test F1",
            labels={"test_f1": "Test F1", "model_name": "Model"},
            color="model_family" if "model_family" in model_ranked.columns else None,
            color_discrete_sequence=["#4A2A1F", "#6B3F2F", "#8A533D", "#B57752", "#D9A178"]
        )
        st.plotly_chart(style_plot(fig), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        left, right = st.columns(2)

        with left:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="mini-title">Precision and Recall Tradeoff</div>', unsafe_allow_html=True)

            fig_pr = px.scatter(
                model_ranked,
                x="test_recall",
                y="test_precision",
                size="test_f1",
                color="model_name",
                hover_name="model_name",
                title="Precision vs Recall by Model",
                labels={"test_recall": "Recall", "test_precision": "Precision"},
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_pr.update_xaxes(range=[0, 1.02])
            fig_pr.update_yaxes(range=[0, 1.02])
            st.plotly_chart(style_plot(fig_pr), use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="mini-title">Error Type Comparison</div>', unsafe_allow_html=True)

            top_error = model_ranked.head(8)
            fig_err = go.Figure()
            fig_err.add_trace(go.Bar(
                x=top_error["model_name"],
                y=top_error["false_positive"],
                name="False Positives"
            ))
            fig_err.add_trace(go.Bar(
                x=top_error["model_name"],
                y=top_error["false_negative"],
                name="False Negatives"
            ))
            fig_err.update_layout(
                barmode="group",
                title="False Positives vs False Negatives",
                xaxis_title="Model",
                yaxis_title="Order Count"
            )
            st.plotly_chart(style_plot(fig_err), use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="mini-title">Ensemble Modeling</div>', unsafe_allow_html=True)

        st.write(
            """
            Three ensemble strategies were tested: equal soft voting, validation-tuned weighted voting, and stacking.
            Stacking was the strongest ensemble.
            """
        )

        ensemble_ranked = ensemble_comparison.sort_values("test_f1", ascending=False).reset_index(drop=True)
        st.dataframe(ensemble_ranked, use_container_width=True, hide_index=True)

        fig = px.bar(
            ensemble_ranked.sort_values("test_f1", ascending=True),
            x="test_f1",
            y="model_name",
            orientation="h",
            title="Ensemble Comparison by Test F1",
            labels={"test_f1": "Test F1", "model_name": "Ensemble"},
            color="ensemble_type" if "ensemble_type" in ensemble_ranked.columns else None,
            color_discrete_sequence=["#4A2A1F", "#8A533D", "#D9A178"]
        )
        fig.update_xaxes(range=[0.93, 0.965])
        st.plotly_chart(style_plot(fig), use_container_width=True)

        callout(
            "",
            "The ensemble section includes more than basic voting. It uses validation-selected weights and stacking with a meta-model.",
            dark=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="mini-title">Final Model Selection</div>', unsafe_allow_html=True)

        final_candidates = model_comparison[
            model_comparison["model_name"].isin(["Gradient Boosting", "Stacking Ensemble", "Random Forest"])
        ].copy()

        st.dataframe(final_candidates.sort_values("test_f1", ascending=False), use_container_width=True, hide_index=True)

        gb = final_candidates[final_candidates["model_name"] == "Gradient Boosting"].iloc[0]
        stack = final_candidates[final_candidates["model_name"] == "Stacking Ensemble"].iloc[0]
        rf = final_candidates[final_candidates["model_name"] == "Random Forest"].iloc[0]

        c1, c2, c3 = st.columns(3)
        c1.metric("Primary final model", "Gradient Boost", f"F1 {gb['test_f1']:.3f}")
        c2.metric("Best ensemble", "Stacking", f"F1 {stack['test_f1']:.3f}")
        c3.metric("High-recall backup", "Random Forest", f"Recall {rf['test_recall']:.3f}")

        callout(
            "Final decision",
            "Gradient Boosting is selected as the final leading model. Stacking is the strongest ensemble. Random Forest is the high-recall backup.",
            dark=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="mini-title">Risk Band Validation</div>', unsafe_allow_html=True)

        st.write(
            """
            The final model converts freight-risk probabilities into Low, Medium, High, and Critical bands.
            This makes the model output easier for planners to use.
            """
        )

        st.dataframe(risk_band_summary, use_container_width=True, hide_index=True)

        fig = px.bar(
            risk_band_summary,
            x="risk_band",
            y="actual_infeasible_rate",
            text=risk_band_summary["actual_infeasible_rate"].map(lambda x: f"{x:.1%}"),
            title="Actual Infeasible Rate by Predicted Risk Band",
            labels={"risk_band": "Risk Band", "actual_infeasible_rate": "Actual Infeasible Rate"},
            color="risk_band",
            color_discrete_sequence=["#D9A178", "#B57752", "#8A533D", "#4A2A1F"]
        )
        fig.update_traces(textposition="outside")
        fig.update_yaxes(range=[0, 1.08])
        st.plotly_chart(style_plot(fig), use_container_width=True)

        callout(
            "Interpretation",
            "The Critical band has a 99.60% actual infeasible rate, while the Low band has only 1.04%. This confirms that the risk bands are meaningful for operational prioritization.",
            dark=True
        )

        st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------
# Client View
# ------------------------------------------------------------

else:

    tab1, tab2, tab3, tab4 = st.tabs([
        "Executive Snapshot",
        "Risk Bands",
        "Planner Queue",
        "Business Value"
    ])

    with tab1:
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Orders scored", f"{len(sample_scored_orders):,}")
        c2.metric("Final model F1", "0.958")
        c3.metric("Critical risk accuracy", "99.6%")
        c4.metric("Best ensemble F1", "0.957")

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="mini-title">Executive Summary</div>', unsafe_allow_html=True)

        st.write(
            """
            FreightRisk helps logistics teams identify orders that are likely to fail freight coverage.
            Instead of manually reviewing every order, planners can focus on the highest-risk orders first.
            """
        )

        callout(
            "Client-ready takeaway",
            "FreightRisk converts model probabilities into Low, Medium, High, and Critical risk bands so freight planners can prioritize exceptions.",
            dark=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        left, right = st.columns([1.1, 0.9])

        with left:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="mini-title">Order Count by Risk Band</div>', unsafe_allow_html=True)

            fig = px.bar(
                risk_band_summary,
                x="risk_band",
                y="order_count",
                text="order_count",
                title="Orders by FreightRisk Band",
                labels={"risk_band": "Risk Band", "order_count": "Orders"},
                color="risk_band",
                color_discrete_sequence=["#D9A178", "#B57752", "#8A533D", "#4A2A1F"]
            )
            fig.update_traces(textposition="outside")
            st.plotly_chart(style_plot(fig), use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="mini-title">Failure Rate by Risk Band</div>', unsafe_allow_html=True)

            fig = px.line(
                risk_band_summary,
                x="risk_band",
                y="actual_infeasible_rate",
                markers=True,
                title="Actual Failure Rate by Risk Band",
                labels={"risk_band": "Risk Band", "actual_infeasible_rate": "Actual Infeasible Rate"},
                color_discrete_sequence=["#4A2A1F"]
            )
            fig.update_yaxes(range=[0, 1.05])
            st.plotly_chart(style_plot(fig), use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        st.dataframe(risk_band_summary, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="mini-title">Planner Review Queue</div>', unsafe_allow_html=True)

        if "risk_band" not in sample_scored_orders.columns:
            st.warning("risk_band column not found in sample scored orders.")
            st.dataframe(sample_scored_orders.head(50), use_container_width=True, hide_index=True)
        else:
            band_order = ["Critical", "High", "Medium", "Low"]
            available_bands = [band for band in band_order if band in sample_scored_orders["risk_band"].dropna().unique()]

            selected_bands = st.multiselect(
                "Filter by risk band",
                options=available_bands,
                default=available_bands[:3]
            )

            filtered = sample_scored_orders[sample_scored_orders["risk_band"].isin(selected_bands)].copy()

            sort_col = "predicted_risk_probability"
            if sort_col in filtered.columns:
                filtered = filtered.sort_values(sort_col, ascending=False)

            st.write(f"Showing {len(filtered):,} orders.")

            display_cols = [
                col for col in [
                    "origin_port",
                    "plant_code",
                    "plant_origin",
                    "unit_quantity",
                    "weight",
                    "actual_freight_infeasible",
                    "predicted_risk_probability",
                    "predicted_freight_infeasible",
                    "risk_band"
                ] if col in filtered.columns
            ]

            st.dataframe(filtered[display_cols].head(100), use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="mini-title">Business Value</div>', unsafe_allow_html=True)

        st.markdown(
            """
            FreightRisk supports freight operations in four ways:

            1. **Prioritize exceptions:** Critical and High-risk orders move to the top of the review queue.
            2. **Reduce missed failures:** The model catches most freight-infeasible orders before shipment planning.
            3. **Make risk explainable:** Risk bands and model comparison make the system easier to trust.
            4. **Support scalable review:** Planners no longer need to inspect every order with the same level of effort.
            """
        )

        callout(
            "Business conclusion",
            "FreightRisk is a decision-support layer for freight coverage review, not just a classification model.",
            dark=True
        )

        st.markdown('</div>', unsafe_allow_html=True)