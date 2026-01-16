import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests

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
    'Riz': {'prod': 2250000, 'obj_2040': 5000000, 'ratio_besoin': 1.6, 'coef_roi': 850, 'seuil_fao': 100},
    'Maïs': {'prod': 850000, 'obj_2040': 2000000, 'ratio_besoin': 1.4, 'coef_roi': 650, 'seuil_fao': 55},
    'Fonio': {'prod': 550000, 'obj_2040': 1300000, 'ratio_besoin': 1.2, 'coef_roi': 450, 'seuil_fao': 40},
    'Cassave': {'prod': 1200000, 'obj_2040': 3000000, 'ratio_besoin': 1.3, 'coef_roi': 550, 'seuil_fao': 80}
}

# --- 4. BARRE LATÉRALE DE PILOTAGE ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Flag_of_Guinea.svg/1200px-Flag_of_Guinea.svg.png", width=150)
st.sidebar.title("Pilotage Stratégique")
st.sidebar.markdown("**UPDIA** : Unité de Pilotage du Développement Industriel Agricole")

options_culture = ["Tout"] + list(filières_db.keys())
culture_select = st.sidebar.selectbox("Filière Agricole Prioritaire", options_culture, key="filiere_master")

scénario = st.sidebar.selectbox("Scénario d'investissement", ["Stagnation", "PNIASAN (Modéré)", "Vision 2040 (Ambitieux)"])
budget_total = st.sidebar.number_input("Budget Total (Milliards GNF)", min_value=1, value=2500)

st.sidebar.markdown("---")
st.sidebar.info("Auteur : Almamy BANGOURA Economiste statisticien, Expert en Data science")

# --- EXTRACTION ET CALCULS DYNAMIQUES ---
if culture_select == "Tout":
    base_prod = sum(f['prod'] for f in filières_db.values())
    obj_2040 = sum(f['obj_2040'] for f in filières_db.values())
    d = {
        'prod': base_prod,
        'obj_2040': obj_2040,
        'ratio_besoin': np.mean([f['ratio_besoin'] for f in filières_db.values()]),
        'coef_roi': np.mean([f['coef_roi'] for f in filières_db.values()]),
        'seuil_fao': np.mean([f['seuil_fao'] for f in filières_db.values()])
    }
else:
    d = filières_db[culture_select]
    base_prod = d['prod']
    obj_2040 = d['obj_2040']

# --- 5. HEADER DYNAMIQUE ---
titre_header = "Toutes les filières" if culture_select == "Tout" else f"la filière {culture_select}"
st.title(f"SAD UPDIA : Pilotage de {titre_header}")
st.markdown("Analyse de souveraineté alimentaire basée sur les objectifs **Vision 2040**. Gouvernance par les **données**.")

# --- 6. ONGLETS STRATÉGIQUES ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Diagnostic", "🤖 IA & Résilience", "🎯 Simulateur 2040", "💰 Finance", "🏭 Transformation"
])

with tab1:
    st.subheader(f"📊 Analyse Complète : {culture_select}")
    
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Production {culture_select}", f"{base_prod:,} T", "+4.2%")
    m2.metric("Objectif National", f"{d['obj_2040']:,} T", "Cible 2040")
    besoin_import_calc = int((d['ratio_besoin'] - 1) * 100)
    m3.metric("Besoin Importé", f"{besoin_import_calc}%", "-2.1%")

    st.write("---")

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    rendement_moyen = base_prod / 800000 
    objectif_rendement = d['obj_2040'] / 800000
    gap_rendement = ((objectif_rendement - rendement_moyen) / rendement_moyen) * 100
    
    col_kpi1.metric("Rendement Actuel", f"{rendement_moyen:.2f} T/Ha")
    col_kpi2.metric("Yield Gap (Écart)", f"{gap_rendement:.1f}%", delta=f"{objectif_rendement:.2f} visé", delta_color="inverse")
    col_kpi3.metric("Souveraineté Actuelle", f"{(1/d['ratio_besoin'])*100:.1f}%")

    st.write("---")

    c_left, c_right = st.columns(2)
    with c_left:
        st.write("**📍 Répartition Territoriale**")
        df_reg = pd.DataFrame({
            'Région': ['Basse Guinée', 'Moyenne Guinée', 'Haute Guinée', 'Guinée Forestière'],
            'Production': [base_prod*0.2, base_prod*0.15, base_prod*0.4, base_prod*0.25]
        })
        fig_prod = px.bar(df_reg, x='Région', y='Production', color='Région', color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_prod, use_container_width=True)

    with c_right:
        st.write("**🎯 Analyse de l'Objectif 2040**")
        df_gap = pd.DataFrame({
            'Indicateur': ['Production Actuelle', 'Déficit à combler'],
            'Valeur': [base_prod, (d['obj_2040'] - base_prod)]
        })
        fig_gap = px.pie(df_gap, values='Valeur', names='Indicateur', hole=0.4, color='Indicateur',
                         color_discrete_map={'Production Actuelle': '#009460', 'Déficit à combler': '#ce1126'})
        st.plotly_chart(fig_gap, use_container_width=True)

    # --- SECTION D : CARTOGRAPHIE DYNAMIQUE (Remplissage Régional) ---
    st.write("---")
    st.write("**📍 Cartographie de l'Efficacité Régionale (Dynamique)**")

    potentiel_regional = {
        'Riz': {'Basse Guinée': 1.1, 'Moyenne Guinée': 0.7, 'Haute Guinée': 1.2, 'Guinée Forestière': 1.0},
        'Maïs': {'Basse Guinée': 0.8, 'Moyenne Guinée': 1.1, 'Haute Guinée': 0.9, 'Guinée Forestière': 1.2},
        'Fonio': {'Basse Guinée': 0.6, 'Moyenne Guinée': 1.3, 'Haute Guinée': 1.1, 'Guinée Forestière': 0.7},
        'Cassave': {'Basse Guinée': 1.2, 'Moyenne Guinée': 0.8, 'Haute Guinée': 0.8, 'Guinée Forestière': 1.2},
        'Tout': {'Basse Guinée': 1.0, 'Moyenne Guinée': 1.0, 'Haute Guinée': 1.0, 'Guinée Forestière': 1.0}
    }

    mult_scen = {"Stagnation": 0.8, "PNIASAN (Modéré)": 1.1, "Vision 2040 (Ambitieux)": 1.4}
    coeff_carte = (budget_total / 2500) * mult_scen.get(scénario, 1.0)
    regions_list = ['Basse Guinée', 'Moyenne Guinée', 'Haute Guinée', 'Guinée Forestière']
    scores_carte = [min(100, potentiel_regional.get(culture_select, potentiel_regional['Tout'])[r] * 70 * coeff_carte) for r in regions_list]
    df_map = pd.DataFrame({'Region_ID': regions_list, 'Efficacité (%)': scores_carte})

    fig_map = px.choropleth(
        df_map,
        geojson="https://raw.githubusercontent.com/deldersveld/topojson/master/countries/guinea/guinea-regions.json",
        locations="Region_ID",
        featureidkey="properties.NAME_1",
        color="Efficacité (%)",
        color_continuous_scale="RdYlGn",
        range_color=(40, 100),
        scope="africa"
    )
    fig_map.update_geos(visible=True, showcountries=True, countrycolor="Black", fitbounds="locations")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
    st.plotly_chart(fig_map, use_container_width=True)

    st.write("---")
    st.info(f"**Priorité :** Réduction du Yield Gap de **{gap_rendement:.1f}%** pour {culture_select}.")

with tab2:
    st.subheader(f"🤖 Simulateur Agro-Climatique : {culture_select}")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.write("**🌍 Terroir & Technique**")
        type_sol = st.selectbox("Type de Sol", ["Alluvial (Fertile)", "Latéritique (Ferralitique)", "Sableux/Limoneux"])
        intrants = st.select_slider("Niveau d'intensification", options=["Traditionnel", "Semi-Mécanisé", "Intensif"])
        irrigation = st.checkbox("Irrigation Maîtrisée")
        meteo_actuelle = st.slider("Variation de la pluie (%)", -50, 50, 0)
        
        f_sol = {"Alluvial (Fertile)": 1.2, "Latéritique (Ferralitique)": 0.8, "Sableux/Limoneux": 0.9}[type_sol]
        boost_base = {"Traditionnel": 1.0, "Semi-Mécanisé": 1.4, "Intensif": 1.9}[intrants] * f_sol
        
        def calculer_rendement_complet(v_pluie, irrig, b_base, s_type):
            if irrig: b_base += 0.3
            impact = v_pluie / 100
            sens_sol = {"Alluvial (Fertile)": 1.0, "Latéritique (Ferralitique)": 1.3, "Sableux/Limoneux": 1.6}[s_type]
            if v_pluie < 0:
                impact = impact / 3 if irrig else impact * sens_sol
            return max(0.1, b_base + impact)

        rendement_final = calculer_rendement_complet(meteo_actuelle, irrigation, boost_base, type_sol)
        prod_simulee = base_prod * rendement_final
        st.metric("Production Projetée", f"{int(prod_simulee):,} T", f"{int((rendement_final-1)*100)}%")

    with col_b:
        fig_comp = px.bar(x=['Actuel', 'IA Simulation'], y=[base_prod, prod_simulee], color=['Actuel', 'IA'],
                          color_discrete_map={'Actuel': '#fcd116', 'IA': '#009460'}, title="Comparaison Actuel vs IA")
        st.plotly_chart(fig_comp, use_container_width=True)
        pluie_range = np.linspace(-50, 50, 21)
        rendements_courbe = [base_prod * calculer_rendement_complet(p, irrigation, boost_base, type_sol) for p in pluie_range]
        df_sens = pd.DataFrame({'Pluie (%)': pluie_range, 'Production (T)': rendements_courbe})
        st.plotly_chart(px.line(df_sens, x='Pluie (%)', y='Production (T)', title="Courbe de Résilience"), use_container_width=True)

    st.write("---")
    st.subheader("📡 Anticipation Satellite (NDVI)")
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        ndvi_obs = st.slider("Indice NDVI observé", 0.1, 0.9, 0.5)
        if ndvi_obs < 0.45: st.error("🚨 ALERTE PRÉCOCE : Stress végétal détecté.")
        else: st.success("✅ Vigueur conforme.")
    with col_s2:
        st.plotly_chart(px.area(x=["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"], y=[0.3, 0.35, 0.42, 0.48, 0.52, ndvi_obs], title="Tendance NDVI"), use_container_width=True)

with tab3:
    st.subheader(f"🎯 Simulateur Vision 2040 : {culture_select}")
    tx_croissance = st.slider("Taux de croissance annuel visé (%)", 1, 15, 6)
    population_growth = 1.025
    years = list(range(2026, 2042))
    prod_path = [base_prod * ((1 + tx_croissance/100)**i) for i in range(len(years))]
    besoin_path = [base_prod * d['ratio_besoin'] * (population_growth ** i) for i in range(len(years))]
    dispo_hab = [(p * 0.7 * 1000) / (14000000 * (population_growth**i)) for i, p in enumerate(prod_path)]
    
    st.plotly_chart(px.line(x=years, y=[prod_path, besoin_path], labels={'y':'Tonnes', 'x':'Année'}, title="Équilibre Offre/Demande"), use_container_width=True)
    st.write(f"**🥗 Disponibilité par habitant (kg/an)**")
    fig_nutri = px.area(x=years, y=dispo_hab)
    fig_nutri.add_hline(y=d['seuil_fao'], line_dash="dash", line_color="orange")
    st.plotly_chart(fig_nutri, use_container_width=True)
    
    annee_auto = next((years[i] for i, (p, b) in enumerate(zip(prod_path, besoin_path)) if p >= b), None)
    if annee_auto: st.success(f"✅ Autosuffisance atteinte en **{annee_auto}**.")
    else: st.error(f"🚨 Déficit de **{int(besoin_path[-1] - prod_path[-1]):,} T** en 2041.")

with tab4:
    st.subheader(f"💰 Finance : {culture_select}")
    c_fin1, c_fin2 = st.columns(2)
    with c_fin1:
        s_sem = st.slider("Semences (Mds GNF)", 0, int(budget_total), int(budget_total*0.3))
        s_eng = st.slider("Engrais (Mds GNF)", 0, int(budget_total - s_sem), int(budget_total*0.4))
        s_mac = budget_total - s_sem - s_eng
        gain_tonnes = (s_sem * d['coef_roi']) + (s_eng * d['coef_roi'] * 1.2) + (s_mac * d['coef_roi'] * 0.8)
        st.metric("Gain Production", f"+{int(gain_tonnes):,} T")
    with c_fin2:
        st.plotly_chart(px.pie(values=[s_sem, s_eng, s_mac], names=['Semences', 'Engrais', 'Machines'], 
                         color_discrete_map={'Semences':'#ce1126','Engrais':'#fcd116','Machines':'#009460'}, hole=0.3), use_container_width=True)
    
    eco_usd = gain_tonnes * 550
    st.write("---")
    st.metric("Économie de Devises (USD)", f"${eco_usd:,.0f}")
    st.info(f"Rentabilité : **{(eco_usd * 8600) / (budget_total * 1e9):.2f}x** par GNF investi.")

with tab5:
    st.subheader(f"🏭 Industrialisation : {culture_select}")
    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        taux_perte = st.slider("Pertes post-récolte (%)", 5, 50, 30)
        niveau_transfo = st.radio("Niveau d'industrialisation", ["Manuel (Faible)", "Artisanal (Moyen)", "Industriel (Élevé)"])
        perte_tonnes = base_prod * (taux_perte / 100)
        st.warning(f"Pertes : **{int(perte_tonnes):,} T**")
    with col_t2:
        fig_valeur = go.Figure(go.Waterfall(orientation="v", measure=["relative", "relative", "total"],
            x=["Champ", "Pertes", "Disponible"], y=[base_prod, -perte_tonnes, 0],
            increasing={"marker":{"color":"#009460"}}, decreasing={"marker":{"color":"#ce1126"}}, totals={"marker":{"color":"#fcd116"}}))
        st.plotly_chart(fig_valeur, use_container_width=True)
