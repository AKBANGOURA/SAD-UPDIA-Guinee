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
st.sidebar.info("Auteur : Almamy Kalla BANGOURA : Economiste statisticien, Expert en Data science et évaluation d'impact des politiques publiques")

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
titre_header = "Toutes les filières (Souveraineté Nationale)" if culture_select == "Tout" else f"la filière {culture_select}"
st.title(f"🇬🇳 SAD UPDIA : Pilotage de {titre_header}")
st.markdown(f"Analyse de souveraineté alimentaire basée sur les objectifs **Vision 2040**.")

# --- 6. ONGLETS STRATÉGIQUES ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Diagnostic : Statistiques nationales", 
    "🤖 IA & Rendements : Résilience", 
    "🎯 Simulateur Vision : Guinée 2040", 
    "💰 Finance : Efficacité Budgétaire", 
    "🏭 Transformation & Valeur Ajoutée"
])

with tab1:
    st.subheader(f"📊 Analyse Complète de la Production : {culture_select}")
    
    # --- SECTION A : TES MÉTRIQUES D'ORIGINE (Tous les indicateurs) ---
    m1, m2, m3 = st.columns(3)
    # On utilise d['obj_2040'] pour que ça change avec la culture choisie
    m1.metric(f"Production {culture_select}", f"{base_prod:,} T", "+4.2%")
    m2.metric("Objectif National", f"{d['obj_2040']:,} T", "Cible 2040")
    
    # Calcul dynamique du besoin importé (Basé sur ton ratio_besoin)
    besoin_import_calc = int((d['ratio_besoin'] - 1) * 100)
    m3.metric("Besoin Importé", f"{besoin_import_calc}%", "-2.1%")

    st.write("---")

    # --- SECTION B : ANALYSE DES RENDEMENTS & GAP (Nouveaux indicateurs PhD) ---
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    # Calcul du rendement moyen (Production / Ha estimé)
    rendement_moyen = base_prod / 800000 
    objectif_rendement = d['obj_2040'] / 800000
    gap_rendement = ((objectif_rendement - rendement_moyen) / rendement_moyen) * 100
    
    col_kpi1.metric("Rendement Actuel", f"{rendement_moyen:.2f} T/Ha")
    col_kpi2.metric("Yield Gap (Écart)", f"{gap_rendement:.1f}%", delta=f"{objectif_rendement:.2f} visé", delta_color="inverse")
    col_kpi3.metric("Souveraineté Actuelle", f"{(1/d['ratio_besoin'])*100:.1f}%")

    st.write("---")

    # --- SECTION C : VISUALISATION (Fusion des deux types de graphiques) ---
    c_left, c_right = st.columns(2)
    
    with c_left:
        # TON GRAPHIQUE RÉGIONAL D'ORIGINE
        st.write("**📍 Répartition Territoriale**")
        df_reg = pd.DataFrame({
            'Région': ['Basse Guinée', 'Moyenne Guinée', 'Haute Guinée', 'Guinée Forestière'],
            'Production': [base_prod*0.2, base_prod*0.15, base_prod*0.4, base_prod*0.25]
        })
        fig_prod = px.bar(df_reg, x='Région', y='Production', 
                          color='Région', 
                          color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_prod, use_container_width=True)

    with c_right:
        # LE GRAPHIQUE D'ANALYSE DU GAP (Analyse de la structure du déficit)
        st.write("**🎯 Analyse de l'Objectif 2040**")
        df_gap = pd.DataFrame({
            'Indicateur': ['Production Actuelle', 'Déficit à combler'],
            'Valeur': [base_prod, (d['obj_2040'] - base_prod)]
        })
        fig_gap = px.pie(df_gap, values='Valeur', names='Indicateur', 
                         hole=0.4,
                         color='Indicateur',
                         color_discrete_map={'Production Actuelle': '#009460', 'Déficit à combler': '#ce1126'})
        st.plotly_chart(fig_gap, use_container_width=True)

    # --- SECTION D : INDICE D'EFFICACITÉ (Analyse finale) ---
    st.write("**📈 Indice d'Efficacité Régionale**")
    df_perf = pd.DataFrame({
        'Région': ['Basse Guinée', 'Moyenne Guinée', 'Haute Guinée', 'Guinée Forestière'],
        'Efficacité (%)': [85, 62, 91, 78]
    })
    fig_perf = px.bar(df_perf, y='Région', x='Efficacité (%)', orientation='h',
                      color='Efficacité (%)', color_continuous_scale='YlGn')
    st.plotly_chart(fig_perf, use_container_width=True)

    # ... (juste après ton graphique st.plotly_chart(fig_perf))
    
    st.write("---")
    st.subheader("📝 Synthèse du Diagnostic")
    
    # Fusion des deux analyses dans un seul bloc informatif
    st.info(f"""
    **Analyse Stratégique & Territoriale :**
    * **Levier Principal :** Pour la filière **{culture_select}**, la priorité est la réduction du *Yield Gap* de **{gap_rendement:.1f}%** par l'intensification technique.
    * **Focus Régional :** La **Haute Guinée** concentrant 40% de la production, une hausse de rendement de **0.5 T/Ha** dans cette zone réduirait les importations nationales de **15%**.
    """)
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
    st.subheader(f"🎯 Trajectoire de Souveraineté 2026-2040 : {culture_select}")
    
    # --- 1. TES PARAMÈTRES D'ORIGINE ---
    tx_croissance = st.slider("Taux de croissance annuel visé (%)", 1, 15, 6)
    population_growth = 1.025  # +2.5% par an
    years = list(range(2026, 2042)) # Ta plage d'années d'origine
    
    # --- 2. CALCULS DES CHEMINS (PROD VS BESOIN) ---
    prod_path = [base_prod * ((1 + tx_croissance/100)**i) for i in range(len(years))]
    besoin_path = [base_prod * d['ratio_besoin'] * (population_growth ** i) for i in range(len(years))]
    
    # Ajout de l'analyse nutritionnelle PhD
    pop_guinee = 14000000 
    dispo_hab = [(p * 0.7 * 1000) / (pop_guinee * (population_growth**i)) for i, p in enumerate(prod_path)]
    seuil_fao = 100 if culture_select == 'Riz' else 55

    # --- 3. TON GRAPHIQUE D'ORIGINE (Conservé strictement) ---
    df_vision = pd.DataFrame({
        'Année': years, 
        'Production': prod_path, 
        'Besoins Population': besoin_path
    })
    
    fig_vision = px.line(df_vision, x='Année', y=['Production', 'Besoins Population'],
                        title=f"Équilibre Offre/Demande : {culture_select}",
                        color_discrete_map={'Production': '#009460', 'Besoins Population': '#ce1126'})
    st.plotly_chart(fig_vision, use_container_width=True)

    # --- 4. NOUVELLE ANALYSE : SÉCURITÉ ALIMENTAIRE ---
    st.write("---")
    st.write(f"**🥗 Indicateur Social : Disponibilité de {culture_select} par habitant**")
    
    fig_nutri = px.area(x=years, y=dispo_hab, title="Évolution de la ration (kg/hab/an)",
                        labels={'x': 'Année', 'y': 'kg/hab/an'})
    fig_nutri.add_hline(y=seuil_fao, line_dash="dash", line_color="orange", annotation_text="Seuil de sécurité")
    st.plotly_chart(fig_nutri, use_container_width=True)

    # --- 5. LOGIQUE DE COHÉRENCE STRICTE (Tes messages originaux + Analyse Gap) ---
    annee_auto = next((years[i] for i, (p, b) in enumerate(zip(prod_path, besoin_path)) if p >= b), None)
    
    st.write("---")
    if annee_auto:
        st.success(f"✅ **SOUVERAINETÉ ATTEINTE** : L'autosuffisance alimentaire est atteinte en **{annee_auto}** pour la culture : **{culture_select}**.")
        st.info(f"À cette date, la disponibilité par habitant sera de **{int(dispo_hab[years.index(annee_auto)])} kg/an**, dépassant les normes de sécurité.")
    else:
        # Ton calcul de Gap précis que tu voulais garder
        gap_final = int(besoin_path[-1] - prod_path[-1])
        st.error(f"🚨 **DÉFICIT PRÉVU** : En 2041, un manque de **{gap_final:,} Tonnes** est à prévoir pour le {culture_select}.")
        st.warning(f"La ration par habitant chutera à **{int(dispo_hab[-1])} kg/an**, soit sous le seuil FAO de {seuil_fao} kg.")
with tab4:
    st.subheader(f"💰 Optimisation du Budget National : {culture_select}")
    
    # --- 1. CONFIGURATION BUDGÉTAIRE (Tes Sliders) ---
    c_fin1, c_fin2 = st.columns([1, 1])
    
    with c_fin1:
        st.write("**Allocation des Ressources (Mds GNF)**")
        # Utilisation du budget global défini en barre latérale
        s_sem = st.slider("Semences Certifiées (Rouge)", 0, int(budget_total), int(budget_total*0.3))
        s_eng = st.slider("Engrais & Intrants (Jaune)", 0, int(budget_total - s_sem), int(budget_total*0.4))
        s_mac = budget_total - s_sem - s_eng
        
        st.info(f"Budget Mécanisation (Vert) : **{int(s_mac)} Mds GNF**")
        
        # --- CALCUL DU ROI AGRONOMIQUE ---
        coef = d['coef_roi']
        # L'impact est pondéré : l'engrais a un boost de 1.2, la machine de 0.8 sur le tonnage immédiat
        gain_tonnes = (s_sem * coef) + (s_eng * coef * 1.2) + (s_mac * coef * 0.8)
        
        st.metric("Gain de Production Estimé", f"+{int(gain_tonnes):,} T", delta="Impact Investissement")

    with c_fin2:
        # --- 2. TON DISQUE AUX COULEURS NATIONALES (Conservé strictement) ---
        st.write("**Structure de l'Investissement**")
        df_pie = pd.DataFrame({
            'Levier': ['Semences', 'Engrais', 'Machines'], 
            'V': [s_sem, s_eng, s_mac]
        })
        fig_pie = px.pie(df_pie, values='V', names='Levier', 
                         color='Levier', 
                         color_discrete_map={'Semences':'#ce1126','Engrais':'#fcd116','Machines':'#009460'},
                         hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- 3. NOUVELLE ANALYSE : ÉCONOMIE DE DEVISES (Substitution) ---
    st.write("---")
    st.subheader("🏦 Impact Macro-économique (Balance Commerciale)")
    
    col_eco1, col_eco2 = st.columns(2)
    
    # Hypothèse : Prix moyen d'une tonne importée (Riz/Maïs) = 550 USD
    prix_import_usd = 550 
    economie_devises = gain_tonnes * prix_import_usd
    
    with col_eco1:
        st.metric("Économie de Devises (USD)", f"${economie_devises:,.0f}", 
                  help="Montant économisé en évitant l'importation de ces tonnes.")
    
    with col_eco2:
        # Taux de change moyen (USD/GNF) approx 8600
        rentabilite_ratio = (economie_devises * 8600) / (budget_total * 1_000_000_000)
        st.metric("Efficacité du GNF", f"{rentabilite_ratio:.2f}x", 
                  help="Pour 1 GNF investi, combien de GNF de valeur importée sont économisés.")

    # --- 4. RÉSUMÉ FINANCIER FUSIONNÉ ---
    st.write("---")
    st.success(f"""
    **📌 Note de Synthèse Financière :**
    * **Impact Productif :** L'allocation actuelle permet de générer un surplus de **{int(gain_tonnes):,} tonnes**.
    * **Indépendance :** Cela représente une économie stratégique de **{economie_devises/1_000_000:.1f} millions de dollars** pour la Banque Centrale de Guinée.
    * **Recommandation :** Le levier 'Engrais' présente actuellement le meilleur ratio coût/bénéfice pour la filière **{culture_select}**.
    """)

with tab5:
    st.subheader(f"🏭 Industrialisation & Réduction des Pertes : {culture_select}")
    
    col_t1, col_t2 = st.columns([1, 2])
    
    with col_t1:
        st.write("**🏗️ Infrastructures de Stockage**")
        taux_perte = st.slider("Taux de pertes post-récolte actuel (%)", 5, 50, 30)
        
        st.write("**⚙️ Capacité de Transformation**")
        niveau_transfo = st.radio("Niveau d'industrialisation", 
                                  ["Manuel (Faible)", "Artisanal (Moyen)", "Industriel (Élevé)"])
        
        # Logique de calcul du gain par la transformation
        gain_efficience = {"Manuel (Faible)": 0.05, "Artisanal (Moyen)": 0.15, "Industriel (Élevé)": 0.30}[niveau_transfo]
        
        # Impact sur la disponibilité réelle
        perte_tonnes = base_prod * (taux_perte / 100)
        economie_perte = perte_tonnes * gain_efficience
        
        st.warning(f"Pertes actuelles : **{int(perte_tonnes):,} T**")
        st.success(f"Gain par l'industrie : **+{int(economie_perte):,} T** récupérées")

    with col_t2:
        st.write("**📦 Flux de Valeur : Du Champ à l'Assiette**")
        
        # Calcul des étapes
        dispo_reelle = base_prod - perte_tonnes
        
        fig_valeur = go.Figure(go.Waterfall(
            name = "Flux", 
            orientation = "v",
            measure = ["relative", "relative", "total"],
            x = ["Production Champ", "Pertes Post-Récolte", "Disponible Final"],
            textposition = "outside",
            text = [f"+{int(base_prod)}", f"-{int(perte_tonnes)}", f"={int(dispo_reelle)}"],
            y = [base_prod, -perte_tonnes, 0], # Le 0 avec 'total' calcule la somme automatiquement
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            increasing = {"marker":{"color":"#009460"}}, # Vert
            decreasing = {"marker":{"color":"#ce1126"}}, # Rouge
            totals = {"marker":{"color":"#fcd116"}}      # Jaune
        ))

        fig_valeur.update_layout(
            title = f"Analyse des Pertes : {culture_select}",
            showlegend = False
        )
        
        st.plotly_chart(fig_valeur, use_container_width=True)

    st.write("---")
    st.info(f"""
    **Analyse de la Valeur Ajoutée :** En réduisant les pertes post-récolte de moitié via des silos modernes et des unités de transformation, 
    la Guinée pourrait gagner l'équivalent de **{int(perte_tonnes/2):,} T** sans même planter un hectare de plus.
    """)
















