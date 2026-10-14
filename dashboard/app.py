"""Results-first Phase 10 stakeholder dashboard."""
import re
from pathlib import Path
import pandas as pd
import streamlit as st
try:
    from dashboard.evidence import ROOT, load_evidence, eligible_findings, load_csv, load_source_dataset
    from dashboard.charts import crop_yield_boxplot
except ModuleNotFoundError:
    from evidence import ROOT, load_evidence, eligible_findings, load_csv, load_source_dataset
    from charts import crop_yield_boxplot
try:
    from dashboard.exploration import descriptive_summary, safe_pearson, outlier_flags, numeric_columns
except ModuleNotFoundError:
    from exploration import descriptive_summary, safe_pearson, outlier_flags, numeric_columns

st.set_page_config(page_title="Crop Yield Insights", page_icon="🌾", layout="wide")
st.markdown("""
<style>
.block-container {max-width: 1400px; padding-top: 2rem;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#0b3b5a,#147d92); color:white; margin-bottom:1.2rem;}
.hero h1 {font-size:2.25rem; margin:0 0 .35rem 0;}
.hero p {margin:0; opacity:.9; font-size:1.05rem;}
.insight {padding:1rem 1.1rem; border:1px solid #e6ebef; border-radius:14px; background:#fff; min-height:110px; box-shadow:0 2px 8px rgba(24,50,70,.06);}
.insight h4 {margin:0 0 .35rem 0; color:#0b3b5a;}
.insight p {margin:0; color:#46525a; font-size:.92rem;}
.section-card {padding: .8rem 1rem; border-radius: 14px; background:#f5f9fb; border-left: 4px solid #147d92; margin:.5rem 0 1rem;}
.kpi {background:#ffffff; border:1px solid #e1e9ee; border-radius:16px; padding:1rem 1.1rem; min-height:108px; box-shadow:0 4px 14px rgba(20,55,75,.07);}
.kpi-label {font-size:.78rem; color:#60727d; text-transform:uppercase; letter-spacing:.04em; font-weight:650;}
.kpi-value {font-size:1.42rem; color:#102d3d; font-weight:750; margin-top:.45rem; white-space:nowrap;}
.trace-card {background:#f8fbfc; border:1px solid #dce8ed; border-radius:14px; padding:.85rem 1rem; min-height:74px;}
.trace-label {font-size:.72rem; color:#627782; text-transform:uppercase; letter-spacing:.05em; font-weight:700;}
.trace-value {font-size:1.05rem; color:#123b52; font-weight:700; margin-top:.35rem; white-space:normal;}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#f3f8fa 0%,#edf3f5 100%); border-right:1px solid #dce7eb;}
[data-testid="stSidebar"] [role="radiogroup"] {gap:.25rem;}
[data-testid="stSidebar"] [role="radio"] {padding:.55rem .65rem; border-radius:10px;}
[data-testid="stSidebar"] [role="radio"]:hover {background:#dceff1;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    manifest, findings, decisions, refs = load_evidence()
    register = pd.read_csv(ROOT / "results/analysis_register.csv")
    human_register = pd.read_csv(ROOT / "results/PHASE9_HUMAN_VERIFICATION_REGISTER.csv")
    return manifest, findings, decisions, refs, register, human_register, load_source_dataset()

manifest, findings, decisions, refs, register, human_register, data = get_data()
decisions["Finding_ID"] = decisions["Finding_ID"].astype(str).str.strip()
human_register["Finding_ID"] = human_register["Finding_ID"].astype(str).str.strip()
# Decision-register schemas evolved across phases. Keep the explorer
# backwards-compatible when an older register has no qualification field.
for frame in (decisions, human_register):
    if "Required_Display_Qualification" not in frame.columns:
        frame["Required_Display_Qualification"] = "Qualification not recorded in this register."
eligible = eligible_findings(decisions)
st.sidebar.markdown("## 🌾 Crop Yield BI")
st.sidebar.caption("Results, patterns and evidence")
page = st.sidebar.radio("Navigate", ["Overview", "Business Questions & Insights", "Crop Performance", "Yield Relationships", "Prediction Accuracy", "Explore the Data", "Traditional BI vs GenAI", "How We Analysed the Data", "Analysis Process"])

def evidence(relative, show_warning=True):
    frame = load_csv(relative)
    if frame.attrs.get("evidence_warning") and show_warning: st.info("Some supporting evidence is temporarily unavailable from the primary storage location. See the methodology page for traceability details.")
    return frame

def show_distribution(frame):
    fig = crop_yield_boxplot(frame)
    if fig is not None: st.plotly_chart(fig, width="stretch")
    else: st.bar_chart(frame.groupby("Crop_Type")["Crop_Yield_ton_per_hectare"].mean())

def analysis_context(ids):
    selected = register[register.analysis_id.isin(ids)]
    if selected.empty: return
    st.caption("Formal evidence: " + ", ".join(ids))
    with st.expander("What these Analysis IDs represent"):
        st.dataframe(selected[["analysis_id", "analysis_purpose", "method", "n", "output_location"]], hide_index=True)

if page == "Overview":
    st.markdown('<div class="hero"><h1>Crop Yield Insights</h1><p>Results from the analysed dataset — clear comparisons, relationships and predictive performance.</p></div>', unsafe_allow_html=True)
    summary = data.groupby("Crop_Type")["Crop_Yield_ton_per_hectare"].agg(count="size", mean="mean").reset_index().sort_values("mean", ascending=False)
    m = pd.read_csv(ROOT / "results/model_metrics.csv")
    best = m[(m.Analysis_ID == "A059") & m.holdout_RMSE.notna()]
    benchmark = m[(m.Analysis_ID == "A061") & m.holdout_RMSE.notna()]
    improvement = (1-best.iloc[0].holdout_RMSE/benchmark.iloc[0].holdout_RMSE)*100 if not best.empty and not benchmark.empty else None
    c1, c2, c3, c4 = st.columns(4)
    cards = [("Highest average yield", f"{summary.iloc[0].Crop_Type} · {summary.iloc[0]['mean']:.2f}"), ("Strongest crop association", "Fertiliser · positive"), ("Rainfall correlation", "0.0312 pooled"), ("Gradient boosting vs crop mean", f"{improvement:.1f}% lower RMSE" if improvement is not None else "Stored result unavailable")]
    for col, (label, value) in zip((c1,c2,c3,c4), cards):
        col.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div></div>', unsafe_allow_html=True)
    st.markdown("### What stands out")
    i1,i2,i3 = st.columns(3)
    i1.markdown('<div class="insight"><h4>Crop groups differ</h4><p>Average recorded yield varies substantially across crop groups. This is descriptive, not evidence that crop choice causes the difference.</p></div>', unsafe_allow_html=True)
    i2.markdown('<div class="insight"><h4>Subgroups reveal more</h4><p>Rainfall is more strongly associated with yield within crops than in the pooled data, an aggregation pattern rather than causation.</p></div>', unsafe_allow_html=True)
    i3.markdown('<div class="insight"><h4>Prediction is design-sensitive</h4><p>Several models perform strongly within this dataset, but the ranking changes with evaluation design.</p></div>', unsafe_allow_html=True)
    try:
        import plotly.express as px
        left, right = st.columns(2)
        with left:
            fig = px.bar(summary.sort_values("mean"), x="mean", y="Crop_Type", orientation="h", text="mean", color_discrete_sequence=["#147d92"], title="Average recorded yield by crop")
            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            fig.update_layout(xaxis_title="Recorded yield value", yaxis_title="")
            fig.update_layout(showlegend=False, coloraxis_showscale=False, xaxis_title="Recorded yield value", yaxis_title="")
            st.plotly_chart(fig, width="stretch")
        with right:
            fig = px.box(data, x="Crop_Type", y="Crop_Yield_ton_per_hectare", color="Crop_Type", points=False, title="Yield distribution within each crop")
            fig.update_layout(showlegend=False, xaxis_title="Crop", yaxis_title="Recorded yield value")
            st.plotly_chart(fig, width="stretch")
        st.subheader("Primary prediction comparison")
        models = m[m.Analysis_ID.isin(["A057","A058","A059","A061"]) & m.holdout_RMSE.notna()].drop_duplicates("model")
        fig = px.bar(models.sort_values("holdout_RMSE", ascending=False), x="holdout_RMSE", y="model", orientation="h", text="holdout_RMSE", color="model", title="Lower RMSE means smaller prediction error")
        fig.update_layout(xaxis_title="Holdout RMSE", yaxis_title="Model", showlegend=False)
        st.plotly_chart(fig, width="stretch")
    except ModuleNotFoundError:
        st.warning("Plotly is required for the Overview visualisations. Install it with: python -m pip install plotly==6.3.0")
    st.info("Dataset provenance is UNKNOWN. Units and real-world generalisation are not confirmed.")
elif page == "Business Questions & Insights":
    st.title("Business Questions & Insights")
    st.caption("Evidence-supported answers from the reviewed analytical results. No new AI calculations are performed here.")
    questions = [
        ("BQ1 — Yield relationships and interactions", "Which crop-specific relationships and interactions between fertiliser, irrigation, soil and environmental conditions are most strongly associated with crop yield?", "Within the analysed dataset, crop groups differ descriptively, fertiliser and rainfall show positive crop-specific associations, and the pooled rainfall relationship is much weaker. Tested irrigation comparisons were not statistically significant.", "F001, F002, F003 and F004", "Association is not causation. Non-significance does not establish that irrigation has no effect. Dataset provenance and units remain unknown."),
        ("BQ2 — Crop yield prediction", "How accurately can crop yield be predicted using the available variables, and which variables contribute most to predictive performance?", "Several tested models predict strongly within this dataset. Gradient boosting ranked first under the primary fixed configuration, while linear regression ranked first on average in the independent five-seed evaluation. Crop type, fertiliser use and rainfall were prominent predictive features under the tested Random Forest configuration.", "F006 and F007", "There is no universally best model. Performance is within this dataset and does not establish real-world generalisation or causal importance."),
        ("BQ3 — Reliable GenAI-assisted insights", "Which additional findings identified through the GenAI-assisted workflow are sufficiently reliable, reproducible and interpretable to support further agricultural investigation?", "Six findings were accepted with qualifications after audit, blind replication and human review. F005 was deferred because the Cotton regression specification warning remains unresolved under D017.", "F001–F007; F005 deferred", "Human decisions remain separate from the technical UNVERIFIED status. No agricultural recommendation is made."),
    ]
    for title, question, answer, ids, limitations in questions:
        st.markdown(f'<div class="insight"><h4>{title}</h4><p><b>Question:</b> {question}</p><p><b>Answer:</b> {answer}</p><p><b>Evidence:</b> {ids}</p><p><b>Qualification:</b> {limitations}</p></div>', unsafe_allow_html=True)
        with st.expander(f"Supporting evidence — {title}"):
            ids_list = list(dict.fromkeys(re.findall(r"F\d{3}", ids)))
            st.caption("Select a Finding_ID to inspect its evidence trail.")
            cols = st.columns(min(4, max(1, len(ids_list))))
            for index, fid in enumerate(ids_list):
                if cols[index % len(cols)].button(fid, key=f"bq3_{title}_{fid}", width="stretch"):
                    st.session_state["bq_selected_finding"] = fid
            chosen = st.session_state.get("bq_selected_finding", ids_list[0] if ids_list else None)
            if chosen in ids_list:
                matches = human_register[human_register.Finding_ID.eq(str(chosen).strip())]
                if matches.empty:
                    st.warning("Finding evidence is temporarily unavailable for this selection.")
                    continue
                row = matches.iloc[0]
                source = next((f for f in findings if f["finding_id"] == chosen), None)
                st.markdown(f"#### {chosen}")
                if source: st.write(source["claim"])
                q1, q2, q3 = st.columns(3)
                q1.markdown(f'<div class="trace-card"><div class="trace-label">Original technical status</div><div class="trace-value">{row["Status"]}</div></div>', unsafe_allow_html=True)
                q2.markdown(f'<div class="trace-card"><div class="trace-label">Human decision</div><div class="trace-value">{row["Human_Decision"].replace("_", " ")}</div></div>', unsafe_allow_html=True)
                q3.markdown(f'<div class="trace-card"><div class="trace-label">Analysis IDs</div><div class="trace-value">{row["Analysis_IDs"]}</div></div>', unsafe_allow_html=True)
                if source:
                    st.write("**Numerical evidence:**", source["supporting_result"])
                    st.write("**Limitations:**", source["limitations"])
                evidence_rows = refs[refs.Finding_ID.astype(str).str.contains(chosen)]
                st.write("**Evidence references:**", ", ".join(evidence_rows.Evidence_ID.astype(str)))
                if chosen == "F005": st.warning("F005 is deferred under D017; Cotton coefficient interpretation remains withheld.")
    st.subheader("AI-assisted insights")
    st.markdown("The AI-assisted workflow helped plan analyses, write and review code, identify candidate patterns and prepare explanations. Numerical results came from executable Python and stored evidence; no AI model is called when this page runs.")
    a,b = st.columns(2)
    with a:
        st.markdown('<div class="insight"><h4>Accepted patterns</h4><p>Crop-specific analysis reveals relationships that pooled summaries can conceal. Predictive model rankings are sensitive to evaluation design, so the dashboard preserves both primary and independent results.</p></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="insight"><h4>Further-investigation questions</h4><p>Would independently documented provenance, measurement units and a resolved Cotton specification change how these patterns should be interpreted?</p></div>', unsafe_allow_html=True)
    st.subheader("Deeper Analytical Insights")
    supported, exploratory, further = st.tabs(["Supported insights", "Exploratory insights", "Questions requiring further testing"])
    with supported:
        st.markdown("These are results already covered by the formal analyses, independent checks and Phase 9 human decisions. They retain their qualifications.")
        st.markdown("- Crop-group yield differences are descriptive (F001).\n- Fertiliser and rainfall show positive crop-specific associations (F002–F003).\n- Irrigation comparisons were non-significant, which does not establish no effect (F004).\n- Predictive performance is strong within this dataset, but model rankings depend on design (F006).\n- Random Forest importance is predictive, not causal (F007).\n- F005 remains deferred under D017.")
    with exploratory:
        st.markdown("Patterns calculated from current dashboard filters are exploratory and not independently audited. They should not receive new Finding IDs automatically.")
        st.markdown("- Compare hidden subgroup relationships by crop, soil type, region and irrigation category.\n- Inspect whether variability differs between crops even when averages look similar.\n- Use the EDA workspace to compare rainfall, soil moisture and fertiliser relationships for selected crops.")
        st.info("Use Explore the Data to investigate these patterns. Filtered results remain descriptive.")
    with further:
        st.markdown("These questions are useful next steps, but current evidence is incomplete:")
        st.markdown("- Are the observed relationships stable across hidden subgroups?\n- How reliable are model predictions separately for each crop?\n- Do nonlinear or interaction terms materially improve performance?\n- Does the Cotton specification warning alter coefficient interpretation?\n- How stable are feature-importance rankings across resamples?")
        matrix = pd.DataFrame({"Evidence area": ["Crop relationships", "Irrigation comparisons", "Cotton regression", "Predictive ranking", "Feature importance"], "Current evidence": ["Primary + independent directional support", "Non-significant after corrections", "Deferred; specification warning", "Strong within-dataset; ranking sensitive", "Directional independent support"], "Strength for interpretation": ["Moderate", "Limited", "Insufficient", "Moderate with qualifications", "Moderate with qualifications"]})
        st.dataframe(matrix, hide_index=True)
    st.subheader("What GenAI contributed")
    st.markdown("Compared with the documented traditional BI workflow, GenAI contributed broader analytical planning, interaction and nonlinear sensitivity proposals, reproducible Python implementation, structured evidence traceability, independent-audit preparation and clearer communication. The project does not claim unmeasured time savings or that traditional tools could not perform these methods. Human review remained the final authority.")
    st.info("Traditional BI versus GenAI efficiency claims were not measured and are intentionally reserved for later evaluation.")
elif page == "Crop Performance":
    st.title("Crop performance")
    analysis_context(["A002"])
    st.markdown('<div class="section-card">Use the controls to compare crop populations. These are descriptive summaries of the selected records, not recommendations.</div>', unsafe_allow_html=True)
    summary = data.groupby("Crop_Type")["Crop_Yield_ton_per_hectare"].agg(count="size", mean="mean", median="median", sd="std").reset_index().sort_values("mean", ascending=False)
    choice = st.multiselect("Compare crops", sorted(data.Crop_Type.unique()), default=sorted(data.Crop_Type.unique()))
    selected = data[data.Crop_Type.isin(choice)]
    if selected.empty: st.warning("Select at least one crop.")
    else:
        try:
            import plotly.express as px
            a,b = st.columns(2)
            with a:
                fig = px.bar(summary[summary.Crop_Type.isin(choice)].sort_values("mean"), x="mean", y="Crop_Type", orientation="h", text="mean", color_discrete_sequence=["#147d92"], title="Average recorded yield")
                fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
                fig.update_layout(xaxis_title="Recorded yield value", yaxis_title="")
                st.plotly_chart(fig, width="stretch")
            with b:
                view = st.selectbox("Distribution view", ["Boxplot", "Violin", "Histogram"])
                fig = px.box(selected, x="Crop_Type", y="Crop_Yield_ton_per_hectare", color="Crop_Type", points=False, title="Yield variation") if view == "Boxplot" else px.violin(selected, x="Crop_Type", y="Crop_Yield_ton_per_hectare", color="Crop_Type", box=True, title="Yield variation") if view == "Violin" else px.histogram(selected, x="Crop_Yield_ton_per_hectare", color="Crop_Type", nbins=35, title="Yield distribution")
                st.plotly_chart(fig, width="stretch")
        except ModuleNotFoundError: show_distribution(selected)
        st.dataframe(summary[summary.Crop_Type.isin(choice)], hide_index=True)
    st.caption("Descriptive comparison only; it does not establish crop superiority or causation.")
elif page == "Yield Relationships":
    st.title("Yield relationships")
    analysis_context(["A004","A005","A006","A007","A008","A009","A016","A017","A018","A019","A020","A021","A022","A010","A011","A012","A013","A014","A015"])
    st.markdown("Rainfall has a stronger association with yield when crops are examined separately than when all crops are pooled. This is an aggregation pattern, not causation.")
    rainfall = evidence("results/baseline_details/A017_A022_crop_rainfall_correlations.csv", show_warning=False)
    fertiliser = evidence("results/baseline_details/A004_A009_crop_fertilizer_correlations.csv", show_warning=False)
    try:
        import plotly.express as px
        left, right = st.columns(2)
        with left:
            if not rainfall.empty:
                rcol = next((c for c in rainfall.columns if c.lower() in {"r", "correlation", "estimate"}), rainfall.columns[-1])
                cropcol = next((c for c in rainfall.columns if "crop" in c.lower()), rainfall.columns[0])
                st.plotly_chart(px.bar(rainfall.sort_values(rcol), x=rcol, y=cropcol, orientation="h", color=rcol, color_continuous_scale="Teal", title="Rainfall–yield association by crop"), width="stretch")
        with right:
            if not fertiliser.empty:
                fcol = next((c for c in fertiliser.columns if c.lower() in {"r", "correlation", "estimate"}), fertiliser.columns[-1])
                cropcol = next((c for c in fertiliser.columns if "crop" in c.lower()), fertiliser.columns[0])
                st.plotly_chart(px.bar(fertiliser.sort_values(fcol), x=fcol, y=cropcol, orientation="h", color=fcol, color_continuous_scale="Sunset", title="Fertiliser–yield association by crop"), width="stretch")
        st.subheader("Pooled versus within-crop rainfall")
        pooled = pd.DataFrame({"Estimate": [0.0312, float(rainfall[rcol].mean()) if not rainfall.empty else 0], "View": ["Pooled", "Average crop-specific"]})
        st.plotly_chart(px.bar(pooled, x="Estimate", y="View", orientation="h", color="View", title="Why subgroup analysis matters"), width="stretch")
        st.caption("The pooled relationship is weak, while crop-specific relationships are stronger. Correlation is association, not proof of a causal response.")
    except ModuleNotFoundError:
        st.warning("Plotly is required for relationship charts. Install plotly==6.3.0.")
    st.caption("Positive correlation describes association, not proof that increasing fertiliser causes higher yield.")
    st.subheader("Irrigation comparison")
    st.info("The tests did not detect statistically significant yield differences. This does not establish that irrigation has no effect.")
    irrigation = data.groupby("Irrigation_Type")["Crop_Yield_ton_per_hectare"].agg(count="size", mean="mean", median="median").reset_index()
    try:
        import plotly.express as px
        st.plotly_chart(px.box(data, x="Irrigation_Type", y="Crop_Yield_ton_per_hectare", color="Irrigation_Type", points=False, title="Recorded yield distributions by irrigation category"), width="stretch")
    except ModuleNotFoundError:
        st.bar_chart(irrigation.set_index("Irrigation_Type")["mean"])
    with st.expander("Supporting statistical evidence"): st.dataframe(evidence("results/baseline_details/A010_A015_irrigation_anova.csv", show_warning=False), hide_index=True)
elif page == "Prediction Accuracy":
    st.title("Prediction accuracy")
    analysis_context(["A056","A057","A058","A059","A060","A061"])
    st.markdown("Several tested models predict accurately within this dataset. The best ranking changes with evaluation design, so no universally best model is claimed.")
    metrics = evidence("results/model_metrics.csv")
    primary = metrics[metrics.Analysis_ID.isin(["A057", "A058", "A059", "A061"]) & metrics.holdout_RMSE.notna()].drop_duplicates("model")
    try:
        import plotly.express as px
        if not primary.empty:
            fig = px.scatter(primary.sort_values("holdout_RMSE"), x="holdout_RMSE", y="model", text="holdout_RMSE", color="model", title="Primary holdout RMSE — lower is better")
            fig.update_traces(texttemplate="%{text:.2f}", textposition="middle right")
            fig.update_layout(xaxis_title="Holdout RMSE", yaxis_title="Model")
            st.plotly_chart(fig, width="stretch")
        global_row = metrics[(metrics.Analysis_ID == "A056") & metrics.holdout_RMSE.notna()]
        if not global_row.empty: st.metric("Global mean context", f"RMSE {global_row.iloc[0].holdout_RMSE:.2f}")
    except ModuleNotFoundError:
        if not primary.empty: st.bar_chart(primary.set_index("model")["holdout_RMSE"])
    with st.expander("Primary metrics"): st.dataframe(primary, hide_index=True)
    st.write("Primary fixed configuration: gradient boosting ranked first. Independent five-seed evaluation: linear regression ranked first on average.")
    with st.expander("Independent evaluation"): st.dataframe(evidence("audit/Phase8_Independent_Replication/PHASE8_RESULTS.csv"), hide_index=True)
    importance = metrics[(metrics.Analysis_ID == "A060") & metrics.importance_mean.notna()]
    if not importance.empty: st.subheader("Predictive feature contribution"); st.bar_chart(importance.set_index("feature")["importance_mean"])
    st.caption("Feature importance is predictive contribution, not causal influence.")
elif page == "Explore the Data":
    st.title("Explore the data")
    st.caption("Exploratory filtered data — not independently audited findings.")
    selected = data.copy()
    for col in ["Crop_Type", "Soil_Type", "Region", "Irrigation_Type"]:
        values = st.sidebar.multiselect(col.replace("_", " "), sorted(data[col].dropna().unique()))
        if values: selected = selected[selected[col].isin(values)]
    st.write(f"Rows shown: {len(selected):,} of {len(data):,}")
    if selected.empty: st.warning("No rows match the selected filters.")
    else:
        nums = numeric_columns(selected)
        summary = descriptive_summary(selected)
        c1,c2,c3,c4 = st.columns(4)
        x_options = [c for c in nums if c != "Crop_Yield_ton_per_hectare"]
        x = st.selectbox("Explanatory variable", x_options, index=x_options.index("Rainfall") if "Rainfall" in x_options else 0)
        r = safe_pearson(selected, x, "Crop_Yield_ton_per_hectare")
        c1.metric("Observations", f"{summary['n']:,}"); c2.metric("Mean yield", f"{summary['mean']:.2f}"); c3.metric("Median yield", f"{summary['median']:.2f}"); c4.metric("Selected association", "Not defined" if r is None else f"r = {r:.3f}")
        tab1, tab2, tab3, tab4 = st.tabs(["Relationship", "Distributions", "Correlation heatmap", "Compare / drill through"])
        try:
            import plotly.express as px
            with tab1:
                chart_type = st.radio("View", ["Scatter", "Trend-free distribution"], horizontal=True)
                if chart_type == "Scatter":
                    facet = st.checkbox("Small multiples by crop")
                    fig = px.scatter(selected, x=x, y="Crop_Yield_ton_per_hectare", color="Crop_Type", facet_col="Crop_Type" if facet else None, opacity=.55, hover_data=["Soil_Type", "Irrigation_Type", "Region"], title=f"Recorded {x.replace('_',' ')} and yield")
                else: fig = px.histogram(selected, x=x, color="Crop_Type", nbins=st.slider("Bins", 10, 80, 30), title=f"Distribution of recorded {x.replace('_',' ')}")
                st.plotly_chart(fig, width="stretch")
                st.caption("Exploratory association within the selected rows; it does not establish causation or statistical significance.")
            with tab2:
                yview = st.selectbox("Distribution chart", ["Yield boxplot", "Yield violin", "Yield histogram"])
                fig = px.box(selected, x="Crop_Type", y="Crop_Yield_ton_per_hectare", color="Crop_Type", points=False, title="Yield distribution by crop") if yview == "Yield boxplot" else px.violin(selected, x="Crop_Type", y="Crop_Yield_ton_per_hectare", color="Crop_Type", box=True, title="Yield distribution by crop") if yview == "Yield violin" else px.histogram(selected, x="Crop_Yield_ton_per_hectare", color="Crop_Type", nbins=35, title="Yield distribution")
                st.plotly_chart(fig, width="stretch")
            with tab3:
                corr_vars = st.multiselect("Numeric variables", nums, default=nums[:min(8,len(nums))])
                if len(corr_vars) >= 2:
                    matrix = selected[corr_vars].corr()
                    st.plotly_chart(px.imshow(matrix, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, title="Exploratory Pearson correlation matrix"), width="stretch")
            with tab4:
                crops = sorted(selected.Crop_Type.unique())
                if len(crops) < 2: st.info("Select at least two crops for drill-through comparison.")
                else:
                    first = st.selectbox("First crop", crops, index=0); second = st.selectbox("Compare with", crops, index=1 if len(crops)>1 else 0)
                    compare = selected[selected.Crop_Type.isin([first, second])]
                    st.plotly_chart(px.box(compare, x="Crop_Type", y="Crop_Yield_ton_per_hectare", color="Crop_Type", points=False, title=f"Drill-through: {first} versus {second}"), width="stretch")
                    st.dataframe(compare.groupby("Crop_Type")["Crop_Yield_ton_per_hectare"].agg(Observations="size", Mean="mean", Median="median", SD="std").reset_index(), hide_index=True)
        except ModuleNotFoundError: st.info("Install Plotly for interactive exploratory charts.")
        st.subheader("Descriptive outlier flags")
        st.caption("Flags use the descriptive 1.5×IQR rule; rows are not removed or changed.")
        st.write(f"Potential yield outliers: {int(outlier_flags(selected, 'Crop_Yield_ton_per_hectare').sum())}")
        st.download_button("Download filtered observations", selected.to_csv(index=False), "filtered_observations.csv", "text/csv")
elif page == "Traditional BI vs GenAI":
    st.title("Traditional BI vs GenAI")
    st.caption("A neutral comparison of the two implemented workflows. This is not a claim that one tool is universally superior.")
    st.markdown('<div class="hero"><h1>Executive comparison</h1><p>The GenAI-assisted workflow expanded the implemented analytical scope and made reproducibility, traceability and human review more explicit. The evidence does not demonstrate that GenAI alone reduced effort or universally improved accuracy.</p></div>', unsafe_allow_html=True)
    st.subheader("What the evidence shows")
    a,b,c = st.columns(3)
    a.markdown('<div class="insight"><h4>Demonstrated advantages</h4><p>Analytical depth, reproducible Python artifacts, evidence traceability and explicit governance gates.</p></div>', unsafe_allow_html=True)
    b.markdown('<div class="insight"><h4>Mixed results</h4><p>Reliability and stakeholder communication improved in documented design, but replication was partial and no user study measured superiority.</p></div>', unsafe_allow_html=True)
    c.markdown('<div class="insight"><h4>Insufficient evidence</h4><p>No defensible time-savings or productivity percentage can be calculated from the available records.</p></div>', unsafe_allow_html=True)
    dimensions = pd.DataFrame({"Dimension": ["Analytical depth", "Efficiency", "Accuracy and reliability", "Reproducibility", "Transparency and traceability", "Stakeholder communication", "Human oversight and governance"], "Assessment": ["GenAI workflow demonstrated an advantage", "Insufficient evidence", "Mixed or context-dependent", "GenAI workflow demonstrated an advantage", "GenAI workflow demonstrated an advantage", "Mixed or context-dependent", "GenAI workflow demonstrated an advantage"], "Plain-English interpretation": ["More relationship, interaction, nonlinear and predictive analyses were implemented.", "Comparable active-hours evidence was not recorded.", "Audits and replication improved checking, but A4/A5 and F005 remain unresolved.", "Checksums, scripts, locked dependencies, seeds and stored outputs are available.", "Claims can be followed through Finding IDs, Analysis IDs and evidence references.", "The dashboard adds exploration and traceability; measured user outcomes are unavailable.", "Independent audit, blind replication and human decisions were explicitly recorded."]})
    st.subheader("Seven evaluation dimensions")
    st.dataframe(dimensions, hide_index=True, width="stretch")
    try:
        import plotly.express as px
        plot = dimensions.copy(); plot["Score"] = plot.Assessment.map({"GenAI workflow demonstrated an advantage": 3, "Mixed or context-dependent": 2, "Insufficient evidence": 1})
        st.plotly_chart(px.bar(plot, x="Score", y="Dimension", orientation="h", color="Assessment", text="Assessment", title="Evidence category by evaluation dimension", range_x=[0,3.5]), width="stretch")
        st.caption("The scores are display categories only, not a composite performance score.")
    except ModuleNotFoundError:
        pass
    st.subheader("What can reasonably be associated with GenAI?")
    st.markdown("- **Explicitly evidenced AI involvement:** analytical planning, code generation and review, documentation, independent AI audit and report drafting.\n- **Observed during the GenAI-assisted workflow but not uniquely attributable to AI:** broader statistical scope, reproducible Python outputs, dashboard development and structured evidence traceability. Python, added project scope and human effort also contributed.\n- **Insufficient evidence:** time savings, productivity percentages and causal superiority over the traditional workflow.")
    st.subheader("Human oversight and limitations")
    st.warning("Human review remains final authority. F005 is deferred under D017. Dataset provenance and units remain UNKNOWN. Predictive performance is within this dataset and model rankings are configuration-sensitive.")
    st.download_button("Download comprehensive Phase 11 report", (ROOT / "results/PHASE11_COMPARATIVE_EVALUATION.md").read_bytes(), "PHASE11_COMPARATIVE_EVALUATION.md", "text/markdown")
    st.download_button("Download executive brief", "GenAI-assisted Python broadened the implemented analysis and strengthened traceability and governance documentation. Time savings and universal accuracy improvements were not demonstrated. Human oversight remained essential.", "PHASE11_EXECUTIVE_BRIEF.txt", "text/plain")
    st.download_button("Download comparative evidence matrix", (ROOT / "results/PHASE11_EVIDENCE_MATRIX.csv").read_bytes(), "PHASE11_EVIDENCE_MATRIX.csv", "text/csv")
    with st.expander("References"):
        st.markdown("Evidence inventory: `results/PHASE11_EVIDENCE_INVENTORY.csv`  \nComparative report: `results/PHASE11_COMPARATIVE_EVALUATION.md`  \nPhase 9 evidence index: `results/PHASE9_EVIDENCE_REFERENCE_INDEX.csv`")
elif page == "How We Analysed the Data":
    st.title("How We Analysed the Data")
    st.caption("The results come first. This section explains how they were checked and where uncertainty remains.")
    st.subheader("The project questions")
    st.markdown("1. Which crop-specific relationships are associated with yield?\n2. How accurately can yield be predicted?\n3. Which GenAI-assisted findings are reliable enough for human review?")
    st.subheader("Evidence journey")
    timeline = pd.DataFrame({"Stage": ["1. Validate", "2. Reproduce", "3. Analyse", "4. Audit", "5. Blind replication", "6. Human review"], "What happened": ["The source file, structure and quality were checked.", "Selected traditional BI calculations were reproduced in Python.", "Relationships, interactions and predictive models were calculated from stored data.", "An independent AI checked methods and numerical evidence.", "A separate AI calculated selected results without seeing the primary answers.", "A human reviewer accepted six findings with qualifications and deferred F005."]})
    st.table(timeline)
    with st.expander("How GenAI assisted"):
        st.write("GenAI helped plan analyses, write code, identify possible patterns, document limitations and prepare the dashboard. Python calculations and stored result files remain the numerical source of truth.")
    with st.expander("Verification and decisions"):
        st.write("Phase 7 audited existing calculations. Phase 8 performed blind replication. Phase 9 recorded the human decisions. F005 was deferred because the Cotton RESET/specification warning remains unresolved under D017.")
        st.metric("Qualified findings", len(eligible)); st.metric("Deferred findings", int((decisions.Human_Decision == "DEFER").sum())); st.metric("Evidence references", len(refs))
        st.dataframe(decisions[["Finding_ID", "Human_Decision", "Required_Display_Qualification", "Status"]], hide_index=True)
    with st.expander("Limitations"):
        st.markdown("**Provenance:** UNKNOWN. Relationships are observational, not causal. Non-significance does not establish equivalence. Predictive performance is within this dataset. Model rankings depend on evaluation design. Units and geographic meaning are not fully documented.")
    with st.expander("Evidence traceability"):
        st.dataframe(refs, hide_index=True)
        st.write("Dataset checksum:", manifest["source_dataset"]["sha256"])
    st.subheader("Finding Evidence Explorer")
    st.caption("Trace a candidate finding from its claim to the stored calculations, independent checks and human decision. Original technical status and human decision are separate fields.")
    selected_finding = st.selectbox("Select Finding_ID", decisions.Finding_ID.tolist(), key="finding_explorer")
    decision_matches = human_register[human_register.Finding_ID.eq(str(selected_finding).strip())]
    if decision_matches.empty:
        st.warning("Finding evidence is temporarily unavailable for this selection.")
        decision = None
    else:
        decision = decision_matches.iloc[0]
    finding = next((f for f in findings if f["finding_id"] == selected_finding), None)
    if finding and decision is not None:
        st.markdown(f"### {selected_finding}")
        st.write(finding["claim"])
        a,b,c = st.columns(3)
        a.markdown(f'<div class="trace-card"><div class="trace-label">Original technical status</div><div class="trace-value">{decision["Status"]}</div></div>', unsafe_allow_html=True)
        b.markdown(f'<div class="trace-card"><div class="trace-label">Human decision</div><div class="trace-value">{decision["Human_Decision"].replace("_", " ")}</div></div>', unsafe_allow_html=True)
        c.markdown(f'<div class="trace-card"><div class="trace-label">Analysis IDs</div><div class="trace-value">{decision["Analysis_IDs"]}</div></div>', unsafe_allow_html=True)
        st.info("UNVERIFIED is the preserved technical verification status. Human acceptance with qualifications is a separate decision and does not rewrite that status.")
        qualification = decision.get("Required_Display_Qualification", "Qualification not recorded in this register.")
        if pd.isna(qualification) or not str(qualification).strip():
            qualification = "Qualification not recorded in this register."
        st.markdown(f"**Qualification:** {qualification}")
        st.markdown(f"**Numerical evidence:** {finding['supporting_result']}")
        st.markdown(f"**Limitations:** {finding['limitations']}")
        finding_refs = refs[refs.Finding_ID.astype(str).str.contains(selected_finding)]
        for stage in ["PRIMARY", "PHASE7", "PHASE8_BLIND", "PHASE8_COMPARISON", "GOVERNANCE"]:
            group = finding_refs[finding_refs.Evidence_Stage.eq(stage)]
            if len(group):
                with st.expander(f"{stage.replace('_',' ').title()} evidence ({len(group)})", expanded=(stage == "PRIMARY")):
                    for _, ref in group.iterrows():
                        path = str(ref.Repository_Relative_Path)
                        exists = (ROOT / path).exists()
                        st.markdown(f"**{ref.Evidence_ID} · {ref.Analysis_ID}** — {ref.Evidence_Description}")
                        st.caption(f"Location: `{path}` · Record: {ref.Exact_Record_or_Location}")
                        if exists:
                            st.markdown(f"[Open repository file]({path})")
                        else:
                            st.warning("Evidence reference unavailable")
        if selected_finding == "F005":
            st.warning("F005 is DEFERRED. Cotton coefficient interpretation remains withheld under D017 and is not presented as an accepted conclusion.")
    with st.expander("Traditional BI versus GenAI"):
        st.write("The Python workflow documents reproducible calculations, broader diagnostic/predictive scope and evidence traceability. The comparison does not claim that Excel or Power BI lacks these capabilities, and time savings were not documented.")
elif page == "Analysis Process":
    st.title("Analysis Process")
    st.caption("A guided view of how the project progressed from traditional BI to governed GenAI-assisted analysis.")
    phases = [
        ("Phase 1", "Dataset validation", "Confirm source identity, dimensions and quality.", "Validated checksum and manifest.", "Assisted documentation; deterministic validation.", "Human approval of checksum and provenance limits.", "results/dataset_manifest.json"),
        ("Phase 1.5", "Reproducibility and metadata", "Define dependencies, data dictionary and provenance status.", "Locked environment; dictionary; provenance record.", "Documentation and dependency planning.", "Human approval of UNKNOWN metadata.", "docs/DATA_DICTIONARY.md"),
        ("Phase 2", "Baseline reproduction", "Reproduce selected traditional BI analyses.", "Analysis register and comparison outputs.", "Python implementation and discrepancy documentation.", "Human approval of reproduction decisions.", "results/analysis_register.csv"),
        ("Phase 2.5", "Method validation", "Review ANOVA, regression and multiple-testing choices.", "Baseline methodology review.", "Assumption and interpretation audit support.", "Human approval of methodological decisions.", "results/baseline_methodology_review.md"),
        ("Phase 3–4", "Relationships and interactions", "Analyse descriptive relationships and prespecified interactions.", "Deterministic relationship and interaction outputs.", "Analysis planning, code and interpretation drafts.", "Human approval of scope and limitations.", "results/interaction_results.csv"),
        ("Phase 5", "Predictive modelling", "Compare baselines, linear, Random Forest and boosting models.", "Model metrics and feature contribution outputs.", "Code generation and leakage/test review.", "Human approval of predictive framing.", "results/model_metrics.csv"),
        ("Phase 7", "Independent audit", "Challenge calculations, methods and claims.", "Audit report and remediation.", "Audit preparation and documentation.", "Human review of corrections.", "audit/Claude Audit result/INDEPENDENT_AUDIT_REPORT (2).md"),
        ("Phase 8", "Blind replication", "Independently reproduce selected results without primary answers.", "Frozen replication outputs and comparison.", "Replication package preparation.", "Human approval of comparison decisions.", "audit/Phase8_Independent_Replication/PHASE8_RESULTS.csv"),
        ("Phase 9", "Human verification", "Decide which findings may be reported.", "Six qualified acceptances; F005 deferred.", "Decision-log preparation.", "Human reviewer is final authority.", "results/PHASE9_HUMAN_DECISION_LOG.md"),
        ("Phase 10", "Dashboard communication", "Make results, evidence and limitations accessible.", "Approved Streamlit dashboard.", "Dashboard code, EDA and evidence explorer.", "Human visual acceptance.", "results/PHASE10_IMPLEMENTATION_REPORT.md"),
        ("Phase 11", "Workflow comparison", "Compare implemented traditional and GenAI-assisted workflows.", "Evidence inventory, matrix and comparative report.", "Structured comparison drafting.", "Review remains required before later phases.", "results/PHASE11_COMPARATIVE_EVALUATION.md"),
    ]
    st.subheader("Project timeline")
    for phase, title, objective, outputs, ai_role, human_role, path in phases:
        with st.expander(f"{phase} · {title}"):
            st.write("**Objective:**", objective)
            st.write("**Main outputs:**", outputs)
            st.write("**GenAI role:**", ai_role)
            st.write("**Human role:**", human_role)
            if (ROOT / path).exists():
                supporting_file = ROOT / path
                st.download_button(
                    f"Download {supporting_file.name}",
                    supporting_file.read_bytes(),
                    file_name=supporting_file.name,
                    mime="text/markdown" if supporting_file.suffix.lower() == ".md" else "text/plain",
                    key=f"phase_download_{path}",
                )
            else: st.warning("Supporting file unavailable")
    st.subheader("Curated document explorer")
    docs = [
        ("Project specification", "Governance", "docs/PROJECT_SPEC.md"), ("Methodology", "Governance", "docs/METHODOLOGY.md"), ("Business questions", "Governance", "docs/BUSINESS_QUESTIONS.md"), ("Analysis rules", "Governance", "docs/ANALYSIS_RULES.md"), ("Human verification", "Governance", "docs/HUMAN_VERIFICATION.md"), ("Decisions", "Governance", "docs/DECISIONS.md"),
        ("Data dictionary", "Governance", "docs/DATA_DICTIONARY.md"), ("Data provenance", "Governance", "docs/DATA_PROVENANCE.md"), ("Phase 7 remediation", "Independent audit", "results/phase7_remediation_report.md"),
        ("Phase 8 comparison", "Blind replication", "results/PHASE8_COMPARISON_REPORT.md"), ("Human decision log", "Human decisions", "results/PHASE9_HUMAN_DECISION_LOG.md"),
        ("Phase 10 report", "Dashboard", "results/PHASE10_IMPLEMENTATION_REPORT.md"), ("Phase 11 report", "Workflow comparison", "results/PHASE11_COMPARATIVE_EVALUATION.md"),
    ]
    search = st.text_input("Search documents")
    category = st.selectbox("Category", ["All"] + sorted({d[1] for d in docs}))
    for title, group, path in docs:
        if search.lower() not in (title + group + path).lower() or (category != "All" and category != group): continue
        with st.expander(f"{title} · {group}"):
            st.caption(path)
            if (ROOT / path).exists():
                file_path = ROOT / path
                # Keep the download control above long previews so it is immediately
                # usable for large governance documents.
                st.download_button(
                    f"Download {Path(path).name}",
                    file_path.read_bytes(),
                    file_name=Path(path).name,
                    mime="text/markdown" if file_path.suffix.lower() == ".md" else "text/plain",
                    key=f"dl_{path}",
                    help="Save this approved repository document to your computer.",
                )
                st.markdown(file_path.read_text(encoding="utf-8")[:5000])
            else: st.warning("Document unavailable")
    st.subheader("Educational prompt examples")
    st.caption("The supplied prompt collection is retrospective and illustrative. It is not an archive of the exact historical prompts used in the project.")
    reconstructed_dir = ROOT / "audit/prompts/reconstructed_examples"
    if reconstructed_dir.exists():
        st.caption("These examples are provided for educational purposes only and do not alter the project evidence record.")
        for example in sorted(reconstructed_dir.glob("Phase_*.md")):
            st.download_button(
                f"Download {example.name}",
                example.read_bytes(),
                file_name=example.name,
                mime="text/markdown",
                key=f"reconstructed_download_{example.name}",
            )
    journey_path = ROOT / "results/AI_DEVELOPMENT_JOURNEY.md"
    if journey_path.exists():
        with st.expander("AI Development Journey — problem → prompt purpose → output → verification → decision"):
            st.markdown(journey_path.read_text(encoding="utf-8"))
    st.subheader("AI and human responsibilities")
    st.markdown("**GenAI assistance:** planning, code generation, exploratory suggestions and interpretation drafts where documented.  \n**Deterministic software:** calculations, model fitting, stored numerical outputs and tests.  \n**Human oversight:** methodology approval, evidence eligibility, unresolved issues, finding decisions and final conclusions.")


