import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Wide Attacker Scouting",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── STYLING ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.main { background: #0D0F14; }
[data-testid="stSidebar"] { background: #111318; border-right: 1px solid #1E2028; }
[data-testid="stSidebar"] label { color: #8A8F9E !important; font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase; }

.metric-card {
    background: #161820; border: 1px solid #1E2028; border-radius: 10px;
    padding: 14px 18px; text-align: center;
}
.metric-card .val { font-family: 'DM Mono', monospace; font-size: 26px; font-weight: 500; color: #F0F2F5; }
.metric-card .lbl { font-size: 10px; color: #5A6072; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px; }

.tier-badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 600; font-family: 'DM Sans', sans-serif;
}
.hdr { font-family: 'DM Mono', monospace; font-size: 10px; color: #5A6072;
       letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 6px; }
.player-name { font-weight: 600; font-size: 14px; color: #F0F2F5; }
.sub-info { font-size: 11px; color: #5A6072; }

div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

.stSlider [data-baseweb="slider"] { margin-top: -8px; }
.section-title {
    font-family: 'DM Mono', monospace; font-size: 11px; color: #4A5568;
    letter-spacing: 0.12em; text-transform: uppercase;
    border-bottom: 1px solid #1E2028; padding-bottom: 8px; margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/scouting_app_data.csv")
    return df

@st.cache_data
def load_benchmarks():
    return {
        'psv_med': 29.45, 'psv_q75': 30.04,
        'hsr_bip': 789.6, 'spr_bip': 285.6, 'hi_bip': 1086.3, 'expl_bip': 1.32,
        'hsr_otip': 386.9, 'spr_otip': 118.5, 'hi_otip': 500.9, 'expl_otip': 0.45,
        't_hsr': 0.66, 't_sprint': 1.315,
    }

df_raw = load_data()
B = load_benchmarks()

TIER_COLORS = {
    '🔥 ELITE TARGET': '#FF6F00',
    '🟢 TOP TARGET':   '#1B5E20',
    '🔵 INTERESTING':  '#0D47A1',
    '🟡 WATCHLIST':    '#F57F17',
    '🔴 RISIKO':       '#B71C1C',
}
SPEED_COLORS = {
    '⚡ ELITE':  '#FF6F00', '🔵 HIGH': '#1565C0',
    '🟡 FAST':  '#0288D1', '🟠 MEDIUM': '#EF6C00', '—': '#2A2D38',
}

# ── IFI RECALCULATION (live) ──────────────────────────────────────────────────
def recalc_ifi(df, w_rq, w_dr, w_bt):
    total_w = w_rq + w_dr + w_bt
    if total_w == 0:
        df = df.copy()
        df['IFI Index']  = 0.0
        df['IFI Punkte'] = 0
    else:
        df = df.copy()
        df['IFI Index'] = (
            df['Run Quality'].fillna(0) * (w_rq / total_w) +
            df['Dribbling'].fillna(0)   * (w_dr / total_w) +
            df['Box Threat'].fillna(0)  * (w_bt / total_w)
        ).round(3)
        df['IFI Punkte'] = df['IFI Index'].apply(
            lambda ts: 5 if ts>=2.0 else (4 if ts>=1.5 else (3 if ts>=0.5 else
                       (2 if ts>=0.0 else (1 if ts>=-0.5 else 0))))
        )
    df['Final Total'] = df['Physical Score'] + df['IFI Punkte']
    df['Final Tier']  = df['Final Total'].apply(
        lambda t: '🔥 ELITE TARGET' if t>=20 else ('🟢 TOP TARGET' if t>=17 else
                  ('🔵 INTERESTING' if t>=14 else ('🟡 WATCHLIST' if t>=10 else '🔴 RISIKO')))
    )
    return df

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ Wide Attacker\n### Scouting Dashboard")
    st.markdown("---")

    st.markdown('<div class="section-title">Filter</div>', unsafe_allow_html=True)

    # Liga
    ligen = sorted(df_raw['Liga'].unique().tolist())
    sel_ligen = st.multiselect("Liga", ligen, default=ligen, label_visibility="visible")

    # PSV-99 Min
    psv_min = st.slider("PSV-99 Minimum (km/h)", 27.0, 32.5, 29.45, 0.1,
                        format="%.2f km/h")

    # Alter
    alter_range = st.slider("Alter", int(df_raw['Alter'].min()), int(df_raw['Alter'].max()),
                            (int(df_raw['Alter'].min()), int(df_raw['Alter'].max())))

    # Minuten
    min_range = st.slider("Minuten gespielt", int(df_raw['Minuten'].min()),
                          int(df_raw['Minuten'].max()), (200, int(df_raw['Minuten'].max())),
                          step=50)

    # Final Tier
    all_tiers = ['🔥 ELITE TARGET','🟢 TOP TARGET','🔵 INTERESTING','🟡 WATCHLIST','🔴 RISIKO']
    sel_tiers = st.multiselect("Final Tier", all_tiers, default=all_tiers)

    # OTIP Gate
    otip_gate = st.checkbox("Nur OTIP Pass ✅ YES", value=False)

    # Spielertyp
    all_typen = sorted(df_raw['Spielertyp'].unique().tolist())
    sel_typen = st.multiselect("Spielertyp", all_typen, default=all_typen)

    st.markdown("---")
    st.markdown('<div class="section-title">🎯 IFI Gewichtung</div>', unsafe_allow_html=True)
    st.caption("Gewichtung der Spielstil-Attribute (Summe = 100%)")

    w_rq = st.slider("Run Quality", 0, 100, 25, 5, format="%d%%")
    w_dr = st.slider("Dribbling",   0, 100, 50, 5, format="%d%%")
    w_bt = st.slider("Box Threat",  0, 100, 25, 5, format="%d%%")
    total_w = w_rq + w_dr + w_bt
    if total_w != 100:
        st.warning(f"Summe: {total_w}% (sollte 100% sein)")
    else:
        st.success("Summe: 100% ✓")

    st.markdown("---")
    st.markdown('<div class="section-title">Sortierung</div>', unsafe_allow_html=True)
    sort_col = st.selectbox("Sortieren nach", [
        "Final Total", "Physical Score", "PSV-99", "IFI Index",
        "OTIP Score", "BIP Score", "Burst Score", "Alter", "Minuten"
    ])

# ── FILTER & RECALC ───────────────────────────────────────────────────────────
df = recalc_ifi(df_raw, w_rq, w_dr, w_bt)

mask = (
    df['Liga'].isin(sel_ligen) &
    (df['PSV-99'] >= psv_min) &
    (df['Alter'] >= alter_range[0]) & (df['Alter'] <= alter_range[1]) &
    (df['Minuten'] >= min_range[0]) & (df['Minuten'] <= min_range[1]) &
    df['Final Tier'].isin(sel_tiers) &
    df['Spielertyp'].isin(sel_typen)
)
if otip_gate:
    mask = mask & (df['OTIP Pass'] == '✅ YES')

df_f = df[mask].sort_values(sort_col, ascending=False).reset_index(drop=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"## Wide Attacker Scouting")
st.markdown(f"<span style='color:#5A6072;font-size:13px'>7 Ligen · Osteuropa + 3.Liga Benchmark · {len(df_f)} Spieler nach Filter</span>",
            unsafe_allow_html=True)
st.markdown("---")

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
c1,c2,c3,c4,c5,c6 = st.columns(6)
for col, (val, lbl) in zip([c1,c2,c3,c4,c5,c6], [
    (len(df_f), "Spieler gesamt"),
    (len(df_f[df_f['Final Tier'].isin(['🔥 ELITE TARGET','🟢 TOP TARGET'])]), "Elite + Top"),
    (len(df_f[df_f['OTIP Pass']=='✅ YES']), "OTIP Pass ✅"),
    (f"{df_f['PSV-99'].max():.2f}", "Höchste PSV-99"),
    (f"{df_f['Final Total'].max():.1f}", "Bester Score"),
    (f"{df_f['Alter'].median():.0f}", "Median Alter"),
]):
    with col:
        st.markdown(f"""<div class="metric-card">
            <div class="val">{val}</div>
            <div class="lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 Spieler-Liste", "📊 Scatter-Plot", "📖 Scoring Info"])

# ────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown(f"<div class='hdr'>{len(df_f)} Spieler · sortiert nach {sort_col}</div>",
                unsafe_allow_html=True)

    if df_f.empty:
        st.info("Keine Spieler mit diesen Filtern.")
    else:
        # Display columns
        disp = df_f[[
            'Spieler','Verein','Liga','Alter','Minuten',
            'Final Total','Final Tier','Physical Score',
            'IFI Punkte','IFI Index',
            'Speed Flag','PSV-99','Δ PSV-99','Speed Score',
            'OTIP Pass','OTIP Score','Δ HSR OTIP',
            'BIP Level','BIP Score','Δ HSR BIP',
            'Burst Score','Δ T→HSR',
            'Spielertyp','Run Quality','Dribbling','Box Threat',
            'Transferwert (€)',
        ]].copy()

        # Color-code Final Tier column
        def tier_color(val):
            colors = {
                '🔥 ELITE TARGET': 'background-color:#7B3100;color:#FFE0B2',
                '🟢 TOP TARGET':   'background-color:#1B3A1E;color:#A5D6A7',
                '🔵 INTERESTING':  'background-color:#0D2A5E;color:#90CAF9',
                '🟡 WATCHLIST':    'background-color:#4A3A00;color:#FFE082',
                '🔴 RISIKO':       'background-color:#4A0D0D;color:#EF9A9A',
            }
            return colors.get(val, '')

        def psv_color(val):
            if pd.isna(val): return ''
            if val >= 32: return 'background-color:#7B3100;color:#FFE0B2'
            if val >= 31: return 'background-color:#0D2A5E;color:#90CAF9'
            if val >= 30.5: return 'background-color:#003344;color:#80DEEA'
            if val >= 29.45: return 'background-color:#3A2800;color:#FFCC80'
            return ''

        def delta_color(val):
            if pd.isna(val): return ''
            if val > 0: return 'color:#81C784'
            if val < 0: return 'color:#EF9A9A'
            return ''

        styled = (disp.style
            .applymap(tier_color, subset=['Final Tier'])
            .applymap(psv_color, subset=['PSV-99'])
            .applymap(delta_color, subset=['Δ PSV-99','Δ HSR OTIP','Δ HSR BIP'])
            .applymap(lambda v: 'color:#EF9A9A' if isinstance(v, float) and not pd.isna(v) and v > 0 else ('color:#81C784' if isinstance(v, float) and not pd.isna(v) and v < 0 else ''), subset=['Δ T→HSR'])
            .format({
                'PSV-99': '{:.2f}', 'Final Total': '{:.1f}', 'Physical Score': '{:.1f}',
                'IFI Index': '{:.3f}', 'Run Quality': '{:.3f}',
                'Dribbling': '{:.3f}', 'Box Threat': '{:.3f}',
                'Δ PSV-99': '{:+.2f}', 'Δ HSR OTIP': '{:+.0f}',
                'Δ HSR BIP': '{:+.0f}', 'Δ T→HSR': '{:+.3f}',
                'Transferwert (€)': lambda v: f"€{int(v):,}" if pd.notna(v) else '—',
            }, na_rep='—')
        )
        st.dataframe(styled, use_container_width=True, height=500)

        # Download
        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇️ Export CSV",
            csv,
            "scouting_export.csv",
            "text/csv",
            use_container_width=False,
        )

# ────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("<div class='hdr'>Scatter-Plot</div>", unsafe_allow_html=True)

    numeric_cols = [
        'PSV-99','Final Total','Physical Score','IFI Index',
        'OTIP Score','BIP Score','Burst Score','Speed Score',
        'Run Quality','Dribbling','Box Threat',
        'HSR OTIP P30','HSR P60BIP','Time→HSR (s)','Alter','Minuten',
        'Δ PSV-99','Δ HSR OTIP','Δ HSR BIP',
    ]

    col_x, col_y, col_size, col_color = st.columns(4)
    with col_x:
        x_axis = st.selectbox("X-Achse", numeric_cols, index=0)
    with col_y:
        y_axis = st.selectbox("Y-Achse", numeric_cols, index=2)
    with col_size:
        size_col = st.selectbox("Punktgröße", ['—'] + numeric_cols, index=0)
    with col_color:
        color_by = st.selectbox("Farbe nach", ['Final Tier','Speed Flag','Spielertyp','Liga'], index=0)

    if df_f.empty:
        st.info("Keine Daten für Plot.")
    else:
        try:
            import plotly.express as px
            import plotly.graph_objects as go

            plot_df = df_f.dropna(subset=[x_axis, y_axis]).copy()

            color_map = TIER_COLORS if color_by == 'Final Tier' else (
                SPEED_COLORS if color_by == 'Speed Flag' else None
            )

            size_vals = None
            if size_col != '—' and size_col in plot_df.columns:
                s = pd.to_numeric(plot_df[size_col], errors='coerce').fillna(0)
                s_min, s_max = s.min(), s.max()
                if s_max > s_min:
                    size_vals = ((s - s_min) / (s_max - s_min) * 20 + 6).tolist()
                else:
                    size_vals = [10] * len(plot_df)

            fig = px.scatter(
                plot_df,
                x=x_axis, y=y_axis,
                color=color_by,
                color_discrete_map=color_map,
                hover_name='Spieler',
                hover_data={
                    'Verein': True, 'Liga': True, 'Alter': True,
                    'Final Total': ':.1f', 'PSV-99': ':.2f',
                    'OTIP Pass': True, 'Speed Flag': True,
                    color_by: False,
                },
                size=size_vals if size_vals else None,
                size_max=24,
                template='plotly_dark',
                height=540,
            )

            # Benchmark lines
            if x_axis == 'PSV-99':
                fig.add_vline(x=B['psv_med'], line_dash="dash", line_color="#444",
                              annotation_text="3.Liga Median", annotation_font_size=10)
            if y_axis == 'PSV-99':
                fig.add_hline(y=B['psv_med'], line_dash="dash", line_color="#444")

            fig.update_layout(
                paper_bgcolor='#0D0F14', plot_bgcolor='#111318',
                font_family='DM Sans', font_color='#8A8F9E',
                xaxis=dict(gridcolor='#1E2028', zeroline=False),
                yaxis=dict(gridcolor='#1E2028', zeroline=False),
                legend=dict(bgcolor='#111318', bordercolor='#1E2028', borderwidth=1),
                margin=dict(l=40, r=20, t=40, b=40),
            )
            fig.update_traces(marker=dict(line=dict(width=0.5, color='#0D0F14')))

            st.plotly_chart(fig, use_container_width=True)

        except ImportError:
            st.warning("Plotly nicht installiert. `pip install plotly`")
            # Fallback: simple table
            st.dataframe(df_f[[x_axis, y_axis, 'Spieler', 'Liga', color_by]].head(30))

# ────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("### Final Total /25 — Formel")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
**Physical Score /20** (80%)
| Komponente | Faktor | Max |
|---|---|---|
| ⚡ Speed Score (0–4) | ×2.0 | 8 Pkte |
| 🏃 OTIP Score (0–4) | ×1.5 | 6 Pkte |
| 💥 BIP Score (0–4) | ×1.0 | 4 Pkte |
| 🚀 Burst Score (0–4) | ×0.5 | 2 Pkte |

**IFI Index Punkte /5** (20%)
- Run Quality × Gewicht + Dribbling × Gewicht + Box Threat × Gewicht
- Punkte: ≥2.0=5 / ≥1.5=4 / ≥0.5=3 / ≥0=2 / ≥−0.5=1 / <−0.5=0
        """)
    with col_b:
        st.markdown("""
**Final Tier — 5 Stufen**
| Score | Tier | Anzahl |
|---|---|---|
| ≥ 20 | 🔥 ELITE TARGET | ~2 |
| ≥ 17 | 🟢 TOP TARGET | ~12 |
| ≥ 14 | 🔵 INTERESTING | ~30 |
| ≥ 10 | 🟡 WATCHLIST | ~50 |
| < 10 | 🔴 RISIKO | Rest |

**Speed Flag**
- ⚡ ELITE ≥32.0 km/h
- 🔵 HIGH ≥31.0 km/h
- 🟡 FAST ≥30.5 km/h
- 🟠 MEDIUM ≥29.45 km/h (3.Liga Median)
- — unter Median
        """)

    st.markdown("---")
    st.markdown("### 3.Liga Benchmark (Wide Attacker, ≥500 min)")
    bench_df = pd.DataFrame([
        {"Metrik": "PSV-99 Median", "Wert": "29.45 km/h", "Layer": "Speed"},
        {"Metrik": "HSR Distance P60BIP", "Wert": "789.6m", "Layer": "BIP"},
        {"Metrik": "Sprint Distance P60BIP", "Wert": "285.6m", "Layer": "BIP"},
        {"Metrik": "HI Distance P60BIP", "Wert": "1086.3m", "Layer": "BIP"},
        {"Metrik": "Expl. Acc to Sprint P60BIP", "Wert": "1.32", "Layer": "BIP"},
        {"Metrik": "HSR Distance OTIP P30", "Wert": "386.9m", "Layer": "OTIP"},
        {"Metrik": "Sprint Distance OTIP P30", "Wert": "118.5m", "Layer": "OTIP"},
        {"Metrik": "HI Distance OTIP P30", "Wert": "500.9m", "Layer": "OTIP"},
        {"Metrik": "Expl. Acc to Sprint OTIP", "Wert": "0.45", "Layer": "OTIP"},
        {"Metrik": "Time to HSR", "Wert": "0.66s", "Layer": "Burst"},
        {"Metrik": "Time to Sprint", "Wert": "1.315s", "Layer": "Burst"},
    ])
    st.dataframe(bench_df, use_container_width=True, hide_index=True)
