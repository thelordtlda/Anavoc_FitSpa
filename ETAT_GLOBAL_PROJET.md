# Rapport d'Audit Technique Global : Écosystème SpaFit Cover Sizer (`ETAT_GLOBAL_PROJET.md`)

> **Rôle du document** : Audit technique exhaustif, forensique et architectural consolidant l'état réel de l'ensemble du projet SpaFit Cover Sizer (moteur de vision et de traçage de joint, configurateur web, catalogue multi-marques, pipeline d'extraction d'actifs, modélisation de compatibilité et historique d'exécution des sessions).
> **Date de réalisation** : 7 novembre 2026  
> **Autorité d'audit** : Lead Technical Auditor & Software Architect (Antigravity 2.0)  
> **Méthodologie** : Rapprochement forensique du code source, analyse des arbres syntaxiques (AST), vérification d'intégrité binaire sur disque, validation des liaisons DOM/Canvas, assertion empirique des bases de données et rétrospective chronologique des interactions et outils exécutés en session. Aucune ligne de code fonctionnel n'a été modifiée durant cet audit.

---

## 1. Vue Explosée de l'Existant (Architecture & Réalisations)

### Arborescence Générale du Projet

L'espace de travail `d:\SPAFIT\Cover Sizer` est structuré autour de deux applications web front-end à la racine et de quatre sous-projets spécialisés :

```
d:\SPAFIT\Cover Sizer/
├── [APPLICATION WEB & MOTEUR GÉOMÉTRIQUE RACINE]
│   ├── index.html                                   # Configurateur d'étanchéité interactif (Gamme Oasis)
│   ├── app.js                                       # Moteur Canvas 2D (3 320 lignes) : edge detection, fit engine & simulation
│   ├── style.css                                    # Styles CSS personnalisés, animations et badges d'ingénierie
│   └── spa_catalog_viewer.html                      # Visualiseur autonome (2 675 lignes) du catalogue de 1 036 spas
│
├── scrapping python/                                # [SOUS-PROJET 1 : EXTRACTION D'ACTIFS & CRAWLERS]
│   ├── AUDIT_SOUS_PROJET.md                         # Audit technique spécifique du module de scraping
│   ├── requirements.txt                             # Dépendances (Requests, PyMuPDF, OpenCV, Pillow, BS4)
│   ├── scrapers/                                    # Modules de scraping par constructeur (Watkins, Jacuzzi, Master, Bullfrog...)
│   ├── wayback_archive_scraper.py                   # Crawler rétroactif interrogeant l'API CDX de Wayback Machine
│   ├── spa_covers_scraper.py                        # Extracteur de patrons dimensionnels auprès des fabricants de bâches
│   └── _archive_legacy/                             # Quarantaine des anciens générateurs de faux actifs synthétiques
│
├── scripts/                                         # [SOUS-PROJET 2 : INGESTION, COMPILATION & BLUEPRINTS]
│   ├── AUDIT_SOUS_PROJET.md                         # Audit technique spécifique des scripts d'ingénierie
│   ├── generate_catalog_json.py                     # Compilateur CSV + models.json -> spas_catalog_data.json / .js
│   ├── build_spa_catalog_viewer.py                  # Générateur monolithique Python (2 683 lignes) de spa_catalog_viewer.html
│   ├── regenerate_authentic_footprints.py           # Moteur vectoriel ReportLab de plans d'ingénierie PDF (1 008 fichiers)
│   ├── unify_and_correct_all_databases.py           # Script d'unification et de correction des bases multi-sources
│   ├── execute_zero_duplicate_purge.py              # Purgeur forensique des doublons binaires MD5
│   └── apply_wave1_ingestion.py à wave4...          # Modules d'ingestion par vagues géographiques mondiales
│
├── data/                                            # [SOUS-PROJET 3 : BASES DE DONNÉES & MODÉLISATION SPAFIT]
│   ├── AUDIT_SOUS_PROJET.md                         # Audit technique spécifique du catalogue de données
│   ├── spas_master_database.csv                     # [SSOT ACTUEL] Base maître (1 036 spas, 38 colonnes certifiées)
│   ├── models.json                                  # Spécifications d'ingénierie des 29 modèles SpaFit
│   ├── spas_catalog_data.json                       # Payload JSON d'échange pour navigateurs modernes
│   ├── spas_catalog_data.js                         # Injection globale window.SPAFIT_CATALOG_DATA (Zero-CORS)
│   ├── base_de_donnees_spas_unifiee.csv             # Référentiel unifié issu du nettoyage multi-sources (1 072 lignes)
│   ├── spas_source_list_720_modeles.csv             # Référentiel canonique dédupliqué sans finitions superflues (719 modèles)
│   └── parsed_cover_templates.json                  # Patrons géométriques extraits des fabricants de toiles
│
└── assets/                                          # [SOUS-PROJET 4 : RÉFÉRENTIEL PHYSIQUE DES ACTIFS (2,42 Go)]
    ├── AUDIT_SOUS_PROJET.md                         # Audit technique spécifique du stockage des actifs
    └── [90 Dossiers de Marques]                     # 1 081 dossiers modèles (images/, footprint/, cad/, 3d/)
        ├── images/                                  # Photos réelles zénithales et latérales (942 fichiers)
        ├── footprint/                               # Plans d'implantation d'ingénierie PDF (1 008 fichiers)
        ├── cad/                                     # Fichiers sources AutoCAD DWG (59 fichiers)
        └── 3d/                                      # Répertoires réservés pour modèles volumiques (514 vides)
```

---

### Analyse de l'Application Racine (`index.html`, `app.js`, `spa_catalog_viewer.html`)

#### 1. Moteur Interactif de Traçage du Joint : `index.html` & `app.js`
- **Rôle** : Plateforme interactive permettant à l'utilisateur de charger une photo réelle de spa, de détourer automatiquement le rebord acrylique, d'extrapoler les rayons de courbure des 4 coins, de vérifier l'appui du joint néoprène SpaFit et d'animer l'élévation des 4 poteaux motorisés en vue de profil.
- **Architecture de `app.js` (3 320 lignes de code)** :
  - *Gestion d'état centralisée (`state`, L293–L360)* : Mémorise les cotes du spa (`lengthIn`, `widthIn`, `heightIn`, `cornerRadiusIn`, `flatRimWidthIn`), le modèle SpaFit sélectionné, la rotation 90°, l'unité active (`po` ou `mm`), les calques visibles et l'état d'ouverture du toit.
  - *Pipeline de Vision par Ordinateur Canvas (`autoCropAndAnalyzeSpaImage`, L407–L760)* :
    - Échantillonnage de la couleur d'arrière-plan sur les 4 marges intérieures (`marginOffset = 8 px`).
    - Détection de masque binaire (`isSpaPixel`) par distance euclidienne de couleur et saturation.
    - Élimination des artefacts ou étiquettes publicitaires roses (`isPinkPixel`).
    - Mesure périmétrique du rebord plat acrylique (`sampleRim`) via profil de luminance radiale.
    - Détermination trigonométrique des rayons de coins individuels (`applyExtrapolatedRadiusFromImage`).
  - *Moteur d'Audit de la Surface d'Appui (`analyzeSealLandingSurface`, L761–L884)* :
    - Vérification du seuil minimal d'appui du joint : conforme si $\ge 1.0"$, optimal si $\ge 1.25"$. Alerte d'erreur critique si $< 1.0"$.
    - Comparaison des rayons de courbure constatés avec le rayon constructeur SpaFit ($R_{min} = 4.0"$, $R_{rec} = 8.0"$).
  - *Évaluation de Compatibilité (`evaluateFit`, L885–L1010)* :
    - Calcul des marges orthogonales aux 4 colonnes en tenant compte de la largeur des poteaux ($6.0"$) et du débordement de l'opérateur moteur ($24.0"$).
  - *Moteur de Rendu Double Canvas 2D (`renderTopDownScene` L1418–L2060 & `renderElevationScene` L2202–L2476)* :
    - Rendu synchrone à 60 FPS avec grille cartésienne, cotations dynamiques, tracé du joint (bande de 3,5" hachurée en cyan ou rouge selon l'appui), affichage des poteaux et projection de l'opérateur moteur.
    - Vue d'élévation latérale animée simulant l'ascension du toit de $34"$ à $115"$ avec vérification du dégagement au passage.
  - *Module d'Export de Plan Haute Définition (`exportFootprintPlan`, L2477–L2668)* :
    - Génération côté client d'un canevas haute résolution composite ($2 400 \times 1 600$ px) téléchargeable en PNG avec cartouche officiel.

#### 2. Visualiseur Monolithique Multi-Spas : `spa_catalog_viewer.html`
- **Rôle** : Portail autonome de consultation et de recherche instantanée sur l'intégralité du catalogue des 1 036 spas et des 29 couvercles SpaFit.
- **Caractéristiques techniques** :
  - Généré par `scripts/build_spa_catalog_viewer.py` (2 675 lignes HTML/CSS/JS embarqué).
  - Charge `data/spas_catalog_data.js` via balise `<script>`, garantissant un fonctionnement hors-ligne à 100 % sous le protocole `file:///` sans restriction CORS.
  - Moteur de filtrage temps réel multi-critères : recherche textuelle floue, sélection par marque, segment de marché (Premium, Milieu de gamme, Thérapeutique, Nage), filtre par statut de compatibilité SpaFit (`Optimal`, `Compatible`, `Incompatible`).
  - Rendu vectoriel SVG dynamique intégré : dessine l'empreinte exacte du spa avec ses rayons de coins arrondis, superpose les 4 colonnes SpaFit et projette le contour d'étanchéité sans recourir à des images externes.
  - Export CSV immédiat des spas filtrés.

---

### Flux de Données Global (End-to-End Pipeline)

```mermaid
flowchart TD
    subgraph 1. Acquisition & Scraping
        A1["Catalogues Web Constructeurs"] --> S1["scrapers/extract_*.py"]
        A2["Wayback Machine (CDX API)"] --> S2["wayback_archive_scraper.py"]
        A3["Sites Fabricants de Bâches"] --> S3["spa_covers_scraper.py"]
        S1 & S2 & S3 --> RAW["Données Brutes & Photos HD"]
    end

    subgraph 2. Assainissement & Consolidation (scripts/)
        RAW --> P1["execute_zero_duplicate_purge.py (MD5)"]
        P1 --> P2["execute_full_generational_cleanup.py"]
        P2 --> P3["scripts/fix_round_radii.py"]
        P3 --> CSV["data/spas_master_database.csv<br/>(1 036 fiches certifiées, 38 colonnes)"]
    end

    subgraph 3. Modélisation Géométrique & Assets
        CSV --> RL["scripts/regenerate_authentic_footprints.py"]
        RL --> PDF["assets/.../footprint/*_blueprint.pdf<br/>(1 008 Plans Vectoriels ReportLab)"]
        MODELS["data/models.json<br/>(29 Modèles d'Ingénierie SpaFit)"] --> GEN["scripts/generate_catalog_json.py"]
        CSV --> GEN
    end

    subgraph 4. Distribution & Exécution Client
        GEN --> JSDATA["data/spas_catalog_data.js & .json<br/>(60 088 Pré-calculs Matriciels de Compatibilité)"]
        JSDATA --> VIEW["spa_catalog_viewer.html<br/>(Visualiseur Catalogue 1 036 Spas)"]
        MODELS --> APP["app.js / index.html<br/>(Moteur Interactif de Traçage & Simulation Oasis)"]
        VIEW <--> APP
    end
```

---

### Métriques Globales Consolidées de l'Écosystème

| Couche / Sous-Projet | Métrique Audité sur Disque | Valeur Réelle | Observation Technique / Écarts Détectés |
| :--- | :--- | :--- | :--- |
| **Catalogue Maître (`spas_master_database.csv`)** | Total des spas indexés | **1 036** | 100 % statut `VERIFIED_COMPLETE`, 38 colonnes d'ingénierie |
| **Catalogue Historique (`base_de_donnees_spas_unifiee.csv`)** | Lignes après unification | **1 072** | Écart de **36 à 42 modèles** non synchronisés dans le CSV maître |
| **Référentiel Canonique (`spas_source_list_720_modeles.csv`)** | Modèles physiques uniques | **719** | 353 doublons d'options d'équipements éliminés |
| **Marques Constructeurs Répertoriées** | Marques couvertes | **90** | Couverture Amérique du Nord, Europe, Australasie |
| **Groupes Industriels Consolidés** | Groupes fabricants | **58** | Watkins Wells, Jacuzzi Group, Master Spas, Artesian, etc. |
| **Photos Réelles Vue de Dessus (Top-View)** | Fiches avec photo liée | **413** (39,86 %) | Vraies photographies constructeur (`image_top_file != 'N/A'`) |
| **Plans Vectoriels d'Ingénierie (Blueprints)** | Fiches avec plan PDF lié | **1 036** (100 %) | 1 008 fichiers PDF ReportLab physiques existants sur disque |
| **Plans CAO Sources (AutoCAD DWG)** | Fiches avec DWG lié | **62** (5,98 %) | 59 fichiers `.dwg` réels sur disque (47 fichiers uniques) |
| **Fichiers CAO DXF & Modèles 3D (STEP / STL)** | Fichiers DXF ou modèles 3D | **0** (0,00 %) | 514 répertoires `3d/` créés mais totalement vides (0 Ko) |
| **Volume Physique de `assets/`** | Poids total sur disque | **2,42 Go** (2 475 Mo) | 2 010 fichiers physiques au total |
| **Actifs Orphelins sur Disque** | Fichiers non indexés dans CSV | **158** fichiers | 180,60 Mo (57 JPG, 52 PNG, 34 PDF, 12 DWG) dans 109 dossiers |
| **Modèles SpaFit Répertoriés (`models.json`)** | Total des variantes d'ingénierie | **29** | Oasis (4), Evolution (4), Legend (11), Endless (6), Legend 89 (4) |
| **Modèles SpaFit Actifs dans l'Interface** | Modèles avec `active_in_ui: true` | **4** (13,79 %) | **86 % de la gamme verrouillée** (Oasis uniquement déverrouillé) |
| **Taux de Compatibilité Global SpaFit** | Spas compatibles $\ge 1$ modèle | **636 / 1 036** (61,39 %) | 400 spas incompatibles (spas compacts $< 70"$ ou spas géants) |
| **Taux de Recommandation Optimale** | Modèles optimaux (marge $\ge 1.25"$) | **430 / 1 036** (41,51 %) | Installation sécurisée sans risque de contact mécanique |

---

## 2. Historique des Défis, Essais-Erreurs & Solutions (Code + Conversation)

L'introspection chronologique des 479 étapes du journal de conversation (`transcript.jsonl`) met en lumière les tournants architecturaux majeurs, les impasses techniques rencontrées par l'agent et les correctifs adoptés :

### Chronologie des Problèmes et Échecs Initiaux :

1. **La Crise des Faux Actifs Synthétiques Pillow (`asset_generator.py`)** :
   - *Contexte* : Afin de combler le déficit photographique des spas anciens (2005–2014), un script initial a synthétisé plus de 14 300 faux fichiers `footprint.png` et `top_view.png` sous Pillow.
   - *Conséquence désastreuse* : Ces faux schémas simulaient une fausse couverture d'actifs et faisaient échouer les algorithmes d'analyse d'image dans `app.js` qui traitaient des rectangles bleu marine génériques.
   - *Décision d'architecture* : Mise en quarantaine immédiate de `asset_generator.py` dans `scrapping python/_archive_legacy/`, purge physique totale des 14 300 fichiers et remplacement exclusif par des plans d'ingénierie vectoriels ReportLab (`_blueprint.pdf`) basés sur des cotes certifiées.
2. **Corruptions de Délimiteurs CSV par Points-Virgules Internes (Étapes 0 à 214)** :
   - *Contexte* : Les fichiers fournis par l'utilisateur (`spas_dimensions_reforme.csv` et fichiers markdown) contenaient des points-virgules littéraux non protégés à l'intérieur des noms d'entreprises et de transactions (ex. `ThermoSpas (Watkins/Masco; 2012)` ou `Tiger River Spas (Watkins; 2011)`).
   - *Impact constaté* : Comme le délimiteur du CSV était également le point-virgule, le parseur décalait les colonnes de 1 à 3 crans vers la droite, injectant des chaînes de texte dans les colonnes métriques de largeur et hauteur.
   - *Solution implémentée* : Dans `unify_and_correct_all_databases.py`, développement d'un pré-processeur textuel remplaçant systématiquement les points-virgules parasites par des tirets avant le fractionnement en colonnes.
3. **Le Crash d'Unification `IndexError: list index out of range` (Étape 214)** :
   - *Contexte* : Lors de l'incorporation de la marque australienne Vortex Spas dans le script d'unification `unify_and_correct_all_databases.py`, le script a planté en plein traitement avec une exception `IndexError`.
   - *Cause racine* : Les tuples de la liste `vortex_models` ne comptaient que 12 éléments au lieu de 13 car la colonne `Modele` avait été accidentellement omise.
   - *Correction* : L'agent a inspecté l'arbre syntaxique abstrait (AST) Python pour mesurer la longueur de chaque sous-liste, puis a corrigé le tableau via `edit_file` pour restaurer la 13ᵉ colonne.
4. **Crash d'Évaluation de Compatibilité `TypeError: cannot use 'list' as a dict key` (Étape 383)** :
   - *Contexte* : L'exécution du script d'extraction de métriques `extract_compat_metrics.py` a échoué avec l'erreur `TypeError: cannot use 'list' as a dict key` sur `optimal_counts[optimal] += 1`.
   - *Cause* : L'agent a présumé que le champ `spafit_optimal` dans `data/spas_catalog_data.json` était une chaîne de caractères scalaire, alors qu'il s'agit d'un tableau JSON (`['oasis-std-8x8', ...]`).
   - *Correction* : Réécriture de l'itérateur pour parcourir individuellement chaque élément de la liste.
5. **Erreurs de Syntaxe Shell PowerShell et Timeouts Récursifs (Étapes 109, 218, 296, 314, 439)** :
   - *Contexte* : Sous l'environnement Windows PowerShell, l'exécution de snippets Python complexes en ligne de commande (`python -c "..."`) avec des regex imbriquées contenant des guillemets et apostrophes a généré des erreurs `ParserError` et `SyntaxError: '(' was never closed`.
   - *Parallèlement* : Les commandes de recherche récursive `Get-ChildItem -Recurse` ou `os.walk('.')` sans exclusion stricte de `assets/` (2,42 Go) et `scrapping python/.venv` ont bloqué le shell et dépassé les délais d'attente de 5 secondes, nécessitant des annulations manuelles par `manage_task(Action='kill')`.
   - *Solution définitive* : Écriture systématique de scripts `.py` autonomes dans `scripts/` (ex. `scripts/audit_workspace_forensic.py`, `scripts/extract_compat_metrics.py`) avec exclusion formelle des répertoires lourds.
6. **Résolution du Conflit des Modèles Commerciaux vs Physiques (719 vs 1 072 Lignes, Étapes 234-253)** :
   - *Contexte* : L'utilisateur a soumis `rapport_d_audit_comparatif_list_from_o_vs_base_unifiee.md` signalant un écart entre les 1 072 lignes et les 719 modèles physiques réels.
   - *Analyse d'ingénierie* : 353 lignes correspondaient à des doublons d'équipements (finitions jets/pompes pour une même cuve acrylique chez Cal Spas, ou rebadgage OEM de Coast Spas).
   - *Solution implémentée* : Création de `data/spas_source_list_720_modeles.csv` (719 configurations canoniques) pour l'ingénierie des moules, tout en maintenant l'index étendu de 1 036 fiches pour permettre la recherche commerciale des concessionnaires.

---

## 3. Goulots d'Étranglement Actuels (Code, Données & Exécution Agent)

### Goulots Techniques & Données :
1. **Scission et Déconnexion des Deux Applications Web Racines** :
   - L'espace de travail héberge deux outils web majeurs qui s'ignorent mutuellement :
     - `index.html` + `app.js` : Outil de pointe pour le traçage du joint, la mesure de lèvre acrylique et l'animation 2D, mais **verrouillé à la gamme Oasis** et à la saisie manuelle.
     - `spa_catalog_viewer.html` : Répertoire de 1 036 spas et 29 modèles SpaFit avec recherche en temps réel, mais **dépourvu de l'analyseur de joint interactif** de `app.js`.
   - Un utilisateur sélectionnant un spa dans le catalogue ne peut pas transférer automatiquement ses cotes vers l'analyseur de joint.
2. **Verrouillage Massif de la Gamme SpaFit (`active_in_ui: false`)** :
   - 25 modèles de couvercles sur 29 sont désactivés dans `data/models.json` et filtrés dans `app.js` (L2877). Les gammes Evolution (spas de 8' à 11') et Legend (spas de nage jusqu'à 24') sont inaccessibles dans le configurateur.
3. **Absence Totale de la Gamme SpaFit Horizon** :
   - Le modèle SpaFit Horizon (toit incliné contemporain avec ouverture vers l'arrière) est totalement absent des spécifications d'ingénierie.
4. **Rupture de la Chaîne CAO DWG $\rightarrow$ Web (DXF/SVG)** :
   - Les 59 fichiers DWG stockés dans `assets/` sont au format propriétaire binaire AutoCAD. Ni le navigateur, ni `app.js`, ni ReportLab ne peuvent les lire nativement. En l'absence de conversion automatique en SVG vectoriel, ces fichiers restent inexploités dans l'interface.
5. **Angle Mort Architectural : Absence de Données Z-Axis (Obstacles 3D)** :
   - Le système modélise les spas comme des surfaces d'appui 2D plates. Sur le terrain, de nombreux spas haut de gamme intègrent des obstacles verticaux (haut-parleurs rétractables dépassant de 2", manettes de vannes surélevées, claviers saillants, cascades sculptées) qui entrent en collision mécanique avec le joint d'étanchéité ou le cadre inférieur du couvercle.
6. **158 Actifs Orphelins (180,6 Mo) Non Reliés au Catalogue** :
   - 57 vraies photos haute définition et 12 fichiers DWG d'origine dorment dans 109 dossiers non indexés par `spas_master_database.csv` suite aux scissions de millésimes.

### Goulots de Workflow Observés lors des Actions :
1. **Architecture Web Monolithique par Chaîne Python Géante** :
   - `build_spa_catalog_viewer.py` encapsule 2 683 lignes de code front-end (HTML, CSS, JS) dans des chaînes Python brutes. Toute modification de l'interface impose d'éditer ce script Python et de le ré-exécuter, interdisant le découpage modulaire en composants web et l'usage de linters.
2. **Processus de Re-Compilation Manuelle Post-Édition CSV** :
   - La chaîne CSV $\rightarrow$ JSON $\rightarrow$ HTML n'est pas automatisée par un observateur de fichiers (file watcher). Une modification dans le CSV maître n'est répercutée dans le visualiseur que si le développeur se rappelle d'exécuter `generate_catalog_json.py` puis `build_spa_catalog_viewer.py`.

---

## 4. Registre des Bogues Actifs (Par Dossier et Fichier)

Ce tableau synthétise exhaustivement les anomalies, régressions et dysfonctionnements identifiés lors de l'audit de code :

| Sous-Projet / Fichier | Lignes | Sévérité | Description Exacte de l'Anomalie | Cause Racine, Impact & État de Correction |
| :--- | :--- | :--- | :--- | :--- |
| **Racine : `app.js`** | L414–418 | **Critique** | Crash silencieux ou exception de sécurité `DOMSecurityError (Tainted Canvas)` lors de l'appel à `ctx.getImageData()`. | L'image chargée n'est pas enveloppée dans un bloc `try/catch` avec gestion de repli en cas d'URL externe sans en-tête CORS permissif ou d'image locale restreinte par le navigateur. Non corrigé. |
| **Racine : `app.js`** | L2877–2884 | **Majeur** | Verrouillage exclusif sur la gamme Oasis : `state.oasisModels = state.allModels.filter(m => m.active_in_ui && m.gamme == "Oasis")`. | Les gammes Evolution, Legend et Endless Pools sont exclues de la simulation interactive même si `models.json` contient leurs données complètes. Non corrigé. |
| **Racine : `index.html`** | L67–73 | **Mineur** | Libellé trompeur dans le bouton de navigation : affiche `Catalogue 1,072 Spas`. | Le fichier de données réellement chargé par le visualiseur (`spas_catalog_data.js`) n'indexe actuellement que 1 036 spas. Non corrigé. |
| **`scripts/generate_catalog_json.py`** | L48–53 | **Majeur** | Valeurs de repli codées en dur (`s_r_min=4.0`, `s_r_max=16.0`, `h_min=34.0`, `h_max=48.0`). | Pour les spas de nage très hauts (50" à 54") testés contre un SpaFit Legend acceptant jusqu'à 55", la valeur de repli 48" génère un faux négatif d'incompatibilité de hauteur. Non corrigé. |
| **`scripts/generate_catalog_json.py`** | L56–59 | **Majeur** | Inversion implicite des dimensions ($L \times W$ vs $W \times L$) sans respect du champ `orientation_entree`. | L'algorithme teste arbitrairement les deux orientations même pour les modèles SpaFit asymétriques imposant l'accès exclusif sur le petit côté (`short_side`). Non corrigé. |
| **`scripts/build_spa_catalog_viewer.py`** | L2650–2665 | **Moyen** | Export CSV client corrompu si les champs contiennent des points-virgules ou retours à la ligne. | Les valeurs de texte (`audit_notes`, `Serie_Collection`) ne sont pas encapsulées conformément à la norme RFC 4180. Non corrigé. |
| **`scripts/regenerate_authentic_footprints.py`** | L44–50 | **Moyen** | Attribution silencieuse d'un rayon de coin de repli de `8.0"` si la valeur est manquante ou non numérique. | Dessine faussement des coins arrondis de 8 pouces sur des spas à arêtes vives carrées ($R=0"$) ou triangulaires. Non corrigé. |
| **`data/models.json`** | L72, 90, 108... | **Majeur** | Clé `"active_in_ui": false` sur 25 modèles SpaFit (Evolution, Legend, Endless Pools, Legend 89). | Filtre d'exclusion empêchant le configurateur d'afficher les modèles de couvercles pour spas de grande taille. Non corrigé. |
| **`data/models.json`** | *Global* | **Moyen** | Absence complète de la gamme SpaFit Horizon. | Omission de conception dans le schéma d'ingénierie initial ; aucun objet géométrique n'est défini pour cette gamme. Non corrigé. |
| **`data/spas_master_database.csv`** | Colonne 23 | **Moyen** | La colonne `cad_dxf_file` contient `"N/A"` sur les 1 036 fiches (0 % de couverture). | La chaîne de conversion DWG $\rightarrow$ DXF n'a jamais été exécutée ni indexée dans la base principale. Non corrigé. |
| **`assets/` (Doublon Marque)** | *Arborescence* | **Moyen** | Coexistence de deux répertoires de marque distincts sur le disque : `assets/Catalina` et `assets/Catalina Spas`. | Problème de casse et de nommage dans les scrapers initiaux, créant des modèles dupliqués et des chemins orphelins. Non corrigé. |
| **`assets/` (Fichiers Orphelins)** | 109 dossiers | **Moyen** | 158 fichiers d'ingénierie (180,6 Mo), dont 57 photos HD et 12 DWG, sont présents sur disque sans lien dans le CSV. | Déconnexion causée par les opérations de scission des fiches parapluies et de renommage des dossiers de millésimes. Non corrigé. |
| **`assets/` (Caractères Spéciaux)** | Noms fichiers | **Mineur** | Présence de caractères `+` non échappés (ex: `AquaGym Max Pro+_overhead.png`). | Risque d'erreur HTTP 404 lors du chargement dans les navigateurs web sans encodage d'URI approprié. Non corrigé. |
| **`scrapping python/` (AWP Scraper)** | L65–80 | **Mineur** | Le crawler American Whirlpool génère un fichier de métadonnées vide de 2 octets (`awp_discovered_manuals.json`). | Problème de sérialisation JSON en fin de script lorsque le sélecteur CSS du portail ne retourne aucun conteneur. Non corrigé. |

---

## 5. Ce Qu'il Reste à Faire (Backlog Technique Priorisé)

Ce backlog est structuré autour des 4 grands objectifs techniques requis pour atteindre la pleine maturité industrielle du système :

### Objectif 1 : Acquisition 100 % Fiable des Vues de Dessus et CAD 2D par Génération
1. [ ] **Sauvetage et Ré-indexation des 158 Actifs Orphelins (P1)** :
   - Écrire et exécuter `scripts/reconcile_orphan_assets.py` pour rattacher les 57 photos haute définition et les 12 DWG existants aux fiches correspondantes de `spas_master_database.csv`.
2. [ ] **Pipeline Headless DWG $\rightarrow$ DXF $\rightarrow$ SVG (P2)** :
   - Mettre en place un utilitaire basé sur `ezdxf` / `libredwg` pour convertir les 59 fichiers DWG en tracés vectoriels SVG légers affichables directement dans le Canvas de `app.js`.
3. [ ] **Campagne Ciblée pour les 623 Vues de Dessus Manquantes (P3)** :
   - Déployer des scrapers ciblés sur les catalogues de distributeurs de pièces détachées (Waterway, Balboa Water Group) disposant de photographies zénithales non protégées.

### Objectif 2 : Tracé Mathématique et Géométrique Optimal du Joint d'Étanchéité SpaFit
4. [ ] **Sécurisation du Traitement d'Images Canvas dans `app.js` (P1 - Critique)** :
   - Envelopper l'appel à `ctx.getImageData()` dans un bloc `try/catch` avec message utilisateur clair et repli gracieux sur les cotes théoriques en cas de blocage CORS.
5. [ ] **Moteur de Distance Point-à-Courbe pour Spas Ronds et Triangulaires (P2)** :
   - Remplacer le test de boîte englobante simplifié dans `generate_catalog_json.py` par un calcul de distance point-à-courbe prenant en compte le profil circulaire ($R = L/2$) et la position exacte des 4 poteaux SpaFit.
6. [ ] **Interconnexion Directe entre le Catalogue et l'Outil de Traçage (P1)** :
   - Ajouter un bouton d'action directe *"Ouvrir dans l'Analyseur de Joint"* sur chaque fiche de `spa_catalog_viewer.html` transférant les paramètres géométriques ($L, W, H, R$, photo) vers `index.html` via paramètres d'URL ou `localStorage`.

### Objectif 3 : Détection et Annotation des Zones Problématiques sur le Spa (Obstacles Z-Axis)
7. [ ] **Enrichissement du Schéma CSV pour les Obstacles Verticaux (P2)** :
   - Ajouter 4 colonnes d'ingénierie dans `spas_master_database.csv` : `has_raised_speakers`, `has_raised_waterfalls`, `has_protruding_controls`, `has_raised_pillows`.
8. [ ] **Détection Automatique d'Obstacles dans `app.js` (P3)** :
   - Implémenter un module de détection de reliefs acryliques dans `autoCropAndAnalyzeSpaImage` qui identifie les zones de contraste élevé empiétant sur la zone de dépose du joint (bande de 3,5" sur le pourtour) et affiche un marqueur de risque orange sur le Canvas.

### Objectif 4 : Moteur de Validation de Compatibilité Produit SpaFit
9. [ ] **Déverrouillage des 25 Modèles SpaFit dans `models.json` et `app.js` (P1)** :
   - Passer `"active_in_ui": true` sur les gammes Evolution et Legend.
   - Supprimer le filtre restrictif `m.gamme == "Oasis"` dans `app.js` (L2877) pour permettre le choix de toutes les gammes SpaFit.
10. [ ] **Modélisation Complète de la Gamme SpaFit Horizon (P2)** :
    - Rédiger les spécifications d'ingénierie complètes de l'Horizon dans `data/models.json` (cotes des colonnes, articulation arrière, joint d'étanchéité biseauté).
11. [ ] **Synchronisation du Catalogue vers les 1 072 Modèles Unifiés (P2)** :
    - Intégrer les 36 à 42 modèles récents de `base_de_donnees_spas_unifiee.csv` (spas de nage USSPA, Vortex) dans `data/spas_master_database.csv`, puis recompiler le catalogue web.

---

## 6. Dépendances Inter-Projets & Points de Friction

### Matrice des Contrats d'Échange de Données

```
+--------------------------+------------------------------+--------------------------+---------------------------------+
| Producteur (Source)      | Fichier Pivot / Format       | Consommateur (Cible)     | Rôle & Contrat d'Interface      |
+--------------------------+------------------------------+--------------------------+---------------------------------+
| scrapping python/        | Images HD, DWG, PDF bruts    | assets/                  | Stockage physique hiérarchisé   |
| scripts/ingestion/       | spas_master_database.csv     | scripts/compilation/     | SSOT : 38 colonnes, sep ';'     |
| data/models.json         | models.json (JSON Schema)    | scripts/ & app.js        | Spécifications d'ingénierie     |
| scripts/generate_catalog | spas_catalog_data.js / .json | spa_catalog_viewer.html  | Matrice pré-calculée Zero-CORS  |
| scripts/regenerate_pdf   | *_blueprint.pdf (PDF Letter) | assets/.../footprint/    | Plans d'ingénierie imprimables  |
| spa_catalog_viewer.html  | Paramètres d'URL / State     | index.html + app.js      | Handoff de traçage de joint     |
+--------------------------+------------------------------+--------------------------+---------------------------------+
```

### Directives d'Harmonisation & Points de Friction Identifiés :

1. **Séparateur CSV et Encodage** :
   - Le point-virgule (`;`) et l'encodage `UTF-8` sans BOM doivent être strictement préservés. Tout point-virgule littéral présent dans les zones de texte doit impérativement être nettoyé en amont pour éviter les corruptions de colonnes constatées lors de l'Étape 214.
2. **Nomenclature Relative des Chemins d'Actifs** :
   - Tous les chemins de médias doivent être stockés sous la forme normalisée `./assets/Marque/Modele/sous-dossier/fichier.ext` avec des barres obliques Unix (`/`). Cela garantit l'interopérabilité sans faille entre Windows, macOS et les déploiements Linux.
3. **Normalisation des Noms de Répertoires** :
   - Les dossiers de marques doivent être fusionnés (`assets/Catalina` vers `assets/Catalina Spas`).
   - Les caractères spéciaux (`+`, `&`, doubles espaces) doivent être bannis des répertoires d'actifs afin de supprimer tout risque d'erreur HTTP 404 lors du chargement web.

---
*Fin du document d'audit master ETAT_GLOBAL_PROJET.md*
