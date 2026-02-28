import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Superstore Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# USD_TO_INR is now set by user in sidebar — see session_state["usd_rate"]

# ═══════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #080c18 !important;
    color: #e2e8f0 !important;
}
.stApp { background: #080c18 !important; }
.main .block-container { padding: 1.4rem 2rem 3rem !important; max-width: 1440px; }
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0d1117 0%,#080c18 100%) !important;
    border-right: 1px solid rgba(96,165,250,0.12) !important;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(145deg,#0f172a,#1e293b);
    border: 1px solid rgba(96,165,250,0.15);
    border-radius: 18px;
    padding: 1.25rem 1.4rem 1.1rem;
    position: relative;
    overflow: hidden;
    min-height: 120px;
    transition: transform .22s ease, box-shadow .22s ease;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(96,165,250,0.13);
}
.kpi-card::before {
    content:'';
    position:absolute; top:0; left:0; right:0;
    height:3px;
    background: var(--accent);
    border-radius: 18px 18px 0 0;
}
.kpi-label {
    font-size:0.62rem; font-weight:700;
    text-transform:uppercase; letter-spacing:2px;
    color:#475569; margin-bottom:0.4rem;
}
.kpi-value {
    font-size:1.35rem; font-weight:700;
    font-family:'DM Mono',monospace;
    line-height:1.15; margin-bottom:0.2rem;
    white-space:normal; word-break:break-word;
    color: var(--val-color);
}
.kpi-words {
    font-size:0.68rem; color:#475569;
    margin-bottom:0.25rem;
    font-style:italic;
}
.kpi-delta {
    font-size:0.7rem; font-weight:500; color:#64748b;
    display:flex; align-items:center; gap:4px;
}
.kpi-delta .up   { color:#34d399; }
.kpi-delta .down { color:#f87171; }
.kpi-delta .na   { color:#94a3b8; font-style:italic; }

/* accent variants */
.kpi-blue   { --accent:linear-gradient(90deg,#3b82f6,#60a5fa); --val-color:#60a5fa; }
.kpi-green  { --accent:linear-gradient(90deg,#10b981,#34d399); --val-color:#34d399; }
.kpi-purple { --accent:linear-gradient(90deg,#8b5cf6,#a78bfa); --val-color:#a78bfa; }
.kpi-orange { --accent:linear-gradient(90deg,#f59e0b,#fbbf24); --val-color:#fbbf24; }
.kpi-teal   { --accent:linear-gradient(90deg,#0d9488,#2dd4bf); --val-color:#2dd4bf; }
.kpi-sky    { --accent:linear-gradient(90deg,#0284c7,#38bdf8); --val-color:#38bdf8; }

/* ── Section headers ── */
.sec-hdr {
    display:flex; align-items:center; gap:10px;
    margin:1.6rem 0 0.9rem;
    padding-bottom:0.55rem;
    border-bottom:1px solid rgba(96,165,250,0.1);
}
.sec-hdr .ico {
    width:28px; height:28px;
    background:linear-gradient(135deg,#1e293b,#1e3a5f);
    border:1px solid rgba(96,165,250,0.22);
    border-radius:7px;
    display:flex; align-items:center; justify-content:center;
    font-size:0.9rem;
}
.sec-hdr .lbl { font-size:0.92rem; font-weight:600; color:#e2e8f0; }
.sec-hdr .bdg {
    margin-left:auto;
    background:rgba(96,165,250,0.08);
    border:1px solid rgba(96,165,250,0.22);
    color:#60a5fa; font-size:0.6rem; font-weight:700;
    text-transform:uppercase; letter-spacing:1px;
    padding:2px 9px; border-radius:20px;
}

/* ── No-data box ── */
.nodata {
    background:linear-gradient(135deg,#0f172a,#1e293b);
    border:1px dashed rgba(96,165,250,0.2);
    border-radius:14px;
    padding:2.2rem 2rem;
    text-align:center;
    margin:0.5rem 0 1rem;
}
.nodata .nd-icon  { font-size:2.2rem; margin-bottom:0.5rem; opacity:0.5; }
.nodata .nd-title { font-size:0.88rem; font-weight:600; color:#64748b; margin-bottom:0.25rem; }
.nodata .nd-sub   { font-size:0.76rem; color:#374151; }

/* ── Top banner ── */
.banner {
    background:linear-gradient(135deg,#0d1117 0%,#0f172a 60%,#0d1117 100%);
    border:1px solid rgba(96,165,250,0.13);
    border-radius:20px;
    padding:1.5rem 2rem;
    margin-bottom:1.2rem;
    display:flex; align-items:center; gap:1.4rem;
    position:relative; overflow:hidden;
}
.banner::after {
    content:'';
    position:absolute; top:-60%; right:-5%;
    width:280px; height:280px;
    background:radial-gradient(circle,rgba(96,165,250,0.07) 0%,transparent 70%);
    pointer-events:none;
}
.banner-logo {
    width:48px; height:48px;
    background:linear-gradient(135deg,#1e293b,#1e3a5f);
    border:1px solid rgba(96,165,250,0.28);
    border-radius:13px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.5rem; flex-shrink:0;
}
.banner-title { font-size:1.35rem; font-weight:700; color:#f1f5f9; letter-spacing:-.3px; }
.banner-sub   { font-size:0.75rem; color:#475569; margin-top:2px; }
.banner-pills { margin-left:auto; display:flex; gap:7px; }
.banner-pill  {
    background:rgba(96,165,250,0.07);
    border:1px solid rgba(96,165,250,0.18);
    color:#60a5fa; font-size:0.6rem; font-weight:700;
    text-transform:uppercase; letter-spacing:1px;
    padding:3px 9px; border-radius:20px;
}

/* ── Currency chip ── */
.curr-chip {
    display:inline-flex; align-items:center; gap:5px;
    padding:2px 10px; border-radius:20px;
    font-size:0.68rem; font-weight:700;
    letter-spacing:.8px; text-transform:uppercase;
    margin-left:8px;
}
.curr-usd { background:rgba(96,165,250,0.1); border:1px solid rgba(96,165,250,0.28); color:#60a5fa; }
.curr-inr { background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.28); color:#34d399; }

/* ── Upload guide ── */
.uzone {
    background:linear-gradient(135deg,#0f172a,#1e293b);
    border:2px dashed rgba(96,165,250,0.25);
    border-radius:20px;
    padding:3rem 2rem;
    text-align:center; margin:1.5rem 0;
}
.uzone .u-ico   { font-size:3.2rem; margin-bottom:0.8rem; opacity:.7; }
.uzone .u-title { font-size:1.2rem; font-weight:700; color:#e2e8f0; margin-bottom:.4rem; }
.uzone .u-sub   { font-size:0.8rem; color:#475569; }

/* ── Guide cards ── */
.gcard {
    background:linear-gradient(145deg,#0f172a,#1e293b);
    border:1px solid rgba(96,165,250,0.13);
    border-radius:16px;
    padding:1.6rem 1.2rem;
    text-align:center;
    transition: transform .2s;
}
.gcard:hover { transform:translateY(-3px); }
.gcard .g-ico   { font-size:1.8rem; margin-bottom:.7rem; }
.gcard .g-title { font-size:.9rem; font-weight:700; color:#e2e8f0; margin-bottom:.35rem; }
.gcard .g-desc  { font-size:.75rem; color:#64748b; line-height:1.5; }

/* ── Insight mini-card ── */
.icard {
    background:linear-gradient(135deg,#0f172a,#1e293b);
    border:1px solid rgba(96,165,250,0.12);
    border-radius:12px;
    padding:.9rem 1.1rem;
    margin-bottom:.55rem;
}
.icard .il { font-size:.62rem; color:#475569; text-transform:uppercase; letter-spacing:1px; font-weight:700; margin-bottom:.18rem; }
.icard .iv { font-size:1.05rem; font-weight:700; color:#e2e8f0; font-family:'DM Mono',monospace; }
.icard .is { font-size:.7rem; color:#94a3b8; margin-top:1px; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background:#0f172a; border-radius:12px;
    padding:4px; gap:3px;
    border:1px solid rgba(96,165,250,0.1);
}
.stTabs [data-baseweb="tab"] {
    background:transparent !important; color:#475569 !important;
    border-radius:8px !important; padding:7px 16px !important;
    font-weight:500 !important; font-size:0.8rem !important;
}
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#1e293b,#1e3a5f) !important;
    color:#60a5fa !important;
    box-shadow:0 2px 10px rgba(96,165,250,0.18) !important;
}
hr { border-color:rgba(96,165,250,0.08) !important; }
[data-testid="stFileUploader"] {
    background:#0f172a;
    border:1px dashed rgba(96,165,250,0.25);
    border-radius:12px; padding:.4rem;
}
.stDataFrame { border:1px solid rgba(96,165,250,0.1) !important; border-radius:12px !important; overflow:hidden; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  PLOTLY BASE — ⚠️ NO xaxis/yaxis HERE (that caused the crash)
#  xaxis/yaxis are applied via fig.update_xaxes() / fig.update_yaxes()
# ═══════════════════════════════════════════════════════════════
_BG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#0f172a",
    font=dict(family="DM Sans", color="#94a3b8", size=12),
    title_font=dict(color="#f1f5f9", size=13, family="DM Sans"),
    colorway=["#60a5fa","#34d399","#fbbf24","#f87171","#a78bfa","#2dd4bf","#fb923c","#818cf8"],
    margin=dict(l=16, r=16, t=46, b=16),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=10)),
    hoverlabel=dict(bgcolor="#1e293b", font_color="#f1f5f9", bordercolor="#3b82f6"),
)
_XA = dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.07)",
           tickfont=dict(color="#475569", size=10))
_YA = dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.07)",
           tickfont=dict(color="#475569", size=10))

def _apply(fig, title="", h=360):
    fig.update_layout(**_BG, title=title, height=h)
    fig.update_xaxes(**_XA)
    fig.update_yaxes(**_YA)
    return fig

# ═══════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def get_rate():
    return st.session_state.get("usd_rate", 83.5)

def fmt(val, inr=False):
    """Compact currency string — complete, never truncated."""
    if inr:
        v = val * get_rate()
        if v >= 1_00_00_000: return f"₹{v/1_00_00_000:.2f} Cr"
        if v >= 1_00_000:    return f"₹{v/1_00_000:.2f} L"
        return f"₹{v:,.0f}"
    if val >= 1_000_000: return f"${val/1_000_000:.2f}M"
    if val >= 1_000:     return f"${val/1_000:.1f}K"
    return f"${val:,.2f}"

def fmt_words(val, inr=False):
    """Full value in words — shown below the compact number."""
    if inr:
        v = val * get_rate()
        if v >= 1_00_00_000:
            cr  = int(v // 1_00_00_000)
            lkh = int((v % 1_00_00_000) // 1_00_000)
            return f"{cr} Crore {lkh} Lakh" if lkh else f"{cr} Crore"
        if v >= 1_00_000:
            lkh = int(v // 1_00_000)
            th  = int((v % 1_00_000) // 1_000)
            return f"{lkh} Lakh {th} Thousand" if th else f"{lkh} Lakh"
        return f"₹{v:,.0f}"
    # USD words
    if val >= 1_000_000:
        m = int(val // 1_000_000)
        k = int((val % 1_000_000) // 1_000)
        return f"{m} Million {k} Thousand" if k else f"{m} Million"
    if val >= 1_000:
        return f"{int(val):,}"
    return ""

def kpi(col, accent, label, value_str, delta, up=True, words=""):
    # kept for signature compat but not used — see KPI ROW below
    pass

def hdr(icon, title, badge=""):
    b = f'<span class="bdg">{badge}</span>' if badge else ""
    st.markdown(f"""
    <div class="sec-hdr">
        <div class="ico">{icon}</div>
        <span class="lbl">{title}</span>{b}
    </div>""", unsafe_allow_html=True)

def nodata(col_name, tip=""):
    msg = tip or f"Your dataset needs a <b>{col_name}</b> column to enable this chart."
    st.markdown(f"""
    <div class="nodata">
        <div class="nd-icon">🔍</div>
        <div class="nd-title">Column &nbsp;<code>{col_name}</code>&nbsp; not found in your data</div>
        <div class="nd-sub">{msg}</div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  SESSION STATE — currency toggle
# ═══════════════════════════════════════════════════════════════
if "inr" not in st.session_state:
    st.session_state.inr = False

# ═══════════════════════════════════════════════════════════════
#  BANNER
# ═══════════════════════════════════════════════════════════════
chip_cls = "curr-inr" if st.session_state.inr else "curr-usd"
chip_txt = "₹ INR"    if st.session_state.inr else "$ USD"
st.markdown(f"""
<div class="banner">
    <div class="banner-logo">📊</div>
    <div>
        <div class="banner-title">
            Superstore Analytics
            <span class="curr-chip {chip_cls}">{chip_txt}</span>
        </div>
        <div class="banner-sub">Business Intelligence · Sales Performance · Profitability</div>
    </div>
    <div class="banner-pills">
        <span class="banner-pill">Live</span>
        <span class="banner-pill">Multi-Year</span>
        <span class="banner-pill">Interactive</span>
    </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  FILE UPLOAD
# ═══════════════════════════════════════════════════════════════
uploaded = st.file_uploader("CSV", type=["csv"], label_visibility="collapsed")

if uploaded is None:
    st.markdown("""
    <div class="uzone">
        <div class="u-ico">📂</div>
        <div class="u-title">Drop your Superstore CSV here</div>
        <div class="u-sub">Supports: Order Date · Sales · Profit · Category · Region · State · Sub-Category</div>
    </div>""", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    for col,ico,t,d in [
        (c1,"📥","Step 1 — Upload","Select your Superstore Sales CSV file from your computer."),
        (c2,"⚙️","Step 2 — Filter","Use the sidebar to slice by region, category, date, or segment."),
        (c3,"📊","Step 3 — Analyse","Explore revenue trends, profitability, products & regional breakdown."),
    ]:
        col.markdown(f"""
        <div class="gcard">
            <div class="g-ico">{ico}</div>
            <div class="g-title">{t}</div>
            <div class="g-desc">{d}</div>
        </div>""", unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════════
#  LOAD DATA
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load(f):
    df = pd.read_csv(f)
    for c in ["Order Date","Ship Date"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], dayfirst=True, errors="coerce")
    return df

df = load(uploaded)

# validate required cols
for req in ["Sales","Region","Category"]:
    if req not in df.columns:
        st.error(f"❌ Required column missing: **{req}**. Please upload the correct Superstore file.")
        st.stop()

# ═══════════════════════════════════════════════════════════════
#  SIDEBAR  — Filters + Currency toggle
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<p style="font-size:.6rem;text-transform:uppercase;letter-spacing:2px;color:#334155;font-weight:700;margin-bottom:.8rem;">CONTROLS</p>', unsafe_allow_html=True)

    st.markdown("**💱 Currency**")
    new_inr = st.toggle("Show values in ₹ Rupees", value=st.session_state.inr)
    st.session_state.inr = new_inr
    if new_inr:
        user_rate = st.number_input(
            "1 USD = ₹ (set your rate)",
            min_value=50.0, max_value=150.0,
            value=st.session_state.get("usd_rate", 83.5),
            step=0.5, format="%.1f"
        )
        st.session_state.usd_rate = user_rate
        st.caption(f"Using: 1 USD = ₹{user_rate:.1f}")

    st.markdown("---")
    st.markdown("**🔎 Filters**")

    date_range = None
    if "Order Date" in df.columns:
        dmin, dmax = df["Order Date"].min().date(), df["Order Date"].max().date()
        date_range = st.date_input("📅 Date range", [dmin, dmax], min_value=dmin, max_value=dmax)

    regs  = sorted(df["Region"].dropna().unique())
    cats  = sorted(df["Category"].dropna().unique())
    s_reg = st.multiselect("🌍 Region",   regs, default=regs)
    s_cat = st.multiselect("🏷️ Category", cats, default=cats)

    s_seg  = None
    s_ship = None
    if "Segment" in df.columns:
        segs  = sorted(df["Segment"].dropna().unique())
        s_seg = st.multiselect("👥 Segment", segs, default=segs)
    if "Ship Mode" in df.columns:
        ships  = sorted(df["Ship Mode"].dropna().unique())
        s_ship = st.multiselect("🚚 Ship Mode", ships, default=ships)

    st.markdown("---")
    st.caption("Superstore Analytics v2.2")

# ═══════════════════════════════════════════════════════════════
#  APPLY FILTERS
# ═══════════════════════════════════════════════════════════════
fdf = df.copy()
if date_range and len(date_range) == 2 and "Order Date" in df.columns:
    fdf = fdf[(fdf["Order Date"].dt.date >= date_range[0]) &
              (fdf["Order Date"].dt.date <= date_range[1])]
if s_reg:  fdf = fdf[fdf["Region"].isin(s_reg)]
if s_cat:  fdf = fdf[fdf["Category"].isin(s_cat)]
if s_seg  and "Segment"  in df.columns: fdf = fdf[fdf["Segment"].isin(s_seg)]
if s_ship and "Ship Mode" in df.columns: fdf = fdf[fdf["Ship Mode"].isin(s_ship)]

if fdf.empty:
    st.warning("⚠️ No data matches your filters — please widen your selection.")
    st.stop()

# ─── Shorthand flags ──────────────────────────────────────────
INR        = st.session_state.inr
HAS_PROFIT = "Profit"       in fdf.columns
HAS_QTY    = "Quantity"     in fdf.columns
HAS_DISC   = "Discount"     in fdf.columns
HAS_DATE   = "Order Date"   in fdf.columns
HAS_STATE  = "State"        in fdf.columns
HAS_SUBCAT = "Sub-Category" in fdf.columns
HAS_PROD   = "Product Name" in fdf.columns
HAS_SEG    = "Segment"      in fdf.columns
HAS_SHIP   = "Ship Mode"    in fdf.columns
HAS_CUST   = "Customer ID"  in fdf.columns

total_sales   = fdf["Sales"].sum()
total_orders  = fdf.shape[0]
avg_order     = fdf["Sales"].mean()
total_profit  = fdf["Profit"].sum() if HAS_PROFIT else 0
margin_pct    = (total_profit / total_sales * 100) if HAS_PROFIT and total_sales else 0
total_qty     = fdf["Quantity"].sum() if HAS_QTY else None
unique_cust   = fdf["Customer ID"].nunique() if HAS_CUST else total_orders

# ═══════════════════════════════════════════════════════════════
#  KPI ROW  — all values on one clean line
# ═══════════════════════════════════════════════════════════════
hdr("📌", "Key Performance Indicators", f"{total_orders:,} orders")

# Build each card's HTML as plain string — no nesting issues
def _card(accent, label, val, words, delta, up=True):
    arr   = "▲" if up else "—"
    arr_c = "#34d399" if up else "#94a3b8"
    w_row = f'<div style="font-size:.68rem;color:#475569;font-style:italic;margin-bottom:.2rem;">{words}</div>' if words else ""
    return f"""
<div class="kpi-card {accent}" style="flex:1;min-width:0;">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{val}</div>
  {w_row}
  <div class="kpi-delta"><span style="color:{arr_c}">{arr}</span>&nbsp;{delta}</div>
</div>"""

c1 = _card("kpi-blue",   "Total Revenue",
           fmt(total_sales, INR), fmt_words(total_sales, INR),
           f"{total_orders:,} transactions")

c2 = _card("kpi-green",  "Gross Profit",
           fmt(total_profit, INR) if HAS_PROFIT else "N/A",
           fmt_words(total_profit, INR) if HAS_PROFIT else "",
           f"{margin_pct:.1f}% margin" if HAS_PROFIT else "Profit column not in data",
           up=HAS_PROFIT and margin_pct > 0)

c3 = _card("kpi-purple", "Profit Margin",
           f"{margin_pct:.1f}%" if HAS_PROFIT else "N/A", "",
           "of total revenue" if HAS_PROFIT else "Add Profit column to enable",
           up=HAS_PROFIT and margin_pct > 0)

c4 = _card("kpi-orange", "Units Sold",
           f"{int(total_qty):,}" if HAS_QTY else "N/A", "",
           "items shipped" if HAS_QTY else "Quantity column not in data",
           up=bool(HAS_QTY))

c5 = _card("kpi-teal",   "Avg Order Value",
           fmt(avg_order, INR), fmt_words(avg_order, INR),
           "per transaction")

c6 = _card("kpi-sky",    "Customers",
           f"{unique_cust:,}", "",
           "unique buyers" if HAS_CUST else "rows (no Customer ID col)")

st.markdown(
    f'<div style="display:flex;gap:12px;margin-bottom:1rem;">{c1}{c2}{c3}{c4}{c5}{c6}</div>',
    unsafe_allow_html=True
)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

#  TABS

tab1,tab2,tab3,tab4,tab5 = st.tabs([
    " Sales Trends"," Regional"," Products"," Profitability"," Data Explorer"
])

─
# TAB 1 — SALES TRENDS─
with tab1:
    if not HAS_DATE:
        nodata("Order Date",
               "Add an <b>Order Date</b> column (DD/MM/YYYY or MM/DD/YYYY) "
               "to unlock time-series charts, YoY comparison, and trend analysis.")
    else:
        _f = fdf.copy()
        _f["YM"] = _f["Order Date"].dt.to_period("M").dt.to_timestamp()

        hdr("📈", "Monthly Revenue & Order Volume")
        mon = _f.groupby("YM").agg(Sales=("Sales","sum"), Orders=("Sales","count")).reset_index()
        mon["MA3"] = mon["Sales"].rolling(3, min_periods=1).mean()

        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=mon["YM"], y=mon["Sales"], name="Revenue",
            marker_color="rgba(96,165,250,0.3)",
            marker_line_color="rgba(96,165,250,0.5)", marker_line_width=1,
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=mon["YM"], y=mon["MA3"], name="3-mo MA",
            line=dict(color="#60a5fa", width=2.5, dash="dot"),
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=mon["YM"], y=mon["Orders"], name="Orders",
            line=dict(color="#fbbf24", width=2),
            mode="lines+markers", marker=dict(size=4),
        ), secondary_y=True)
        fig.update_layout(**_BG, height=370,
                          title="Monthly Revenue (bars) + Order Count (right axis)")
        fig.update_xaxes(**_XA)
        fig.update_yaxes(title_text="Revenue", gridcolor="rgba(255,255,255,0.04)",
                         tickfont=dict(color="#475569",size=10), secondary_y=False)
        fig.update_yaxes(title_text="Orders", gridcolor="rgba(0,0,0,0)",
                         tickfont=dict(color="#fbbf24",size=10), secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

        c1,c2 = st.columns(2)
        with c1:
            hdr("📅","Year-over-Year Comparison")
            _f["Year"]  = _f["Order Date"].dt.year
            _f["Month"] = _f["Order Date"].dt.month
            yoy = _f.groupby(["Year","Month"])["Sales"].sum().reset_index()
            fig = px.line(yoy, x="Month", y="Sales", color="Year",
                          color_discrete_sequence=["#60a5fa","#34d399","#fbbf24","#a78bfa"],
                          markers=True)
            fig.update_layout(**_BG, height=310, title="Sales by Month (each year)")
            fig.update_xaxes(**_XA, tickmode="array", tickvals=list(range(1,13)),
                             ticktext=["Jan","Feb","Mar","Apr","May","Jun",
                                       "Jul","Aug","Sep","Oct","Nov","Dec"])
            fig.update_yaxes(**_YA)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            hdr("🏷️","Category Revenue Over Time")
            cm = _f.groupby(["YM","Category"])["Sales"].sum().reset_index()
            fig = px.area(cm, x="YM", y="Sales", color="Category",
                          color_discrete_sequence=["#60a5fa","#fbbf24","#34d399"])
            fig.update_traces(opacity=0.72)
            fig.update_layout(**_BG, height=310, title="Category Trend")
            fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
            st.plotly_chart(fig, use_container_width=True)

        hdr("📆","Revenue by Day of Week")
        c1,c2 = st.columns(2)
        with c1:
            _f["DayOfWeek"] = _f["Order Date"].dt.day_name()
            day_ord = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            dow = _f.groupby("DayOfWeek")["Sales"].sum().reindex(day_ord).reset_index()
            fig = px.bar(dow, x="DayOfWeek", y="Sales",
                         color="Sales", color_continuous_scale=["#1e293b","#60a5fa"])
            fig.update_layout(**_BG, height=290, title="Revenue by Order Day",
                              showlegend=False, coloraxis_showscale=False)
            fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            if HAS_SHIP:
                ss = _f.groupby("Ship Mode")["Sales"].sum().reset_index().sort_values("Sales")
                fig = px.bar(ss, x="Sales", y="Ship Mode", orientation="h",
                             color="Sales", color_continuous_scale=["#1e293b","#34d399"])
                fig.update_layout(**_BG, height=290, title="Revenue by Ship Mode",
                                  showlegend=False, coloraxis_showscale=False)
                fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
                st.plotly_chart(fig, use_container_width=True)
            else:
                nodata("Ship Mode")

# TAB 2 — REGIONAL
with tab2:
    hdr("🗺️","Regional Performance")
    c1,c2 = st.columns(2)

    reg = fdf.groupby("Region").agg(Sales=("Sales","sum"), Orders=("Sales","count")).reset_index()
    reg["Share"] = (reg["Sales"]/reg["Sales"].sum()*100).round(1)

    with c1:
        fig = go.Figure(go.Bar(
            x=reg["Region"], y=reg["Sales"],
            marker=dict(color=reg["Sales"],
                        colorscale=[[0,"#1e293b"],[.5,"#2563eb"],[1,"#60a5fa"]],
                        line=dict(color="rgba(96,165,250,0.2)",width=1)),
            text=[fmt(v,INR) for v in reg["Sales"]],
            textposition="outside",
            textfont=dict(color="#e2e8f0", size=12),
            cliponaxis=False,
        ))
        fig.update_layout(**_BG, title="Revenue by Region", height=360,
                          yaxis=dict(range=[0, reg["Sales"].max() * 1.25],
                                     gridcolor="rgba(255,255,255,0.04)",
                                     tickfont=dict(color="#475569", size=10)))
        fig.update_xaxes(**_XA)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        total_s = reg["Sales"].sum()
        fig = px.pie(reg, names="Region", values="Sales", hole=.6,
                     color_discrete_sequence=["#60a5fa","#34d399","#fbbf24","#a78bfa"])
        fig.update_traces(textposition="outside", textinfo="percent+label",
                          marker=dict(line=dict(color="#080c18",width=2)))
        fig.update_layout(**_BG, height=330, title="Revenue Share",
                          annotations=[dict(text=fmt(total_s,INR),x=.5,y=.5,
                                           font_size=17,font_color="#f1f5f9",showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    hdr("📍","Top & Bottom States by Revenue")
    if HAS_STATE:
        sd = fdf.groupby("State")["Sales"].sum().reset_index().sort_values("Sales",ascending=False)
        c1,c2 = st.columns(2)
        with c1:
            t10 = sd.head(10).sort_values("Sales")
            fig = px.bar(t10, x="Sales", y="State", orientation="h",
                         color="Sales", color_continuous_scale=["#1e3a5f","#60a5fa"],
                         text=[fmt(v,INR) for v in t10["Sales"]])
            fig.update_traces(textposition="outside")
            fig.update_layout(**_BG, height=350, title="🏆 Top 10 States",
                              showlegend=False, coloraxis_showscale=False)
            fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            b10 = sd.tail(10).sort_values("Sales",ascending=False)
            fig = px.bar(b10, x="Sales", y="State", orientation="h",
                         color="Sales", color_continuous_scale=["#f87171","#1e293b"],
                         text=[fmt(v,INR) for v in b10["Sales"]])
            fig.update_traces(textposition="outside")
            fig.update_layout(**_BG, height=350, title="📉 Bottom 10 States",
                              showlegend=False, coloraxis_showscale=False)
            fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
            st.plotly_chart(fig, use_container_width=True)
    else:
        nodata("State","Add a <b>State</b> column to see state-level performance maps.")

    hdr("🔥","Region × Category Revenue Matrix")
    piv = fdf.pivot_table(values="Sales",index="Region",columns="Category",aggfunc="sum").fillna(0)
    fig = px.imshow(piv, color_continuous_scale=["#080c18","#1e3a5f","#60a5fa"],
                    text_auto=".2s", aspect="auto")
    fig.update_layout(**_BG, height=270, title="Sales Heatmap: Region vs Category")
    st.plotly_chart(fig, use_container_width=True)

# TAB 3 — PRODUCTS
with tab3:
    hdr("🏷️","Product Performance")
    c1,c2 = st.columns(2)

    with c1:
        cd = fdf.groupby("Category")["Sales"].sum().reset_index()
        fig = px.bar(cd, x="Category", y="Sales", color="Category",
                     color_discrete_sequence=["#60a5fa","#fbbf24","#34d399"],
                     text=[fmt(v,INR) for v in cd["Sales"]])
        fig.update_traces(textposition="outside")
        fig.update_layout(**_BG, height=310, title="Revenue by Category", showlegend=False)
        fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        if HAS_SUBCAT:
            sub = fdf.groupby("Sub-Category")["Sales"].sum().sort_values().reset_index()
            fig = px.bar(sub, x="Sales", y="Sub-Category", orientation="h",
                         color="Sales", color_continuous_scale=["#1e293b","#60a5fa"])
            fig.update_layout(**_BG, height=310, title="Revenue by Sub-Category",
                              showlegend=False, coloraxis_showscale=False)
            fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
            st.plotly_chart(fig, use_container_width=True)
        else:
            nodata("Sub-Category")

    hdr("🎯","Sub-Category: Sales vs Profit Bubble")
    if HAS_SUBCAT and HAS_PROFIT:
        bub = fdf.groupby("Sub-Category").agg(
            Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Sales","count")
        ).reset_index()
        bub["Margin"] = (bub["Profit"]/bub["Sales"]*100).round(1)
        fig = px.scatter(bub, x="Sales", y="Profit", size="Orders",
                         text="Sub-Category", color="Margin",
                         color_continuous_scale=["#f87171","#fbbf24","#34d399"], size_max=55)
        fig.update_traces(textposition="top center", textfont=dict(size=9,color="#94a3b8"))
        fig.add_hline(y=0, line_color="rgba(255,255,255,0.15)", line_dash="dash")
        fig.add_vline(x=bub["Sales"].mean(), line_color="rgba(255,255,255,0.08)", line_dash="dot")
        fig.update_layout(**_BG, height=410,
                          title="Sub-Category: Sales vs Profit  (bubble size = orders)")
        fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
        st.plotly_chart(fig, use_container_width=True)
    elif not HAS_SUBCAT:
        nodata("Sub-Category")
    else:
        nodata("Profit","Add a <b>Profit</b> column to see the profitability bubble chart.")

    if HAS_PROD:
        hdr("🥇","Top 10 Products by Revenue")
        tp = fdf.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()
        tp["Short"] = tp["Product Name"].str[:44]
        tps = tp.sort_values("Sales")
        fig = px.bar(tps, x="Sales", y="Short", orientation="h",
                     color="Sales", color_continuous_scale=["#1e3a5f","#60a5fa"],
                     text=[fmt(v,INR) for v in tps["Sales"]])
        fig.update_traces(textposition="outside")
        fig.update_layout(**_BG, height=370, title="Top 10 Products",
                          showlegend=False, coloraxis_showscale=False, yaxis_title="")
        fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
        st.plotly_chart(fig, use_container_width=True)
    else:
        nodata("Product Name","Add a <b>Product Name</b> column to see the top-10 product leaderboard.")

# TAB 4 — PROFITABILITY
with tab4:
    if not HAS_PROFIT:
        nodata("Profit",
               "Your dataset doesn't have a <b>Profit</b> column. "
               "Add it to unlock: profit margin trends, discount impact analysis, "
               "monthly P&L, loss-making sub-categories and more.")
    else:
        hdr("Profitability Overview")
        c1,c2,c3 = st.columns(3)

        with c1:
            cp = fdf.groupby("Category")["Profit"].sum().reset_index()
            clr = ["#34d399" if v>0 else "#f87171" for v in cp["Profit"]]
            fig = go.Figure(go.Bar(
                x=cp["Category"], y=cp["Profit"], marker_color=clr,
                text=[fmt(v,INR) for v in cp["Profit"]], textposition="outside",
            ))
            _apply(fig,"Profit by Category",295)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            rpm = fdf.groupby("Region").agg(Sales=("Sales","sum"),Profit=("Profit","sum")).reset_index()
            rpm["Margin"] = (rpm["Profit"]/rpm["Sales"]*100).round(2)
            clr = ["#34d399" if v>10 else "#fbbf24" if v>0 else "#f87171" for v in rpm["Margin"]]
            fig = go.Figure(go.Bar(
                x=rpm["Region"], y=rpm["Margin"], marker_color=clr,
                text=[f"{v:.1f}%" for v in rpm["Margin"]], textposition="outside",
            ))
            _apply(fig,"Margin % by Region",295)
            fig.add_hline(y=0, line_color="rgba(255,255,255,0.2)", line_dash="dash")
            st.plotly_chart(fig, use_container_width=True)

        with c3:
            fig = px.histogram(fdf, x="Profit", nbins=50,
                               color_discrete_sequence=["#60a5fa"])
            fig.update_traces(opacity=.78, marker_line_width=0)
            fig.add_vline(x=0, line_color="#f87171", line_dash="dash", line_width=2)
            fig.add_vline(x=fdf["Profit"].mean(), line_color="#34d399",
                          line_dash="dot", line_width=2)
            fig.update_layout(**_BG, height=295, title="Profit Distribution", bargap=.04)
            fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
            st.plotly_chart(fig, use_container_width=True)

        if HAS_DATE:
            hdr("📈","Monthly Profit Trend")
            _f2 = fdf.copy()
            _f2["YM2"] = _f2["Order Date"].dt.to_period("M").dt.to_timestamp()
            mp = _f2.groupby("YM2").agg(Profit=("Profit","sum"),Sales=("Sales","sum")).reset_index()
            mp["Margin"] = (mp["Profit"]/mp["Sales"]*100).round(2)

            fig = make_subplots(specs=[[{"secondary_y":True}]])
            fig.add_trace(go.Bar(
                x=mp["YM2"], y=mp["Profit"], name="Profit",
                marker_color=[("#34d399" if v>0 else "#f87171") for v in mp["Profit"]],
                opacity=.82,
            ), secondary_y=False)
            fig.add_trace(go.Scatter(
                x=mp["YM2"], y=mp["Margin"], name="Margin %",
                line=dict(color="#fbbf24",width=2),
                mode="lines+markers", marker=dict(size=4),
            ), secondary_y=True)
            fig.update_layout(**_BG, height=355, title="Monthly Profit & Margin %")
            fig.update_xaxes(**_XA)
            fig.update_yaxes(title_text="Profit", gridcolor="rgba(255,255,255,0.04)",
                             tickfont=dict(color="#475569",size=10), secondary_y=False)
            fig.update_yaxes(title_text="Margin %", gridcolor="rgba(0,0,0,0)",
                             tickfont=dict(color="#fbbf24",size=10), secondary_y=True)
            fig.add_hline(y=0, line_color="rgba(255,255,255,0.15)", line_dash="dash",
                          secondary_y=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            nodata("Order Date","Add an <b>Order Date</b> column to see monthly P&L trends.")

        if HAS_DISC:
            hdr("🎟️","Discount Impact on Profit")
            c1,c2 = st.columns(2)
            with c1:
                samp = fdf.sample(min(3000,len(fdf)),random_state=42)
                fig = px.scatter(samp, x="Discount", y="Profit", color="Category",
                                 color_discrete_sequence=["#60a5fa","#fbbf24","#34d399"],
                                 opacity=.5)
                fig.add_hline(y=0, line_color="#f87171", line_dash="dash")
                fig.update_layout(**_BG, height=310, title="Discount vs Profit (sample)")
                fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                bins = pd.cut(fdf["Discount"],
                              bins=[0,.1,.2,.3,.5,1.0],
                              labels=["0-10%","10-20%","20-30%","30-50%","50%+"],
                              include_lowest=True)
                dp = fdf.groupby(bins,observed=True)["Profit"].mean().reset_index()
                dp.columns=["Disc Range","Avg Profit"]
                fig = px.bar(dp, x="Disc Range", y="Avg Profit", color="Avg Profit",
                             color_continuous_scale=["#f87171","#fbbf24","#34d399"])
                fig.add_hline(y=0, line_color="rgba(255,255,255,0.2)", line_dash="dash")
                fig.update_layout(**_BG, height=310, title="Avg Profit by Discount Band",
                                  showlegend=False, coloraxis_showscale=False)
                fig.update_xaxes(**_XA); fig.update_yaxes(**_YA)
                st.plotly_chart(fig, use_container_width=True)
        else:
            nodata("Discount","Add a <b>Discount</b> column to see how discount bands affect profitability.")


#DATA EXPLORER

with tab5:
    hdr("📋","Raw Data Explorer", f"{len(fdf):,} rows")

    c1,c2,c3,c4 = st.columns(4)
    for col, lbl, val, sub in [
        (c1,"Total Rows",   f"{len(fdf):,}",                          "after filters"),
        (c2,"Columns",      f"{fdf.shape[1]}",                        "in dataset"),
        (c3,"Memory",       f"{fdf.memory_usage(deep=True).sum()/1024:.0f} KB", "loaded"),
        (c4,"Null Values",  f"{fdf.isnull().sum().sum():,}",           "across all columns"),
    ]:
        col.markdown(f"""
        <div class="icard">
            <div class="il">{lbl}</div>
            <div class="iv">{val}</div>
            <div class="is">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

    show = st.multiselect("Select columns to display",
                          fdf.columns.tolist(), default=fdf.columns.tolist()[:8])
    if show:
        st.dataframe(fdf[show].reset_index(drop=True), use_container_width=True, height=400)

    hdr("⬇️","Export Filtered Data")
    st.download_button(
        label=f"⬇️  Download filtered CSV  ({len(fdf):,} rows)",
        data=fdf.to_csv(index=False).encode("utf-8"),
        file_name="superstore_filtered.csv",
        mime="text/csv",
    )

    hdr("📐","Statistical Summary")
    num_cols = fdf.select_dtypes(include=np.number).columns.tolist()
    if num_cols:
        st.dataframe(fdf[num_cols].describe().round(2), use_container_width=True)
    else:
        nodata("numeric columns","No numeric columns detected for summary statistics.")