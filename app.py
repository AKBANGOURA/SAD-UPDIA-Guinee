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
filières_db = {
    'Riz': {'prod': 2250000, 'obj_2040': 5000000, 'ratio_besoin': 1.6, 'coef_roi': 850, 'seuil_fao': 100},
    'Maïs': {'prod': 850000, 'obj_2040': 2000000, 'ratio_besoin': 1.4, 'coef_roi': 650, 'seuil_fao': 55},
    'Fonio': {'prod': 550000, 'obj_2040': 1300000, 'ratio_besoin': 1.2, 'coef_roi': 450, 'seuil_fao': 40},
    'Cassave': {'prod': 1200000, 'obj_2040': 3000000, 'ratio_besoin': 1.3, 'coef_roi': 550, 'seuil_fao': 80}
}

# --- 4. BARRE LATÉRALE DE PILOTAGE ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Flag_of_Guinea.svg/1200px-Flag_of_Guinea.svg.png", width=150)
st.sidebar.title("Pilotage Stratégique")

options_culture = ["Tout"] + list(filières_db.keys())
culture_select = st.sidebar.selectbox("Filière Agricole Prioritaire", options_culture, key="filiere_master")
scénario = st.sidebar.selectbox("Scénario d'investissement", ["Stagnation", "PNIASAN (Modéré)", "Vision 2040 (Ambitieux)"])
budget_total = st.sidebar.number_input("Budget Total (Milliards GNF)", min_value=1, value=2500)

st.sidebar.markdown("---")
st.sidebar.info("Auteur : Almamy BANGOURA Economiste statisticien, Expert en Data science")

# --- 5. LOGIQUE DE CALCULS RÉGIONAUX (8 RÉGIONS) ---
regions_guinee = ["Boke", "Kindia", "Mamou", "Faranah", "Kankan", "Labe", "N'Zerekore", "Conakry"]

potentiels = {
    'Riz': {'Boke': 1.2, 'Kindia': 1.1, 'Mamou': 0.7, 'Faranah': 1.3, 'Kankan': 1.2, 'Labe': 0.6, "N'Zerekore": 1.1, "Conakry": 0.1},
    'Maïs': {'Boke': 0.8, 'Kindia': 0.9, 'Mamou': 1.1, 'Faranah': 1.2, 'Kankan': 1.1, 'Labe': 1.0, "N'Zerekore": 1.3, "Conakry": 0.1},
    'Fonio': {'Boke': 0.6, 'Kindia': 0.7, 'Mamou': 1.3, 'Faranah': 1.1, 'Kankan': 0.9, 'Labe': 1.4, "N'Zerekore": 0.7, "Conakry": 0.1},
    'Cassave': {'Boke': 1.2, 'Kindia': 1.2, 'Mamou': 0.8, 'Faranah': 0.9, 'Kankan': 0.8, 'Labe': 0.7, "N'Zerekore": 1.4, "Conakry": 0.1},
    'Tout': {'Boke': 1.0, 'Kindia': 1.0, 'Mamou': 1.0, 'Faranah': 1.0, 'Kankan': 1.0, 'Labe': 1.0, "N'Zerekore": 1.0, "Conakry": 0.5}
}

if culture_select == "Tout":
    base_prod = sum(f['prod'] for f in filières_db.values())
    obj_2040 = sum(f['obj_2040'] for f in filières_db.values())
    d = {
        'prod': base_prod, 'obj_2040': obj_2040,
        'ratio_besoin': np.mean([f['ratio_besoin'] for f in filières_db.values()]),
        'coef_roi': np.mean([f['coef_roi'] for f in filières_db.values()]),
        'seuil_fao': np.mean([f['seuil_fao'] for f in filières_db.values()])
    }
else:
    d = filières_db[culture_select]
    base_prod, obj_2040 = d['prod'], d['obj_2040']

# --- 6. HEADER ---
st.title(f"SAD UPDIA : Pilotage de {'Toutes les filières' if culture_select == 'Tout' else f'la filière {culture_select}'}")

# --- 7. ONGLETS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Diagnostic", "🤖 IA & Rendements", "🎯 Vision 2040", "💰 Finance", "🏭 Transformation"])

with tab1:
    st.subheader(f"📊 Analyse de Production : {culture_select}")
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Production {culture_select}", f"{base_prod:,} T", "+4.2%")
    m2.metric("Objectif National", f"{d['obj_2040']:,} T", "Cible 2040")
    m3.metric("Besoin Importé", f"{int((d['ratio_besoin'] - 1) * 100)}%", "-2.1%")

    st.write("---")
    
    # Rendement & Gap
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    rendement_moyen = base_prod / 800000 
    objectif_rendement = d['obj_2040'] / 800000
    gap_rendement = ((objectif_rendement - rendement_moyen) / rendement_moyen) * 100
    col_kpi1.metric("Rendement Actuel", f"{rendement_moyen:.2f} T/Ha")
    col_kpi2.metric("Yield Gap", f"{gap_rendement:.1f}%", delta=f"{objectif_rendement:.2f} visé", delta_color="inverse")
    col_kpi3.metric("Souveraineté", f"{(1/d['ratio_besoin'])*100:.1f}%")

    # Section C : Graphiques
    c_left, c_right = st.columns(2)
    with c_left:
        st.write("**📍 Répartition Territoriale Administrative**")
        # Pondération régionale dynamique
        filiere_ref = culture_select if culture_select in potentiels else 'Tout'
        df_reg = pd.DataFrame({
            'Région': regions_guinee,
            'Production': [base_prod * (potentiels[filiere_ref][r]/8) for r in regions_guinee]
        })
        fig_prod = px.bar(df_reg, x='Région', y='Production', color='Région', color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_prod, use_container_width=True)

    with c_right:
        st.write("**🎯 Analyse de l'Objectif 2040**")
        df_gap = pd.DataFrame({'Indicateur': ['Production Actuelle', 'Déficit'], 'Valeur': [base_prod, max(0, d['obj_2040'] - base_prod)]})
        fig_gap = px.pie(df_gap, values='Valeur', names='Indicateur', hole=0.4, color_discrete_map={'Production Actuelle': '#009460', 'Déficit': '#ce1126'})
        st.plotly_chart(fig_gap, use_container_width=True)

    # Section D : Carte Choroplèthe
    st.write("---")
    st.subheader("📍 Cartographie de l'Efficacité (Dynamique)")
    facteur_budget = budget_total / 2500
    data_map = [{'Région': r, 'Efficacité (%)': min(100, int(potentiels[filiere_ref][r] * facteur_budget * 75))} for r in regions_guinee]
    df_map_final = pd.DataFrame(data_map)
    
    geojson_url = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/guinea/guinea-regions.json"
    fig_map = px.choropleth(df_map_final, geojson=geojson_url, locations="Région", featureidkey="properties.NAME_1",
                           color="Efficacité (%)", color_continuous_scale="RdYlGn", range_color=(40, 100))
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
    st.plotly_chart(fig_map, use_container_width=True)

    st.info(f"**Synthèse :** La filière **{culture_select}** présente un Yield Gap de **{gap_rendement:.1f}%**. L'efficacité territoriale est corrélée au budget de **{budget_total} Mds GNF**.")

with tab2:
    st.subheader(f"Simulateur Agro-Climatique : {culture_select}")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        type_sol = st.selectbox("Type de Sol", ["Alluvial (Fertile)", "Latéritique (Ferralitique)", "Sableux/Limoneux"])
        intrants = st.select_slider("Intensification", options=["Traditionnel", "Semi-Mécanisé", "Intensif"])
        irrigation = st.checkbox("Irrigation Maîtrisée")
        meteo_actuelle = st.slider("Variation Pluie (%)", -50, 50, 0)
        
        f_sol = {"Alluvial (Fertile)": 1.2, "Latéritique (Ferralitique)": 0.8, "Sableux/Limoneux": 0.9}[type_sol]
        boost_base = {"Traditionnel": 1.0, "Semi-Mécanisé": 1.4, "Intensif": 1.9}[intrants] * f_sol
        
        def calc_rend(v, ir, b, s):
            if ir: b += 0.3
            imp = v/100 * (1.6 if s=="Sableux/Limoneux" else 1.0)
            return max(0.1, b + (imp/3 if ir and v<0 else imp))
        
        rend_final = calc_rend(meteo_actuelle, irrigation, boost_base, type_sol)
        prod_sim = base_prod * rend_final
        st.metric("Production Projetée", f"{int(prod_sim):,} T", f"{int((rend_final-1)*100)}%")

    with col_b:
        fig_comp = px.bar(x=['Actuel', 'IA'], y=[base_prod, prod_sim], color=['Actuel', 'IA'], color_discrete_map={'Actuel':'#fcd116','IA':'#009460'})
        st.plotly_chart(fig_comp, use_container_width=True)
    
    st.write("---")
    st.subheader("📡 Suivi Satellite (NDVI)")
    ndvi_obs = st.slider("Indice NDVI observé", 0.1, 0.9, 0.5)
    fig_sat = px.area(x=["Jan","Fev","Mar","Avr","Mai","Juin"], y=[0.3, 0.35, 0.42, 0.48, 0.52, ndvi_obs], title="Tendance NDVI")
    st.plotly_chart(fig_sat, use_container_width=True)

with tab3:
    st.subheader(f"🎯 Trajectoire Vision 2040 : {culture_select}")
    tx_croissance = st.slider("Croissance annuelle (%)", 1, 15, 6)
    years = list(range(2026, 2042))
    prod_path = [base_prod * ((1 + tx_croissance/100)**i) for i in range(len(years))]
    besoin_path = [base_prod * d['ratio_besoin'] * (1.025 ** i) for i in range(len(years))]
    
    fig_v = px.line(x=years, y=[prod_path, besoin_path], labels={'x':'Année','y':'Tonnes'}, title="Offre vs Demande")
    st.plotly_chart(fig_v, use_container_width=True)
    
    annee_auto = next((years[i] for i, (p, b) in enumerate(zip(prod_path, besoin_path)) if p >= b), None)
    if annee_auto: st.success(f"Autosuffisance en {annee_auto}")
    else: st.error(f"Déficit en 2041 : {int(besoin_path[-1]-prod_path[-1]):,} T")

with tab4:
    st.subheader(f"💰 Finance : {culture_select}")
    c1, c2 = st.columns(2)
    with c1:
        s_sem = st.slider("Semences (Mds)", 0, int(budget_total), int(budget_total*0.3))
        s_eng = st.slider("Engrais (Mds)", 0, int(budget_total-s_sem), int(budget_total*0.4))
        s_mac = budget_total - s_sem - s_eng
        gain_t = (s_sem * d['coef_roi']) + (s_eng * d['coef_roi']*1.2) + (s_mac * d['coef_roi']*0.8)
        st.metric("Gain Production", f"+{int(gain_t):,} T")
    with c2:
        fig_p = px.pie(values=[s_sem, s_eng, s_mac], names=['Semences','Engrais','Machines'], color_discrete_sequence=['#ce1126','#fcd116','#009460'])
        st.plotly_chart(fig_p, use_container_width=True)
    
    eco_dev = gain_t * 550
    st.info(f"Économie de devises : ${eco_dev:,.0f} USD (Substitution aux importations)")

with tab5:
    st.subheader(f"🏭 Transformation : {culture_select}")
    t_perte = st.slider("Pertes post-récolte (%)", 5, 50, 30)
    perte_t = base_prod * (t_perte/100)
    fig_w = go.Figure(go.Waterfall(x=["Champ", "Pertes", "Final"], y=[base_prod, -perte_t, 0], measure=["relative","relative","total"],
                                  increasing={"marker":{"color":"#009460"}}, decreasing={"marker":{"color":"#ce1126"}}))
    st.plotly_chart(fig_w, use_container_width=True)
    st.success(f"Récupération possible par industrialisation : +{int(perte_t*0.3):,} Tonnes.")
