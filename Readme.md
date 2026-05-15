# STA — Système de Traçabilité d'Activité

> Application web Django permettant aux équipes de développement de centraliser, sécuriser et tracer leurs activités quotidiennes.

---

## Présentation du projet

STA remplace les fichiers Excel partagés, les messages WhatsApp perdus et les mails interminables par une plateforme centralisée où chaque développeur gère ses propres logs d'activité de manière sécurisée et structurée.

---

## Fonctionnalités

- **Authentification** — Inscription, connexion et déconnexion sécurisées
- **Gestion des logs** — Créer, consulter, modifier et supprimer ses entrées
- **Isolation des données** — Chaque utilisateur accède uniquement à ses propres logs
- **Upload d'images** — Joindre une capture d'écran comme preuve à chaque log
- **Signals Django** — Log automatique dans le terminal à chaque création d'entrée
- **Pagination** — Navigation fluide sans surcharge d'affichage
- **Catégories** — Classer les logs par thématique (Bug, Sprint, Veille...)

---

## Stack technique

| Technologie | Usage |
|---|---|
| Python 3.11 | Langage principal |
| Django 6.x| Framework web |
| MySQL | Base de données |
| Bootstrap 5 | Interface utilisateur |
| Pillow | Gestion des images |
| mysqlclient | Connecteur MySQL |

---

## 📁 Structure du projet

```
sta_project/
├── Config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sta/
│   ├── migrations/
│   ├── templates/
│   │    |
│   │    ├── accueil.html
│   │    ├── entry-list.html
│   │    ├── entry_detail.html
│   │    ├── entry_form.html
│   │    └── entry_confirm_delete.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
|   ├── templates/
│   │   ├── base.html
│   │   ├── registration/
│   │   │   ├── login.html
│   │   │   └── register.html
├── media/
├── .env
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## Installation

### 1. Cloner le repository

```bash
git clone https://github.com/anf692/STA
cd STA
```

### 2. Créer et activer l'environnement virtuel

```bash
# Créer
python -m venv env

# Activer (Mac/Linux)
source env/bin/activate

# Activer (Windows)
env\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Créer la base de données MySQL

```sql
CREATE DATABASE sta_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurer les variables d'environnement

Crée un fichier `.env` à la racine :

```env
SECRET_KEY=ta_secret_key_django
DB_NAME=sta_db
DB_USER=root
DB_PASSWORD=ton_mot_de_passe
DB_HOST=localhost
DB_PORT=3306
```

### 6. Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 8. Lancer le serveur

```bash
python manage.py runserver
```

L'application est accessible sur **http://127.0.0.1:8000**

---

## Sécurité

| Règle | Implémentation |
|---|---|
| Accès réservé aux connectés | `LoginRequiredMixin` sur toutes les vues privées |
| Modification réservée à l'auteur | `UserPassesTestMixin` + `test_func()` |
| Protection CSRF | `{% csrf_token %}` sur tous les formulaires |
| Isolation des données | `get_queryset()` filtré par `request.user` |

---

## Signals Django

À chaque création de log, le terminal affiche automatiquement :

```bash
==================================================
Nouveau log créé !
Auteur    : john_dev
Titre     : Bug API pagination
Catégorie : Bug
Date      : 2025-06-12 09:14:32
==================================================
```

---

## Captures d'écran

| Page | Description |
|---|---|
| `/` | Page d'accueil publique avec les 3 derniers logs |
| `/login/` | Connexion utilisateur |
| `/register/` | Création de compte |
| `/dashboard/` | Liste paginée des logs de l'utilisateur connecté |
| `/entry/create/` | Formulaire de création d'un log |
| `/entry/<id>/` | Détail d'un log avec image de preuve |
| `/entry/<id>/update/` | Modification d'un log (auteur uniquement) |
| `/entry/<id>/delete/` | Suppression avec confirmation (auteur uniquement) |

---

## Requirements

```txt
Django>=6.0.5
mysqlclient>=2.2.8
Pillow>=12.2.0
python-decouple>=3.8
```

Générer le fichier :

```bash
pip freeze > requirements.txt
```

---

## Auteur

Développé dans le cadre d'un projet pédagogique — Formation Développeur Web & Mobile.

---