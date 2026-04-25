import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Jahn Regensburg · Scouting",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

LOGO_B64 = "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"

R   = "#CC0000"
R2  = "#990000"
R3  = "#3D0000"
W   = "#FFFFFF"
W2  = "#F0F0F0"
BG  = "#0D0D0D"
C1  = "#181818"
C2  = "#2A2A2A"
SB  = "#181818"
MUT = "#999999"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{{font-family:'DM Sans',sans-serif;background:{BG};color:{W2};}}
.main{{background:{BG};}}
.block-container{{padding-top:2rem !important;padding-bottom:1rem;}}

/* Top red bar */
[data-testid="stHeader"]{{background:transparent;}}
[data-testid="stHeader"]::after{{
    content:'';display:block;height:4px;
    background:linear-gradient(90deg,{R2},{R} 30%,#FF3333 50%,{R} 70%,{R2});
    position:fixed;top:0;left:0;right:0;z-index:9999;
}}

/* Sidebar — aufgehellt */
[data-testid="stSidebar"]{{
    background:{SB};
    border-right:2px solid {R};
}}
[data-testid="stSidebar"] label{{
    color:{W2} !important;
    font-size:11px !important;
    letter-spacing:0.08em;
    text-transform:uppercase;
    font-weight:500 !important;
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span{{
    color:{W2} !important;
}}
[data-testid="stSidebar"] .stSlider [data-testid="stMarkdownContainer"] p{{
    color:{W2} !important;
    font-weight:600 !important;
}}

/* Slider rot */
[data-testid="stSlider"] [role="progressbar"]{{background:{R} !important;}}

/* Buttons rot/weiß */
.stButton>button,.stDownloadButton>button{{
    background:{R} !important;color:{W} !important;
    border:none !important;border-radius:6px !important;
    font-weight:700 !important;letter-spacing:0.05em !important;
}}

/* Tabs */
[role="tab"]{{color:{MUT} !important;font-size:13px;font-weight:500;border-bottom:2px solid transparent;}}
[role="tab"][aria-selected="true"]{{color:{R} !important;border-bottom:2px solid {R} !important;}}

/* Multiselect tags */
[data-baseweb="tag"]{{background:{R2} !important;color:{W} !important;}}

/* Cards */
.jcard{{
    background:{C1};border:1px solid {C2};border-top:3px solid {R};
    border-radius:8px;padding:14px 12px;text-align:center;margin-bottom:4px;
}}
.jcard .val{{font-family:'DM Mono',monospace;font-size:22px;font-weight:600;color:{W};}}
.jcard .lbl{{font-size:10px;color:{MUT};letter-spacing:0.1em;text-transform:uppercase;margin-top:4px;}}
.sec{{font-family:'DM Mono',monospace;font-size:10px;color:{R};
      letter-spacing:0.15em;text-transform:uppercase;
      border-bottom:1px solid {C2};padding-bottom:4px;margin-bottom:10px;}}
.div{{height:1px;background:linear-gradient(90deg,{R}66,{C2});margin:10px 0;}}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/scouting_app_data.csv")

B = dict(psv_med=29.45, hsr_bip=789.6, spr_bip=285.6, hi_bip=1086.3,
         hsr_otip=386.9, spr_otip=118.5, hi_otip=500.9, t_hsr=0.66, t_sprint=1.315)

TIER_COLORS = {
    "🔥 ELITE TARGET":"#CC0000","🟢 TOP TARGET":"#1B5E20",
    "🔵 INTERESTING":"#0D47A1","🟡 WATCHLIST":"#E65100","🔴 RISIKO":"#4A0D0D",
}
SPEED_COLORS = {
    "⚡ ELITE":"#CC0000","🔵 HIGH":"#1565C0",
    "🟡 FAST":"#0288D1","🟠 MEDIUM":"#EF6C00","—":"#333333",
}

def recalc_ifi(df, w_rq, w_dr, w_bt):
    df = df.copy()
    tw = w_rq+w_dr+w_bt
    if tw==0:
        df["IFI Index"]=0.0; df["IFI Punkte"]=0
    else:
        df["IFI Index"]=(
            df["Run Quality"].fillna(0)*(w_rq/tw)+
            df["Dribbling"].fillna(0)*(w_dr/tw)+
            df["Box Threat"].fillna(0)*(w_bt/tw)
        ).round(3)
        df["IFI Punkte"]=df["IFI Index"].apply(
            lambda v:5 if v>=2 else(4 if v>=1.5 else(3 if v>=0.5 else
                    (2 if v>=0 else(1 if v>=-0.5 else 0)))))
    df["Final Total"]=df["Physical Score"]+df["IFI Punkte"]
    def _tier(r):
        t,i=r["Final Total"],r["IFI Punkte"]
        if i<2: return "🟡 WATCHLIST" if t>=10 else "🔴 RISIKO"
        if t>=20: return "🔥 ELITE TARGET"
        if t>=17: return "🟢 TOP TARGET"
        if t>=14: return "🔵 INTERESTING"
        if t>=10: return "🟡 WATCHLIST"
        return "🔴 RISIKO"
    df["Final Tier"]=df.apply(_tier,axis=1)
    return df

df_raw = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:24px 0 16px;">
        <img src="data:image/png;base64,{LOGO_B64}"
             style="width:110px;filter:drop-shadow(0 0 16px #CC000088);">
        <div style="font-size:15px;font-weight:800;color:#FFFFFF;
                    margin-top:12px;letter-spacing:0.08em;">JAHN REGENSBURG</div>
        <div style="font-size:11px;color:#AAAAAA;letter-spacing:0.15em;
                    text-transform:uppercase;margin-top:4px;">Scouting · Wide Attacker</div>
    </div>
    <div class="div"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec">Filter</div>', unsafe_allow_html=True)
    ligen=sorted(df_raw["Liga"].unique())
    sel_ligen=st.multiselect("Liga", ligen, default=ligen)
    psv_min=st.slider("PSV-99 Minimum (km/h)", 27.0, 32.5, 29.45, 0.1, format="%.2f")
    ar=st.slider("Alter", int(df_raw["Alter"].min()), int(df_raw["Alter"].max()),
                 (int(df_raw["Alter"].min()), int(df_raw["Alter"].max())))
    mr=st.slider("Minuten", int(df_raw["Minuten"].min()), int(df_raw["Minuten"].max()),
                 (200, int(df_raw["Minuten"].max())), step=50)
    all_tiers=["🔥 ELITE TARGET","🟢 TOP TARGET","🔵 INTERESTING","🟡 WATCHLIST","🔴 RISIKO"]
    sel_tiers=st.multiselect("Final Tier", all_tiers, default=all_tiers)
    otip_gate=st.checkbox("Nur OTIP Pass ✅", value=False)
    all_typen=sorted(df_raw["Spielertyp"].unique())
    sel_typen=st.multiselect("Spielertyp", all_typen, default=all_typen)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec">🎯 IFI Gewichtung</div>', unsafe_allow_html=True)
    w_rq=st.slider("Run Quality", 0, 100, 25, 5, format="%d%%")
    w_dr=st.slider("Dribbling",   0, 100, 50, 5, format="%d%%")
    w_bt=st.slider("Box Threat",  0, 100, 25, 5, format="%d%%")
    tw=w_rq+w_dr+w_bt
    st.success("✓ Summe: 100%") if tw==100 else st.warning(f"Summe: {tw}% (sollte 100 sein)")

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec">Sortierung</div>', unsafe_allow_html=True)
    sort_col=st.selectbox("Sortieren nach", [
        "Final Total","Physical Score","PSV-99","IFI Index",
        "OTIP Score","BIP Score","Burst Score","Alter","Minuten"])

# ── FILTER ────────────────────────────────────────────────────────────────────
df=recalc_ifi(df_raw, w_rq, w_dr, w_bt)
mask=(df["Liga"].isin(sel_ligen)&(df["PSV-99"]>=psv_min)&
      (df["Alter"]>=ar[0])&(df["Alter"]<=ar[1])&
      (df["Minuten"]>=mr[0])&(df["Minuten"]<=mr[1])&
      df["Final Tier"].isin(sel_tiers)&df["Spielertyp"].isin(sel_typen))
if otip_gate: mask=mask&(df["OTIP Pass"]=="✅ YES")
df_f=df[mask].sort_values(sort_col,ascending=False).reset_index(drop=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
c_logo,c_title=st.columns([1,11])
with c_logo:
    st.markdown(f'''<div style="padding-top:4px;">
        <img src="data:image/png;base64,{LOGO_B64}"
             style="width:56px;filter:drop-shadow(0 2px 8px #CC000066);">
    </div>''', unsafe_allow_html=True)
with c_title:
    st.markdown(f'''
    <div style="padding-top:8px;">
        <span style="font-size:24px;font-weight:800;color:#FFFFFF;">Wide Attacker Scouting</span>
        <span style="font-size:13px;color:#777;margin-left:14px;">
            Jahn Regensburg &nbsp;·&nbsp; 7 Ligen &nbsp;·&nbsp;
            <span style="color:#CC0000;font-weight:700;">{len(df_f)} Spieler</span> nach Filter
        </span>
    </div>''', unsafe_allow_html=True)

st.markdown('<div class="div" style="margin:12px 0 18px;"></div>', unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
cols=st.columns(6)
kpis=[
    (len(df_f),"Spieler gesamt"),
    (len(df_f[df_f["Final Tier"].isin(["🔥 ELITE TARGET","🟢 TOP TARGET"])]),"Elite + Top"),
    (len(df_f[df_f["OTIP Pass"]=="✅ YES"]),"OTIP Pass ✅"),
    (f"{df_f['PSV-99'].max():.2f}" if len(df_f) else "—","Höchste PSV-99"),
    (f"{df_f['Final Total'].max():.1f}" if len(df_f) else "—","Bester Score /25"),
    (f"{int(df_f['Alter'].median())}" if len(df_f) else "—","Median Alter"),
]
for col,(val,lbl) in zip(cols,kpis):
    with col:
        st.markdown(f'<div class="jcard"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>',
                    unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1,tab2,tab3=st.tabs(["📋 Spieler-Liste","📊 Scatter-Plot","📖 Scoring Info"])

with tab1:
    st.markdown(f'<div style="font-size:11px;color:#666;font-family:DM Mono,monospace;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">{len(df_f)} Spieler · Sortiert nach {sort_col}</div>',
                unsafe_allow_html=True)
    if df_f.empty:
        st.info("Keine Spieler mit diesen Filtern.")
    else:
        disp=df_f[[
            "Spieler","Verein","Liga","Alter","Minuten",
            "Final Total","Final Tier","Physical Score",
            "IFI Punkte","IFI Index",
            "Speed Flag","PSV-99","Δ PSV-99","Speed Score",
            "OTIP Pass","OTIP Score","Δ HSR OTIP",
            "BIP Level","BIP Score","Δ HSR BIP",
            "Burst Score","Δ T→HSR",
            "Spielertyp","Run Quality","Dribbling","Box Threat",
            "Transferwert (€)",
        ]].copy()

        tier_bg=lambda v:{"🔥 ELITE TARGET":"background-color:#3D0000;color:#FF9999;font-weight:700",
                          "🟢 TOP TARGET":"background-color:#0A1F0A;color:#81C784;font-weight:700",
                          "🔵 INTERESTING":"background-color:#060E22;color:#90CAF9;font-weight:700",
                          "🟡 WATCHLIST":"background-color:#1F1000;color:#FFCC80;font-weight:700",
                          "🔴 RISIKO":"background-color:#1A0000;color:#EF9A9A;font-weight:700"}.get(v,"")
        psv_bg=lambda v:("" if pd.isna(v) else
                         "background-color:#3D0000;color:#FF9999;font-weight:700" if v>=32 else
                         "background-color:#0D1F50;color:#90CAF9;font-weight:700" if v>=31 else
                         "background-color:#003344;color:#80DEEA;font-weight:700" if v>=30.5 else
                         "background-color:#1F1000;color:#FFCC80;font-weight:700" if v>=29.45 else "color:#555")
        pos_d=lambda v:"" if pd.isna(v) else("color:#81C784" if v>0 else("color:#EF9A9A" if v<0 else ""))
        neg_d=lambda v:"" if pd.isna(v) else("color:#81C784" if v<0 else("color:#EF9A9A" if v>0 else ""))

        styled=(disp.style
            .map(tier_bg,subset=["Final Tier"])
            .map(psv_bg, subset=["PSV-99"])
            .map(pos_d,  subset=["Δ PSV-99","Δ HSR OTIP","Δ HSR BIP"])
            .map(neg_d,  subset=["Δ T→HSR"])
            .format({"PSV-99":"{:.2f}","Final Total":"{:.1f}","Physical Score":"{:.1f}",
                     "IFI Index":"{:.3f}","Run Quality":"{:.3f}","Dribbling":"{:.3f}","Box Threat":"{:.3f}",
                     "Δ PSV-99":"{:+.2f}","Δ HSR OTIP":"{:+.0f}",
                     "Δ HSR BIP":"{:+.0f}","Δ T→HSR":"{:+.3f}",
                     "Transferwert (€)":lambda v:f"€{int(v):,}" if pd.notna(v) else "—"},
                    na_rep="—"))
        st.dataframe(styled,use_container_width=True,height=520)
        st.download_button("⬇️ Export CSV",
                           df_f.to_csv(index=False).encode("utf-8"),
                           "jahn_scouting.csv","text/csv")

with tab2:
    numeric_cols=["PSV-99","Final Total","Physical Score","IFI Index",
                  "OTIP Score","BIP Score","Burst Score","Speed Score",
                  "Run Quality","Dribbling","Box Threat",
                  "HSR OTIP P30","HSR P60BIP","Time→HSR (s)","Alter","Minuten",
                  "Δ PSV-99","Δ HSR OTIP","Δ HSR BIP"]
    c1,c2,c3,c4=st.columns(4)
    with c1: x=st.selectbox("X-Achse",numeric_cols,index=0)
    with c2: y=st.selectbox("Y-Achse",numeric_cols,index=2)
    with c3: sz=st.selectbox("Punktgröße",["—"]+numeric_cols,index=0)
    with c4: cb=st.selectbox("Farbe",["Final Tier","Speed Flag","Spielertyp","Liga"],index=0)

    if df_f.empty:
        st.info("Keine Daten.")
    else:
        try:
            import plotly.express as px
            pdf=df_f.dropna(subset=[x,y]).copy()
            cm=TIER_COLORS if cb=="Final Tier" else(SPEED_COLORS if cb=="Speed Flag" else None)
            sv=None
            if sz!="—" and sz in pdf.columns:
                s=pd.to_numeric(pdf[sz],errors="coerce").fillna(0)
                sv=(((s-s.min())/(s.max()-s.min()+0.001))*20+6).tolist()
            fig=px.scatter(pdf,x=x,y=y,color=cb,color_discrete_map=cm,
                           hover_name="Spieler",
                           hover_data={"Verein":True,"Liga":True,"Alter":True,
                                       "Final Total":":.1f","PSV-99":":.2f",
                                       "OTIP Pass":True,cb:False},
                           size=sv,size_max=24,template="plotly_dark",height=520)
            if x=="PSV-99":
                fig.add_vline(x=B["psv_med"],line_dash="dash",line_color="#CC0000",
                              annotation_text="3.Liga Median",annotation_font_size=11)
            if y=="PSV-99":
                fig.add_hline(y=B["psv_med"],line_dash="dash",line_color="#CC0000")
            fig.update_layout(
                paper_bgcolor="#0D0D0D",plot_bgcolor="#181818",
                font_family="DM Sans",font_color="#AAAAAA",
                xaxis=dict(gridcolor="#2A2A2A",zeroline=False),
                yaxis=dict(gridcolor="#2A2A2A",zeroline=False),
                legend=dict(bgcolor="#181818",bordercolor="#2A2A2A",borderwidth=1),
                margin=dict(l=40,r=20,t=40,b=40))
            fig.update_traces(marker=dict(line=dict(width=0.5,color="#0D0D0D")))
            st.plotly_chart(fig,use_container_width=True)
        except Exception as e:
            st.error(f"Plot-Fehler: {e}")

with tab3:
    ca,cb_=st.columns(2)
    with ca:
        st.markdown("### Final Total /25")
        st.markdown("""
| Komponente | Faktor | Max |
|---|---|---|
| ⚡ Speed Score (0–4) | ×2.0 | 8 |
| 🏃 OTIP Score (0–4) | ×1.5 | 6 |
| 💥 BIP Score (0–4) | ×1.0 | 4 |
| 🚀 Burst Score (0–4) | ×0.5 | 2 |
| 🎯 IFI Punkte (0–5) | additiv | 5 |
| **Maximum** | | **25** |

**IFI Gate:** IFI Punkte < 2 → max. 🟡 WATCHLIST
        """)
    with cb_:
        st.markdown("### Final Tier")
        st.markdown("""
| Score | Tier |
|---|---|
| ≥20 + IFI≥2 | 🔥 ELITE TARGET |
| ≥17 + IFI≥2 | 🟢 TOP TARGET |
| ≥14 + IFI≥2 | 🔵 INTERESTING |
| ≥10 | 🟡 WATCHLIST |
| <10 | 🔴 RISIKO |

**Speed Flag:** ⚡ ELITE ≥32 · 🔵 HIGH ≥31 · 🟡 FAST ≥30.5 · 🟠 MEDIUM ≥29.45 · — darunter
        """)
    st.markdown("---")
    st.markdown("### 3.Liga Benchmark (Wide Attacker · ≥500 min · Saison 2024/25)")
    st.dataframe(pd.DataFrame([
        {"Metrik":"PSV-99 Median","Wert":"29.45 km/h","Layer":"Speed"},
        {"Metrik":"HSR P60BIP","Wert":"789.6m","Layer":"BIP"},
        {"Metrik":"Sprint P60BIP","Wert":"285.6m","Layer":"BIP"},
        {"Metrik":"HSR OTIP P30","Wert":"386.9m","Layer":"OTIP"},
        {"Metrik":"Sprint OTIP P30","Wert":"118.5m","Layer":"OTIP"},
        {"Metrik":"Time to HSR","Wert":"0.66s","Layer":"Burst"},
        {"Metrik":"Time to Sprint","Wert":"1.315s","Layer":"Burst"},
    ]),use_container_width=True,hide_index=True)
