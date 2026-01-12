# 🇬🇳 SAD-UPDIA : Système d'Aide à la Décision pour la Souveraineté Alimentaire

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg) 
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg) 
![INRAE](https://img.shields.io/badge/Context-PhD_Research-green.svg)

## 📌 Présentation
Le **SAD-UPDIA** est un outil interactif de simulation et d'aide à la décision conçu pour accompagner la République de Guinée vers l'autosuffisance alimentaire d'ici 2040. Ce projet modélise l'impact des politiques agricoles, des aléas climatiques et de l'innovation technique sur les principales filières nationales (Riz, Maïs, Fonio, Cassave).

## 🚀 Fonctionnalités Clés
L'application est structurée en quatre modules analytiques complémentaires :

1. **📊 Diagnostic Territorial (SNSA)** : 
   - Analyse du *Yield Gap* (écart de rendement entre potentiel et réel).
   - Cartographie de la production par région naturelle.
   - Indicateurs de souveraineté actuelle.

2. **🤖 IA & Résilience Climatique** : 
   - Modélisation de l'interaction **Sol-Climat** (Sols Alluviaux, Latéritiques, Sableux).
   - Simulation de stress hydrique et impact de l'irrigation.
   - Anticipation des crises via l'imagerie satellite (Suivi de l'indice **NDVI**).

3. **🎯 Vision 2040** : 
   - Projection de l'équilibre Offre/Demande face à la croissance démographique (+2.5%/an).
   - Calcul de la **disponibilité alimentaire par habitant** (kg/hab/an) comparé aux seuils de la FAO.
   - Identification de l'année théorique d'autosuffisance.

4. **💰 Finance & ROI** : 
   - Optimisation du budget national (Arbitrage entre Semences, Engrais et Mécanisation).
   - Calcul de la **Substitution aux Importations** (Économie de devises en USD).
   - Analyse du retour sur investissement agronomique.

## 🧬 Logique Scientifique
L'outil repose sur des fonctions de réponse agronomique calibrées pour les environnements tropicaux. Le rendement ($Y$) est modélisé comme une résultante des leviers technologiques pondérés par les contraintes pédoclimatiques :

$$Y = Y_{base} \cdot f(Intrants, Sol) \cdot \Delta(Pluviométrie, Irrigation)$$

La courbe de sensibilité intégrée permet d'identifier les seuils de rupture des systèmes de production face aux variations extrêmes du climat.

## 🛠️ Installation et Utilisation
Pour exécuter l'application localement, suivez ces étapes :

1. **Cloner le dépôt** :
   ```bash
   git clone [https://github.com/votre-utilisateur/sad-updia.git](https://github.com/votre-utilisateur/sad-updia.git)
   cd sad-updia
   
2. **Installer les dependances**

   pip install -r requirements.txt

3. **Lancer l'application**

   streamlit run app.py
