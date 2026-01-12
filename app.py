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
    st.subheader(f"Simulateur Agro-Climatique Avancé : {culture_select}")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.write("**🌍 Caractéristiques du Terroir**")
        type_sol = st.selectbox("Type de Sol", ["Alluvial (Fertile)", "Latéritique (Ferralitique)", "Sableux/Limoneux"], 
                               help="Le type de sol influence la rétention d'eau et la réponse aux intrants.")
        
        st.write("**⚙️ Configuration Technique**")
        intrants = st.select_slider("Niveau d'intensification", options=["Traditionnel", "Semi-Mécanisé", "Intensif"], key="ia_tech")
        irrigation = st.checkbox("Irrigation Maîtrisée", help="Essentiel pour sécuriser le rendement face aux aléas.")
        
        st.write("---")
        st.write("**☁️ Facteur Pluviométrique**")
        meteo_actuelle = st.slider("Variation de la pluie (%)", -50, 50, 0)
        
        # --- LOGIQUE DE CALCUL (PARAMÈTRES INRAE) ---
        # 1. Facteur Sol
        f_sol = {"Alluvial (Fertile)": 1.2, "Latéritique (Ferralitique)": 0.8, "Sableux/Limoneux": 0.9}[type_sol]
        
        # 2. Boost technique de base
        boost_base = {"Traditionnel": 1.0, "Semi-Mécanisé": 1.4, "Intensif": 1.9}[intrants] * f_sol
        
        def calculer_rendement_complet(v_pluie, irrig, b_base, s_type):
            if irrig: b_base += 0.3 # Bonus fixe irrigation
            
            impact = v_pluie / 100
            # Sensibilité selon le sol (Sableux = très sensible au manque d'eau)
            sens_sol = {"Alluvial (Fertile)": 1.0, "Latéritique (Ferralitique)": 1.3, "Sableux/Limoneux": 1.6}[s_type]
            
            if v_pluie < 0:
                if irrig:
                    impact = impact / 3 # Protection par l'eau maîtrisée
                else:
                    impact = impact * sens_sol # Impact aggravé par la nature du sol
            return max(0.1, b_base + impact)

        rendement_final = calculer_rendement_complet(meteo_actuelle, irrigation, boost_base, type_sol)
        prod_simulee = base_prod * rendement_final

        st.metric(f"Production {culture_select} Projetée", f"{int(prod_simulee):,} T", 
                  f"{int((rendement_final-1)*100)}% vs Actuel")

        # --- GESTION DES ALERTES CRITIQUES ---
        if meteo_actuelle < -20 and not irrigation:
            st.error(f"🚨 **ALERTE SÉCHERESSE** : Sans irrigation sur sol {type_sol}, la production de {culture_select} s'effondre malgré les intrants.")
        
        if meteo_actuelle > 30:
            st.warning("🌊 **RISQUE D'INONDATION** : Un excès de pluie peut saturer les sols et détruire les cultures.")

    with col_b:
        # 1. GRAPHIQUE DE COMPARAISON (REMIS À JOUR)
        fig_comp = px.bar(
            x=['Production Actuelle', f'Projection IA ({culture_select})'], 
            y=[base_prod, prod_simulee], 
            color=['Actuel', 'IA'],
            color_discrete_map={'Actuel': '#fcd116', 'IA': '#009460' if prod_simulee >= base_prod else '#ce1126'},
            title=f"Comparaison : Actuel vs Simulation {culture_select}"
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        # 2. COURBE DE SENSIBILITÉ (RÉSILIENCE)
        pluie_range = np.linspace(-50, 50, 21)
        rendements_courbe = [base_prod * calculer_rendement_complet(p, irrigation, boost_base, type_sol) for p in pluie_range]
        
        df_sens = pd.DataFrame({'Pluie (%)': pluie_range, 'Production (T)': rendements_courbe})
        fig_sens = px.line(df_sens, x='Pluie (%)', y='Production (T)', 
                           title=f"Courbe de Résilience : Impact de la Pluie sur Sol {type_sol}",
                           markers=True)
        fig_sens.add_vline(x=meteo_actuelle, line_dash="dot", line_color="red", annotation_text="Position Curseur")
        fig_sens.add_hline(y=base_prod, line_dash="dash", line_color="orange", annotation_text="Seuil Actuel")
        
        st.plotly_chart(fig_sens, use_container_width=True)
    st.success(f"**Synthèse IA :** L'interaction entre le sol **{type_sol}** et une variation pluviométrique de **{meteo_actuelle}%** donne un rendement de **{rendement_final:.2f} T/Ha** (équivalent).")
st.write("---")
st.subheader("📡 Anticipation des Crises (Imagerie Satellite & NDVI)")

col_s1, col_s2 = st.columns([1, 2])

with col_s1:
    st.write("**Analyse Sentinel-2 (Simulation)**")
    # Simulation d'un indice NDVI (0.0 à 1.0)
    ndvi_obs = st.slider("Indice de Végétation observé (NDVI)", 0.1, 0.9, 0.5, 
                         help="Un NDVI < 0.4 indique souvent un stress hydrique ou une anomalie de croissance.")
    
    # Logique d'anticipation
    seuil_alerte = 0.45
    alerte_crise = ndvi_obs < seuil_alerte
    
    if alerte_crise:
        st.error(f"🚨 **ALERTE PRÉCOCE** : Le NDVI est anormalement bas ({ndvi_obs}). Risque de crise alimentaire détecté pour le {culture_select}.")
    else:
        st.success(f"✅ **Vigueur Optimale** : Le couvert végétal ({ndvi_obs}) est conforme aux moyennes saisonnières.")

with col_s2:
    # Graphique de tendance satellite (Simulé sur les 6 derniers mois)
    mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"]
    # On génère une courbe qui finit par la valeur du slider
    tendance_ndvi = [0.3, 0.35, 0.42, 0.48, 0.52, ndvi_obs]
    
    fig_satellite = px.area(x=mois, y=tendance_ndvi, 
                            title=f"Suivi Satellite NDVI (Tendance 6 mois) - {culture_select}",
                            labels={'x': 'Mois', 'y': 'Indice NDVI'},
                            color_discrete_sequence=['#1e4d2b'])
    
    # Zone d'alerte rouge
    fig_satellite.add_hrect(y0=0.1, y1=0.4, line_width=0, fillcolor="red", opacity=0.2, annotation_text="ZONE DE CRISE")
    
    st.plotly_chart(fig_satellite, use_container_width=True)

st.info(f"""
**Note Scientifique :** Ce module simule l'intégration de données multispectrales. 
En cas de NDVI < {seuil_alerte}, le modèle UPDIA recommande l'activation immédiate des stocks de sécurité 
et une aide d'urgence pour la filière **{culture_select}**.
""")

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







