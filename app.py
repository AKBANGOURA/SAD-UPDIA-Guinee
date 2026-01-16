import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
# Note : J'ai ajouté 'seuil_fao' pour que l'onglet 3 fonctionne aussi en mode "Tout"
filières_db = {
    'Riz': {'prod': 2250000, 'obj_2040': 5000000, 'ratio_besoin': 1.6, 'coef_roi': 850, 'seuil_fao': 100},
    'Maïs': {'prod': 850000, 'obj_2040': 2000000, 'ratio_besoin': 1.4, 'coef_roi': 650, 'seuil_fao': 55},
    'Fonio': {'prod': 550000, 'obj_2040': 1300000, 'ratio_besoin': 1.2, 'coef_roi': 450, 'seuil_fao': 40},
    'Cassave': {'prod': 1200000, 'obj_2040': 3000000, 'ratio_besoin': 1.3, 'coef_roi': 550, 'seuil_fao': 80}
}

# --- 4. BARRE LATÉRALE DE PILOTAGE ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Flag_of_Guinea.svg/1200px-Flag_of_Guinea.svg.png", width=150)
st.sidebar.title("Pilotage Stratégique")

# Variable Maîtresse : Ajout de l'option "Tout"
options_culture = ["Tout"] + list(filières_db.keys())
culture_select = st.sidebar.selectbox("Filière Agricole Prioritaire", options_culture, key="filiere_master")

scénario = st.sidebar.selectbox("Scénario d'investissement", ["Stagnation", "PNIASAN (Modéré)", "Vision 2040 (Ambitieux)"])
budget_total = st.sidebar.number_input("Budget Total (Milliards GNF)", min_value=1, value=2500)

st.sidebar.markdown("---")
st.sidebar.info("Auteur : Almamy BANGOURA Economiste statisticien, Expert en Data science et évaluation d'impact des politiques publiques")

# --- EXTRACTION ET CALCULS DYNAMIQUES (Le nouveau bloc logique) ---
if culture_select == "Tout":
    # On additionne les volumes pour la vision nationale
    base_prod = sum(f['prod'] for f in filières_db.values())
    obj_2040 = sum(f['obj_2040'] for f in filières_db.values())
    
    # On fait la moyenne pour les indicateurs de rendement/besoin
    d = {
        'prod': base_prod,
        'obj_2040': obj_2040,
        'ratio_besoin': np.mean([f['ratio_besoin'] for f in filières_db.values()]),
        'coef_roi': np.mean([f['coef_roi'] for f in filières_db.values()]),
        'seuil_fao': np.mean([f['seuil_fao'] for f in filières_db.values()])
    }
    r_besoin = d['ratio_besoin']
else:
    # Extraction classique pour une seule filière
    d = filières_db[culture_select]
    base_prod = d['prod']
    obj_2040 = d['obj_2040']
    r_besoin = d['ratio_besoin']

# --- 5. HEADER DYNAMIQUE ---
titre_header = "Toutes les filières" if culture_select == "Tout" else f"la filière {culture_select}"
st.title(f"SAD UPDIA : Pilotage de {titre_header}")
st.markdown(f"Analyse de souveraineté alimentaire basée sur les objectifs **Vision 2040**. Gouvernance de la politique agricole par les **données**.")

# --- 6. ONGLETS STRATÉGIQUES ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Diagnostic : Statistiques nationales", 
    "🤖 IA & Rendements : Résilience", 
    "🎯 Simulateur Vision : Guinée 2040", 
    "💰 Finance : Efficacité Budgétaire", 
    "🏭 Transformation & Valeur Ajoutée"
])

# --- 1. DÉFINITION DES DONNÉES (À placer avant les onglets) ---
# Ce dictionnaire assure la cohérence entre les barres, la synthèse et la carte
potentiels_regionaux = {
    'Riz': {'Boké': 0.12, 'Kindia': 0.15, 'Mamou': 0.08, 'Faranah': 0.15, 'Kankan': 0.25, 'Labé': 0.10, "N'Zérékoré": 0.14, 'Conakry': 0.01},
    'Maïs': {'Boké': 0.10, 'Kindia': 0.12, 'Mamou': 0.15, 'Faranah': 0.20, 'Kankan': 0.18, 'Labé': 0.10, "N'Zérékoré": 0.14, 'Conakry': 0.01},
    'Fonio': {'Boké': 0.05, 'Kindia': 0.08, 'Mamou': 0.20, 'Faranah': 0.15, 'Kankan': 0.12, 'Labé': 0.30, "N'Zérékoré": 0.09, 'Conakry': 0.01},
    'Cassave': {'Boké': 0.15, 'Kindia': 0.18, 'Mamou': 0.05, 'Faranah': 0.10, 'Kankan': 0.08, 'Labé': 0.07, "N'Zérékoré": 0.35, 'Conakry': 0.02},
    'Tout': {'Boké': 0.12, 'Kindia': 0.14, 'Mamou': 0.10, 'Faranah': 0.15, 'Kankan': 0.20, 'Labé': 0.12, "N'Zérékoré": 0.16, 'Conakry': 0.01}
}

# --- 2. CODE DU TAB 1 ---

with tab1:
    st.subheader(f"📊 Analyse Territoriale de la Production : {culture_select}")
    
    # --- SECTION A : MÉTRIQUES DE PERFORMANCE (Origine) ---
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Production {culture_select}", f"{base_prod:,} T", "+4.2%")
    m2.metric("Objectif National", f"{d['obj_2040']:,} T", "Cible 2040")
    besoin_import_calc = int((d['ratio_besoin'] - 1) * 100)
    m3.metric("Besoin Importé", f"{besoin_import_calc}%", "-2.1%")

    st.write("---")

    # --- SECTION B : RENDEMENTS & GAP (Origine) ---
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    rendement_moyen = base_prod / 800000 
    objectif_rendement = d['obj_2040'] / 800000
    gap_rendement = ((objectif_rendement - rendement_moyen) / rendement_moyen) * 100
    
    col_kpi1.metric("Rendement Actuel", f"{rendement_moyen:.2f} T/Ha")
    col_kpi2.metric("Yield Gap (Écart)", f"{gap_rendement:.1f}%", delta=f"{objectif_rendement:.2f} visé", delta_color="inverse")
    col_kpi3.metric("Souveraineté Actuelle", f"{(1/d['ratio_besoin'])*100:.1f}%")

    # --- SECTION C : LOGIQUE DE SPÉCIALISATION (33 Préfectures) ---
    prefectures_base = [
        {'Region': 'Boké', 'Pref': 'Boké', 'lat': 11.05, 'lon': -14.28},
        {'Region': 'Boké', 'Pref': 'Boffa', 'lat': 10.17, 'lon': -14.03},
        {'Region': 'Boké', 'Pref': 'Fria', 'lat': 10.45, 'lon': -13.58},
        {'Region': 'Boké', 'Pref': 'Gaoual', 'lat': 11.75, 'lon': -13.20},
        {'Region': 'Boké', 'Pref': 'Koundara', 'lat': 12.48, 'lon': -13.30},
        {'Region': 'Kindia', 'Pref': 'Kindia', 'lat': 10.05, 'lon': -12.85},
        {'Region': 'Kindia', 'Pref': 'Coyah', 'lat': 9.70, 'lon': -13.38},
        {'Region': 'Kindia', 'Pref': 'Dubréka', 'lat': 9.78, 'lon': -13.52},
        {'Region': 'Kindia', 'Pref': 'Forécariah', 'lat': 9.43, 'lon': -13.08},
        {'Region': 'Kindia', 'Pref': 'Télimélé', 'lat': 10.90, 'lon': -13.03},
        {'Region': 'Mamou', 'Pref': 'Mamou', 'lat': 10.38, 'lon': -12.08},
        {'Region': 'Mamou', 'Pref': 'Dalaba', 'lat': 10.68, 'lon': -12.25},
        {'Region': 'Mamou', 'Pref': 'Pita', 'lat': 11.05, 'lon': -12.40},
        {'Region': 'Faranah', 'Pref': 'Faranah', 'lat': 10.03, 'lon': -10.74},
        {'Region': 'Faranah', 'Pref': 'Dabola', 'lat': 10.74, 'lon': -11.11},
        {'Region': 'Faranah', 'Pref': 'Dinguiraye', 'lat': 11.48, 'lon': -10.71},
        {'Region': 'Faranah', 'Pref': 'Kissidougou', 'lat': 9.18, 'lon': -10.11},
        {'Region': 'Kankan', 'Pref': 'Kankan', 'lat': 10.38, 'lon': -9.30},
        {'Region': 'Kankan', 'Pref': 'Kérouané', 'lat': 9.26, 'lon': -9.01},
        {'Region': 'Kankan', 'Pref': 'Kouroussa', 'lat': 10.65, 'lon': -9.88},
        {'Region': 'Kankan', 'Pref': 'Siguiri', 'lat': 11.42, 'lon': -9.17},
        {'Region': 'Kankan', 'Pref': 'Mandiana', 'lat': 10.63, 'lon': -8.68},
        {'Region': 'Labé', 'Pref': 'Labé', 'lat': 11.32, 'lon': -12.28},
        {'Region': 'Labé', 'Pref': 'Koubia', 'lat': 11.58, 'lon': -11.89},
        {'Region': 'Labé', 'Pref': 'Lélouma', 'lat': 11.42, 'lon': -12.51},
        {'Region': 'Labé', 'Pref': 'Mali', 'lat': 12.08, 'lon': -12.29},
        {'Region': 'Labé', 'Pref': 'Tougué', 'lat': 11.44, 'lon': -11.66},
        {'Region': 'N\'Zérékoré', 'Pref': 'N\'Zérékoré', 'lat': 7.75, 'lon': -8.82},
        {'Region': 'N\'Zérékoré', 'Pref': 'Beyla', 'lat': 8.68, 'lon': -8.63},
        {'Region': 'N\'Zérékoré', 'Pref': 'Guéckédou', 'lat': 8.57, 'lon': -10.13},
        {'Region': 'N\'Zérékoré', 'Pref': 'Lola', 'lat': 7.80, 'lon': -8.53},
        {'Region': 'N\'Zérékoré', 'Pref': 'Macenta', 'lat': 8.54, 'lon': -9.47},
        {'Region': 'N\'Zérékoré', 'Pref': 'Yomou', 'lat': 7.56, 'lon': -9.26},
        {'Region': 'Conakry', 'Pref': 'Conakry', 'lat': 9.53, 'lon': -13.67}
    ]

    if culture_select == 'Riz':
        poids_map = {'Kankan': 0.08, 'Boké': 0.05, 'Kindia': 0.04, 'N\'Zérékoré': 0.04, 'Faranah': 0.03, 'Labé': 0.01, 'Mamou': 0.01, 'Conakry': 0.005}
    elif culture_select == 'Fonio':
        poids_map = {'Labé': 0.12, 'Mamou': 0.09, 'Faranah': 0.05, 'Boké': 0.03, 'Kindia': 0.02, 'Kankan': 0.015, 'N\'Zérékoré': 0.01, 'Conakry': 0.005}
    elif culture_select == 'Cassave':
        poids_map = {'N\'Zérékoré': 0.09, 'Kindia': 0.07, 'Boké': 0.06, 'Faranah': 0.04, 'Kankan': 0.02, 'Labé': 0.015, 'Mamou': 0.01, 'Conakry': 0.005}
    else:
        poids_map = {'Faranah': 0.07, 'Kankan': 0.06, 'N\'Zérékoré': 0.05, 'Kindia': 0.04, 'Boké': 0.03, 'Labé': 0.02, 'Mamou': 0.02, 'Conakry': 0.005}

    df_pref = pd.DataFrame(prefectures_base)
    df_pref['poids'] = df_pref['Region'].map(poids_map).fillna(0.01)
    df_pref['Production'] = df_pref['poids'] * base_prod
    df_pref['Efficacité'] = (df_pref['poids'] / df_pref['poids'].max()) * 100
    df_reg = df_pref.groupby('Region')['Production'].sum().reset_index().sort_values('Production', ascending=False)

    # --- SECTION D : CARTE (Placée en haut pour visibilité maximale) ---
    st.write("---")
    st.subheader(f"📍 Carte de l'Efficacité Territoriale : {culture_select} (33 Préfectures)")

    fig_map = px.scatter_mapbox(
        df_pref, lat="lat", lon="lon", 
        color="Efficacité", size="Production",
        hover_name="Pref", hover_data=["Region", "Production"],
        color_continuous_scale="RdYlGn", size_max=18, zoom=5.8,
        mapbox_style="carto-positron"
    )
    fig_map.update_layout(
        height=500, margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=dict(center=dict(lat=10.5, lon=-11.0))
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.write("---")

    # --- SECTION E : GRAPHIQUES (Côte à côte) ---
    c_left, c_right = st.columns(2)

    with c_left:
        st.write("**📊 Répartition par Région Administrative**")
        fig_prod = px.bar(
            df_reg, x='Region', y='Production', 
            color='Production', color_continuous_scale='Greens',
            text_auto='.2s'
        )
        fig_prod.update_layout(height=350, showlegend=False, coloraxis_showscale=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig_prod, use_container_width=True)

    with c_right:
        st.write("**🎯 Analyse de l'Objectif 2040**")
        df_gap = pd.DataFrame({
            'Indicateur': ['Production Actuelle', 'Déficit à combler'],
            'Valeur': [base_prod, max(0, d['obj_2040'] - base_prod)]
        })
        fig_gap = px.pie(
            df_gap, values='Valeur', names='Indicateur', hole=0.5,
            color='Indicateur',
            color_discrete_map={'Production Actuelle': '#009460', 'Déficit à combler': '#ce1126'}
        )
        fig_gap.update_layout(
            height=350, margin=dict(t=20, b=20, l=0, r=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_gap, use_container_width=True)

    # --- SECTION F : SYNTHÈSE DU DIAGNOSTIC ---
    st.write("---")
    st.subheader("📝 Synthèse du Diagnostic Stratégique")
    pref_leader = df_pref.loc[df_pref['Production'].idxmax()]
    region_leader = df_reg.iloc[0]['Region']
    poids_pref_leader = (pref_leader['Production'] / base_prod) * 100

    st.info(f"""
        **Analyse Spécialisée (Modèle UPDIA) :**
        * **Bastion de Production :** Pour la filière **{culture_select}**, la région de **{region_leader}** confirme son rôle de leader stratégique. La préfecture de **{pref_leader['Pref']}** concentre **{poids_pref_leader:.1f}%** de la production.
        * **Potentiel de Rendement :** L'écart de rendement de **{gap_rendement:.1f}%** indique une marge de progression massive pour atteindre les objectifs 2040.
        * **Recommandation :** Prioriser les investissements en mécanisation dans le cluster **{region_leader}** pour transformer ce potentiel en souveraineté alimentaire réelle.
    """)
    

with tab2:
    st.subheader(f"📊 Simulateur Agro-Climatique Avancé : {culture_select}")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.write("**🌍 Caractéristiques du Terroir**")
        type_sol = st.selectbox(
            "Type de Sol", 
            ["Alluvial (Fertile)", "Latéritique (Ferralitique)", "Sableux/Limoneux"], 
            help="Le type de sol influence la rétention d'eau et la réponse aux intrants."
        )
        
        st.write("**⚙️ Configuration Technique**")
        intrants = st.select_slider(
            "Niveau d'intensification", 
            options=["Traditionnel", "Semi-Mécanisé", "Intensif"], 
            key="ia_tech"
        )
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
            if irrig: 
                b_base += 0.3 # Bonus fixe irrigation
            
            impact = v_pluie / 100
            # Sensibilité selon le sol (Sableux = très sensible au manque d'eau)
            sens_sol = {"Alluvial (Fertile)": 1.0, "Latéritique (Ferralitique)": 1.3, "Sableux/Limoneux": 1.6}[s_type]
            
            if v_pluie < 0:
                if irrig:
                    impact = impact / 3 # Protection par l'eau maîtrisée
                else:
                    impact = impact * sens_sol # Impact aggravé par la nature du sol
            return max(0.1, b_base + impact)

        # Calcul des résultats basés sur la sélection dynamique
        rendement_final = calculer_rendement_complet(meteo_actuelle, irrigation, boost_base, type_sol)
        prod_simulee = base_prod * rendement_final

        st.metric(
            f"Production {culture_select} Projetée", 
            f"{int(prod_simulee):,} T", 
            f"{int((rendement_final-1)*100)}% vs Actuel"
        )

        # --- GESTION DES ALERTES CRITIQUES ---
        if meteo_actuelle < -20 and not irrigation:
            st.error(f"🚨 **ALERTE SÉCHERESSE** : Sans irrigation sur sol {type_sol}, la production de {culture_select} s'effondre.")
        
        if meteo_actuelle > 30:
            st.warning("🌊 **RISQUE D'INONDATION** : Un excès de pluie peut saturer les sols et détruire les récoltes.")

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
        fig_sens = px.line(
            df_sens, x='Pluie (%)', y='Production (T)', 
            title=f"Courbe de Résilience : Impact de la Pluie sur Sol {type_sol}",
            markers=True
        )
        fig_sens.add_vline(x=meteo_actuelle, line_dash="dot", line_color="red", annotation_text="Position Curseur")
        fig_sens.add_hline(y=base_prod, line_dash="dash", line_color="orange", annotation_text="Seuil Actuel")
        
        st.plotly_chart(fig_sens, use_container_width=True)

    st.success(f"**Synthèse IA :** L'interaction entre le sol **{type_sol}** et une variation pluviométrique de **{meteo_actuelle}%** donne un rendement équivalent de **{(rendement_moyen * rendement_final):.2f} T/Ha**.")

    st.write("---")
    st.subheader("📡 Anticipation des Crises (Imagerie Satellite & NDVI)")

    col_s1, col_s2 = st.columns([1, 2])

    with col_s1:
        st.write("**Analyse Sentinel-2 (Simulation)**")
        ndvi_obs = st.slider(
            "Indice de Végétation observé (NDVI)", 0.1, 0.9, 0.5, 
            help="Un NDVI < 0.4 indique un stress hydrique ou une anomalie de croissance."
        )
        
        seuil_alerte = 0.45
        if ndvi_obs < seuil_alerte:
            st.error(f"🚨 **ALERTE PRÉCOCE** : NDVI bas ({ndvi_obs}). Risque de crise détecté pour le {culture_select}.")
        else:
            st.success(f"✅ **Vigueur Optimale** : Le couvert végétal ({ndvi_obs}) est sain.")

    with col_s2:
        mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"]
        tendance_ndvi = [0.3, 0.35, 0.42, 0.48, 0.52, ndvi_obs]
        
        fig_satellite = px.area(
            x=mois, y=tendance_ndvi, 
            title=f"Suivi Satellite NDVI (Tendance 6 mois) - {culture_select}",
            labels={'x': 'Mois', 'y': 'Indice NDVI'},
            color_discrete_sequence=['#1e4d2b']
        )
        fig_satellite.add_hrect(y0=0.1, y1=0.4, line_width=0, fillcolor="red", opacity=0.2, annotation_text="ZONE DE CRISE")
        st.plotly_chart(fig_satellite, use_container_width=True)

    st.info(f"**Note Scientifique :** En cas de NDVI < {seuil_alerte}, le modèle UPDIA recommande l'activation des stocks de sécurité pour la filière **{culture_select}**.")

with tab3:
    st.subheader(f"🎯 Trajectoire de Souveraineté 2026-2040 : {culture_select}")
    
    # --- 1. PARAMÈTRES DE SIMULATION ---
    tx_croissance = st.slider("Taux de croissance annuel visé (%)", 1, 15, 6, key="growth_v")
    population_growth = 1.025  # Croissance démographique +2.5% par an
    years = list(range(2026, 2042)) # Projection sur 15 ans
    
    # --- 2. CALCULS DES CHEMINS (PROD VS BESOIN) ---
    # Production indexée sur le taux choisi
    prod_path = [base_prod * ((1 + tx_croissance/100)**i) for i in range(len(years))]
    # Besoins indexés sur la démographie et le ratio de départ
    besoin_path = [base_prod * d['ratio_besoin'] * (population_growth ** i) for i in range(len(years))]
    
    # Analyse nutritionnelle (Hypothèse : 70% de la production destinée à la consommation directe)
    pop_guinee = 14000000 
    dispo_hab = [(p * 0.7 * 1000) / (pop_guinee * (population_growth**i)) for i, p in enumerate(prod_path)]
    
    # Récupération dynamique du seuil FAO depuis votre base de données
    seuil_fao = d.get('seuil_fao', 50)

    # --- 3. GRAPHIQUE ÉQUILIBRE OFFRE/DEMANDE ---
    df_vision = pd.DataFrame({
        'Année': years, 
        'Production': prod_path, 
        'Besoins Population': besoin_path
    })
    
    fig_vision = px.line(
        df_vision, x='Année', y=['Production', 'Besoins Population'],
        title=f"Équilibre Offre/Demande : {culture_select} (Projection 2040)",
        color_discrete_map={'Production': '#009460', 'Besoins Population': '#ce1126'}
    )
    fig_vision.update_layout(yaxis_title="Volume (Tonnes)", hovermode="x unified")
    st.plotly_chart(fig_vision, use_container_width=True)

    # --- 4. ANALYSE DE LA SÉCURITÉ ALIMENTAIRE PAR HABITANT ---
    st.write("---")
    st.write(f"**🥗 Indicateur Social : Disponibilité de {culture_select} par habitant**")
    
    fig_nutri = px.area(
        x=years, y=dispo_hab, 
        title="Évolution de la ration projetée (kg/hab/an)",
        labels={'x': 'Année', 'y': 'kg/hab/an'},
        color_discrete_sequence=['#fcd116']
    )
    fig_nutri.add_hline(y=seuil_fao, line_dash="dash", line_color="red", 
                        annotation_text=f"Seuil FAO ({seuil_fao}kg)")
    st.plotly_chart(fig_nutri, use_container_width=True)

    # --- 5. LOGIQUE DE COHÉRENCE ET DIAGNOSTIC FINAL ---
    # Identification de l'année d'intersection
    annee_auto = next((years[i] for i, (p, b) in enumerate(zip(prod_path, besoin_path)) if p >= b), None)
    
    st.write("---")
    if annee_auto:
        st.success(f"✅ **SOUVERAINETÉ ATTEINTE** : L'autosuffisance alimentaire est prévue en **{annee_auto}** pour la culture : **{culture_select}**.")
        idx_auto = years.index(annee_auto)
        st.info(f"À cette échéance, la disponibilité par habitant sera de **{int(dispo_hab[idx_auto])} kg/an**, garantissant la sécurité alimentaire nationale.")
    else:
        # Calcul du déficit à l'horizon 2041
        gap_final = int(besoin_path[-1] - prod_path[-1])
        st.error(f"🚨 **DÉFICIT PRÉVU** : En 2041, un manque de **{gap_final:,} Tonnes** est à prévoir pour le {culture_select} avec un taux de {tx_croissance}%.")
        st.warning(f"La ration par habitant de **{int(dispo_hab[-1])} kg/an** restera sous le seuil critique de {seuil_fao} kg.")

with tab4:
    st.subheader(f"💰 Optimisation du Budget National : {culture_select}")
    
    # --- 1. CONFIGURATION BUDGÉTAIRE (Calculs Dynamiques) ---
    c_fin1, c_fin2 = st.columns([1, 1])
    
    with c_fin1:
        st.write("**Allocation des Ressources (Mds GNF)**")
        # Utilisation du budget global défini en barre latérale
        s_sem = st.slider("Semences Certifiées (Rouge)", 0, int(budget_total), int(budget_total*0.3))
        s_eng = st.slider("Engrais & Intrants (Jaune)", 0, int(budget_total - s_sem), int(budget_total*0.4))
        
        # Le reste est alloué automatiquement à la mécanisation
        s_mac = max(0, budget_total - s_sem - s_eng)
        
        st.info(f"Budget Mécanisation (Vert) : **{int(s_mac)} Mds GNF**")
        
        # --- CALCUL DU ROI AGRONOMIQUE ---
        # On récupère le coefficient spécifique à la culture (ex: 850 pour le Riz)
        coef = d.get('coef_roi', 500)
        
        # L'impact est pondéré : l'engrais a un boost de 1.2, la machine de 0.8 sur le tonnage immédiat
        gain_tonnes = (s_sem * coef) + (s_eng * coef * 1.2) + (s_mac * coef * 0.8)
        
        st.metric("Gain de Production Estimé", f"+{int(gain_tonnes):,} T", delta="Impact Investissement")

    with c_fin2:
        # --- 2. GRAPHIQUE AUX COULEURS NATIONALES ---
        st.write("**Structure de l'Investissement**")
        df_pie = pd.DataFrame({
            'Levier': ['Semences', 'Engrais', 'Machines'], 
            'Valeur': [s_sem, s_eng, s_mac]
        })
        fig_pie = px.pie(
            df_pie, values='Valeur', names='Levier', 
            hole=0.4,
            color='Levier', 
            color_discrete_map={'Semences':'#ce1126','Engrais':'#fcd116','Machines':'#009460'}
        )
        fig_pie.update_layout(margin=dict(t=20, b=20, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- 3. ANALYSE MACRO-ÉCONOMIQUE ---
    st.write("---")
    st.subheader("🏦 Impact Macro-économique (Balance Commerciale)")
    
    col_eco1, col_eco2 = st.columns(2)
    
    # Hypothèse : Prix moyen d'une tonne importée (Riz/Maïs) = 550 USD
    prix_import_usd = 550 
    economie_devises = gain_tonnes * prix_import_usd
    
    with col_eco1:
        st.metric(
            "Économie de Devises (USD)", 
            f"${economie_devises:,.0f}", 
            help="Montant économisé en devises étrangères en produisant localement ces tonnes."
        )
    
    with col_eco2:
        # Taux de change (USD/GNF) approx 8600. Conversion du budget Mds en GNF unité.
        valeur_gnf_economisee = economie_devises * 8600
        investissement_gnf = budget_total * 1_000_000_000
        rentabilite_ratio = valeur_gnf_economisee / investissement_gnf if investissement_gnf > 0 else 0
        
        st.metric(
            "Efficacité du GNF", 
            f"{rentabilite_ratio:.2f}x", 
            help="Pour 1 GNF investi, combien de GNF de valeur d'importation sont économisés."
        )

    # --- 4. RÉSUMÉ FINANCIER ---
    st.write("---")
    st.success(f"""
    **📌 Note de Synthèse Financière :**
    * **Impact Productif :** L'allocation de **{budget_total} Mds GNF** permet de générer un surplus de **{int(gain_tonnes):,} tonnes** de **{culture_select}**.
    * **Indépendance :** Cela représente une économie de **{economie_devises/1_000_000:.1f} millions de dollars** pour la balance commerciale.
    * **Efficacité :** Le levier 'Engrais' reste le plus performant à court terme pour maximiser le rendement de la filière **{culture_select}**.
    """)

with tab5:
    st.subheader(f"🏭 Industrialisation & Réduction des Pertes : {culture_select}")
    
    col_t1, col_t2 = st.columns([1, 2])
    
    with col_t1:
        st.write("**🏗️ Infrastructures de Stockage**")
        taux_perte = st.slider("Taux de pertes post-récolte actuel (%)", 5, 50, 30, help="Part de la récolte perdue par manque de silos ou de transport adéquat.")
        
        st.write("**⚙️ Capacité de Transformation**")
        niveau_transfo = st.radio(
            "Niveau d'industrialisation", 
            ["Manuel (Faible)", "Artisanal (Moyen)", "Industriel (Élevé)"],
            help="L'industrie permet de stabiliser les produits et de réduire le gaspillage."
        )
        
        # Logique de calcul du gain par l'efficience industrielle
        gain_efficience = {"Manuel (Faible)": 0.05, "Artisanal (Moyen)": 0.15, "Industriel (Élevé)": 0.30}[niveau_transfo]
        
        # Impact sur la disponibilité réelle basé sur base_prod
        perte_tonnes = base_prod * (taux_perte / 100)
        economie_perte = perte_tonnes * gain_efficience
        
        st.warning(f"Pertes actuelles : **{int(perte_tonnes):,} T**")
        st.success(f"Gain par l'industrie : **+{int(economie_perte):,} T** récupérées")

    with col_t2:
        st.write("**📦 Flux de Valeur : Du Champ à l'Assiette**")
        
        # Calcul de la disponibilité finale pour le graphique
        dispo_reelle = base_prod - perte_tonnes
        
        # Construction du graphique Waterfall
        fig_valeur = go.Figure(go.Waterfall(
            name = "Flux de production", 
            orientation = "v",
            measure = ["relative", "relative", "total"],
            x = ["Production Champ", "Pertes Post-Récolte", "Disponible Final"],
            textposition = "outside",
            text = [f"+{int(base_prod):,} T", f"-{int(perte_tonnes):,} T", f"={int(dispo_reelle):,} T"],
            y = [base_prod, -perte_tonnes, 0], # Le 0 avec 'total' déclenche le calcul automatique
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            increasing = {"marker":{"color":"#009460"}}, # Vert Guinée
            decreasing = {"marker":{"color":"#ce1126"}}, # Rouge Guinée
            totals = {"marker":{"color":"#fcd116"}}      # Jaune Guinée
        ))

        fig_valeur.update_layout(
            title = f"Analyse des pertes et disponibilité : {culture_select}",
            showlegend = False,
            height = 450
        )
        
        st.plotly_chart(fig_valeur, use_container_width=True)

    st.write("---")
    
    # Calcul d'impact pour la note de synthèse
    gain_potentiel_max = int(perte_tonnes * 0.5) # Simule une réduction de 50% des pertes
    
    st.info(f"""
    **💡 Analyse de la Valeur Ajoutée (Modèle UPDIA) :**
    En investissant dans des silos modernes et des unités de transformation pour la filière **{culture_select}**, 
    la Guinée pourrait récupérer environ **{gain_potentiel_max:,} tonnes** par an. 
    
    *Cela équivaut à nourrir **{(gain_potentiel_max * 1000 // d.get('seuil_fao', 50)):,.0f}** personnes supplémentaires sans augmenter les surfaces cultivées.*
    """)
















































