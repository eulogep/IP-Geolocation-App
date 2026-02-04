# 🚀 IP Geolocation & Threat Intelligence Dashboard

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Modern-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![NiceGUI](https://img.shields.io/badge/NiceGUI-UI_Framework-5844a4?style=for-the-badge)](https://nicegui.io)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

**Un projet Full-Stack Python démontrant la maîtrise des architectures modernes, des APIs et de l'expérience utilisateur.**

---

## 🎯 Objectif du Projet

Développer une application professionnelle de **cybersécurité** et de **géolocalisation** permettant l'analyse en temps réel d'adresses IP. Ce projet illustre ma capacité à concevoir des solutions complètes, du backend robuste au frontend interactif.

## 🛠️ Stack Technique & Compétences Démontrées

### Backend (Architecture & API)

* **Technologies** : Python 3.14, **FastAPI**, Uvicorn.
* **Compétences** :
  * Architecture **Client/Serveur** découplée (API Gateway Pattern).
  * Consommation d'APIs externes (CIRCL.lu) avec gestion d'erreurs avancée.
  * Validation de données stricte avec **Pydantic**.
  * Programmation asynchrone (`async/await`).

### Frontend (UI/UX & Data Viz)

* **Technologies** : **NiceGUI**, Leaflet.js, CSS3 (Glassmorphism).
* **Compétences** :
  * Design d'interface moderne (Thème sombre, Responsive).
  * Intégration de **cartographie interactive** (OpenStreetMap).
  * Expérience utilisateur fluide (Loading states, Notifications, Animations).
  * Injection de JavaScript pour des fonctionnalités dynamiques.

### DevOps & Qualité

* **Outils** : **Docker**, Docker Compose, **Poetry**, Git.
* **Compétences** :
  * Conteneurisation d'applications multi-services.
  * Gestion de dépendances professionnelle.
  * **Tests unitaires** et d'intégration (`pytest`, `httpx`).
  * Documentation technique claire et maintenable.

## ✨ Fonctionnalités Clés

1. **Géolocalisation Précise** : Affichage instantané sur carte interactive.
2. **Enrichissement de Données** :
    * 🚩 Drapeaux et codes pays.
    * 🏢 Identification du FAI (ISP) et numéro de Système Autonome (ASN).
    * 🕒 Fuseaux horaires locaux.
3. **Expérience Optimisée** :
    * Détection automatique de l'IP publique.
    * Historique de session.
    * Validation intelligente des entrées.

## 🚀 Architecture du Projet

```mermaid
graph LR
    User[Utilisateur] -->|HTTPS| Frontend[Client NiceGUI (Port 8080)]
    Frontend -->|API REST| Backend[Serveur FastAPI (Port 8000)]
    Backend -->|Request| ExternalAPI[CIRCL Public API]
    Backend -->|JSON| Frontend
```

## 📸 Aperçu

> ![Interface Finale](assets/interfarce%203.png)

## 🚀 Fonctionnalités Clés

1. **Dashboard Premium Cyber-Security** 🎨 :
    * Interface sombre "Glassmorphism" avec animations fluides.
    * Visualisation claire des données (IP, FAI, ASN, Drapeau).
    * **Carte Interactive** : Intégration native de Leaflet.js (OpenStreetMap) avec zoom automatique.

2. **Géolocalisation Avancée** 🌍 :
    * Données précises via l'API CIRCL.lu.
    * **Mon IP** : Détection automatique de votre IP publique en un clic.
    * Support des noms d'hôtes personnalisés (API locale ou distante).

3. **Architecture Robuste** 🏗️ :

---

## 👨‍💻 Pourquoi ce projet est pertinent pour votre entreprise ?

Ce projet dépasse le simple exercice scolaire en intégrant des **contraintes du monde réel** :

* **Robustesse** : Gestion des pannes réseaux et des erreurs d'API tierces.
* **Sécurité** : Isolation du frontend et du backend, pas d'exposition directe des APIs critiques.
* **Maintenabilité** : Code modulaire, typé et testé.
* **Modernité** : Utilisation des derniers standards Python et Web.

C'est une démonstration concrète de mon autonomie technique et de ma capacité à délivrer de la valeur rapidement.

---

## 👨‍💻 Contact & Réseaux

Ce projet a été réalisé par **Euloge Junior Mabiala**.

* 💼 **LinkedIn** : [Profil LinkedIn](https://www.linkedin.com/in/euloge-junior-mabiala-6931b71b8/)
* 📧 **Email** : [mabiala@et.esiea.fr](mailto:mabiala@et.esiea.fr)
* 🐙 **GitHub** : [eulogep](https://github.com/eulogep) | [Repo du Projet](https://github.com/eulogep/IP-Geolocation-App)

---

### 📥 Installation Rapide (Docker)

```bash
git clone [URL_DU_REPO]
cd ip-geolocation-app
docker compose up --build
```

L'application sera accessible sur `http://localhost:8080`.
