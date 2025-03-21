# 📌 Cuisine Assistant

Cuisine Assistant est une application développée avec Kivy permettant de gérer des recettes, planifier des menus et générer une liste de courses. Elle offre aussi une fonctionnalité d'exportation des recettes en PDF.

## 🚀 Fonctionnalités

✅ Ajouter, modifier et supprimer des recettes

✅ Lister et filtrer les recettes

✅ Gérer les ingrédients avec quantité et unité

✅ Planifier un menu hebdomadaire

✅ Générer automatiquement une liste de courses

✅ Exporter une recette en PDF

## 🛠️ Installation

🔹 1. Prérequis

Assurez-vous d'avoir Python 3 installé sur votre machine.

Installez les dépendances nécessaires :

```bash
pip install kivy reportlab
```

🔹 2. Exécution du projet

Lancez l'application avec :

```bash
python main.py
```

## 📲 Générer un APK pour Android

1️⃣ Installer Buildozer

Buildozer est nécessaire pour générer un APK. Installez-le avec :

```bash
pip install buildozer
```

2️⃣ Initialiser le fichier de configuration

Dans le dossier du projet, exécutez :

```bash
buildozer init
```

3️⃣ Modifier buildozer.spec

Ajoutez les dépendances nécessaires dans le fichier buildozer.spec :

```bash
requirements = python3,kivy,reportlab
```

4️⃣ Compiler l'APK

Générez l'APK avec la commande :

```bash
buildozer -v android debug
```

L'APK sera disponible dans le dossier bin/.

## 📜 Licence

Ce projet est sous licence MIT. Vous pouvez le modifier et l'utiliser librement.

## 👨‍💻 Auteur

Développé par Antoine.

Si vous avez des questions ou suggestions, n'hésitez pas à me contacter ! 😊