"""Small chart builders kept separate from Streamlit rendering.

Plotly is optional at runtime: the dashboard falls back to native Streamlit
charts when the dependency has not yet been installed.
"""
try:
    import plotly.express as px
except ModuleNotFoundError:  # graceful startup before dependency installation
    px = None

def crop_yield_boxplot(data):
    if px is None:
        return None
    return px.box(data, x="Crop_Type", y="Crop_Yield_ton_per_hectare", color="Crop_Type", points=False, title="Yield distribution by crop")

def crop_mean_bar(summary):
    if px is None:
        return None
    return px.bar(summary, x="Crop_Type", y="mean", text="count", title="Mean yield by crop (labels show count)")

