import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. CONFIGURATION AVANCÉE ---
st.set_page_config(page_title="SAD UPDIA - Vision 2040", layout="wide")

# --- 2. STYLE OFFICIEL (VERT FORÊT & OR) ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stMetric { background-color: #ffffff; border-left: 5px solid #009460; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); padding: 15px; border-radius: 10px; }
    h1 { color: #1e4d2b; font-family: 'Trebuchet MS'; border-bottom: 3px solid #ce1126; padding-bottom: 10px; }
    h3 { color: #1e4d2b; }
    .stTabs [aria-selected="true"] { background-color: #1e4d2b !important; color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES MULTI-FILIÈRES (PNIASAN) ---
filières_db = {
    'Riz': {'prod': 2250000, 'obj_2040': 5000000, 'ratio_besoin': 1.6, 'coef_roi': 850},
    'Maïs': {'prod': 850000, 'obj_2040': 2000000, 'ratio_besoin': 1.4, 'coef_roi': 650},
    'Fonio': {'prod': 550000, 'obj_2040': 1300000, 'ratio_besoin': 1.2, 'coef_roi': 450},
    'Cassave': {'prod': 1200000, 'obj_2040': 3000000, 'ratio_besoin': 1.3, 'coef_roi': 550}
}

# --- 4. BARRE LATÉRALE DE PILOTAGE ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Flag_of_Guinea.svg/1200px-Flag_of_Guinea.svg.png", width=150)
st.sidebar.title("Pilotage Stratégique")

# Variable Maîtresse : Choix de la culture
culture_select = st.sidebar.selectbox("Filière Agricole Prioritaire", list(filières_db.keys()), key="filiere_master")

scénario = st.sidebar.selectbox("Scénario d'investissement", ["Stagnation", "PNIASAN (Modéré)", "Vision 2040 (Ambitieux)"])
budget_total = st.sidebar.number_input("Budget Total (Milliards GNF)", min_value=1, value=2500)

st.sidebar.markdown("---")
st.sidebar.info("Expertise : PhD INRAE\nCellule : UPDIA\nVision Guinée 2040")

# Extraction des données dynamiques
d = filières_db[culture_select]
base_prod = d['prod']
obj_2040 = d['obj_2040']
r_besoin = d['ratio_besoin']

# --- 5. HEADER DYNAMIQUE ---
st.title(f"🇬🇳 SAD UPDIA : Pilotage de la filière {culture_select}")
st.markdown(f"Analyse de souveraineté alimentaire basée sur les objectifs **Vision 2040**.")

# --- 6. ONGLETS STRATÉGIQUES ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Diagnostic SNSA", "🤖 IA & Rendements", "🎯 Simulateur Vision 2040", "💰 Efficacité Budgétaire"])

with tab1:
    st.subheader(f"Analyse de la Production : {culture_select}")
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Production {culture_select}", f"{base_prod:,} T", "+4.2%")
    m2.metric("Objectif National", f"{obj_2040:,} T", "Cible 2040")
    m3.metric("Besoin Importé", f"{int((r_besoin-1)*100)}%", "-2.1%")

    # Répartition régionale simulée
    df_reg = pd.DataFrame({
        'Région': ['Basse Guinée', 'Moyenne Guinée', 'Haute Guinée', 'Guinée Forestière'],
        'Production': [base_prod*0.2, base_prod*0.15, base_prod*0.4, base_prod*0.25]
    })
    fig_prod = px.bar(df_reg, x='Région', y='Production', title=f"Répartition régionale du {culture_select}",
                      color='Région', color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig_prod, use_container_width=True)

with tab2:
    st.subheader("Optimisation des Rendements par l'IA (Modèle INRAE)")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        intrants = st.select_slider("Niveau de mécanisation & Intrants", options=["Traditionnel", "Semi-Mécanisé", "Intensif"])
        irrigation = st.checkbox("Déploiement Irrigation Maîtrisée")
        
        boost = 1.0
        if intrants == "Semi-Mécanisé": boost += 0.4
        if intrants == "Intensif": boost += 0.8
        if irrigation: boost += 0.5
        st.warning(f"Impact estimé sur le rendement : **+{int((boost-1)*100)}%**")
        
    with col_b:
        prod_simulee = base_prod * boost
        fig_ia = px.bar(x=['Actuel', 'Simulé (IA)'], y=[base_prod, prod_simulee], 
                        color=['Actuel', 'IA'], color_discrete_map={'Actuel': '#fcd116', 'IA': '#009460'},
                        title=f"Potentiel de production {culture_select} après optimisation")
        st.plotly_chart(fig_ia, use_container_width=True)

with tab3:
    st.subheader(f"Trajectoire de Souveraineté 2026-2040 : {culture_select}")
    tx_croissance = st.slider("Taux de croissance annuel visé (%)", 1, 15, 6)
    population_growth = 1.025 
    
    years = list(range(2026, 2042))
    prod_path = [base_prod * ((1 + tx_croissance/100)**i) for i in range(len(years))]
    besoin_path = [base_prod * r_besoin * (population_growth ** i) for i in range(len(years))]
    
    df_vision = pd.DataFrame({'Année': years, 'Production': prod_path, 'Besoins Population': besoin_path})
    fig_vision = px.line(df_vision, x='Année', y=['Production', 'Besoins Population'],
                        title=f"Équilibre Offre/Demande : {culture_select}",
                        color_discrete_map={'Production': '#009460', 'Besoins Population': '#ce1126'})
    st.plotly_chart(fig_vision, use_container_width=True)
    
    # --- LOGIQUE DE COHÉRENCE STRICTE ---
    annee_auto = next((years[i] for i, (p, b) in enumerate(zip(prod_path, besoin_path)) if p >= b), None)

    if annee_auto:
        st.success(f"✅ **SOUVERAINETÉ ATTEINTE** : L'autosuffisance alimentaire est atteinte en **{annee_auto}** pour la culture : **{culture_select}**.")
    else:
        gap = int(besoin_path[-1] - prod_path[-1])
        st.error(f"🚨 **DÉFICIT PRÉVU** : En 2041, un manque de {gap:,} Tonnes est à prévoir pour le {culture_select}. Intensifiez les investissements.")

with tab4:
    st.header(f"Efficacité Budgétaire : {culture_select}")
    c1, c2 = st.columns(2)
    with c1:
        b_semences = st.slider("Semences Certifiées", 0, int(budget_total), int(budget_total*0.3))
        b_engrais = st.slider("Engrais & Intrants", 0, int(budget_total - b_semences), int(budget_total*0.4))
        b_machines = st.slider("Mécanisation", 0, int(budget_total - b_semences - b_engrais), int(budget_total*0.3))
        st.info(f"Reliquat budget : {budget_total - (b_semences + b_engrais + b_machines)} Md GNF")

    with c2:
        coef = d['coef_roi']
        impact_total = (b_semences * coef) + (b_engrais * (coef*1.2)) + (b_machines * (coef*0.8))
        st.metric(f"Gain de Production ({culture_select})", f"+{int(impact_total):,} T", f"{impact_total/base_prod:.1%}")
        
        # Préparation des données pour le disque
        df_roi = pd.DataFrame({
            'Levier': ['Semences', 'Engrais', 'Machines'], 
            'Impact': [b_semences*coef, b_engrais*coef*1.2, b_machines*coef*0.8]
        })
        
        # --- APPLICATION DES COULEURS NATIONALES ---
        fig_roi = px.pie(
            df_roi, 
            values='Impact', 
            names='Levier', 
            title="Répartition de l'impact par levier",
            color='Levier',
            color_discrete_map={
                'Semences': '#009460',  # Vert
                'Engrais': '#fcd116',  # Jaune
                'Machines': '#ce1126' # Rouge
            }
        )
        
        st.plotly_chart(fig_roi, use_container_width=True)
st.markdown("---")

st.caption(f"SAD UPDIA | République de Guinée | Expertise PhD INRAE | Filière active : {culture_select}")

