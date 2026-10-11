# Portfolio — Jérémy Bruguet

Site statique HTML/CSS/JavaScript, prévu pour être publié avec GitHub Pages.

## Fichiers

- `index.html` : accueil, présentation, compétences, certifications et contact.
- `veille.html` : veille sur les vulnérabilités informatiques, de la découverte à la correction, avec un focus sur les failles zero-day.
- `projets.html` : page des projets, accessible depuis le menu principal en haut de chaque page.
- `mentions-legales.html` : mentions légales (éditeur, hébergeur).
- `CV_jeremy_bruguet.pdf` : CV, lié depuis le menu, l'accueil et le pied de page de chaque page.
- `404.html` : page d'erreur personnalisée avec Flammy.
- `style.css`, `script.js` : styles et comportements partagés.
- `assets/` : images, favicon et icônes SVG locales (inspirées du jeu d’icônes Lucide). Les icônes sont embarquées dans le projet et ne nécessitent pas de chargement depuis un site externe.

## Avant publication

1. Si le dépôt GitHub Pages ne s'appelle pas `portfolio`, changer la variable `PROJECT_REPO` dans `404.html` pour le nom exact du dépôt. Pour un site utilisateur `pseudo.github.io` ou un domaine personnalisé, laisser `PROJECT_REPO` vide.
2. Relire les mentions légales si ta situation change (site professionnel, publicité, vente).

## Publication avec GitHub Pages

1. Créer un dépôt GitHub, par exemple `portfolio`.
2. Décompresser cette archive et envoyer **le contenu du dossier** directement à la racine du dépôt. Il faut que `index.html` et `404.html` soient à la racine du dossier publié, pas cachés dans un sous-dossier.
3. Dans GitHub, ouvrir **Settings → Pages**.
4. Dans **Build and deployment**, choisir **Deploy from a branch**, sélectionner la branche `main` et le dossier `/(root)`, puis enregistrer.
5. Attendre la fin du déploiement. Pour un dépôt `portfolio`, l'adresse ressemble à `https://VOTRE-PSEUDO.github.io/portfolio/`.

### Comment fonctionne la page 404 ?

Il n'y a pas de lien à créer dans GitHub. GitHub Pages repère automatiquement un fichier nommé exactement `404.html` placé à la racine du site publié. Il l'affiche lorsqu'une URL du site n'existe pas. Le visiteur peut ensuite cliquer sur « Retour à l'accueil ».

Le site calcule les liens de la page 404 en utilisant `PROJECT_REPO`. Si le dépôt s'appelle par exemple `mon-portfolio`, remplacez `var PROJECT_REPO = 'portfolio';` par `var PROJECT_REPO = 'mon-portfolio';`. Pour un site publié directement à la racine `https://VOTRE-PSEUDO.github.io/`, laissez la valeur vide : `var PROJECT_REPO = '';`.

Pour tester visuellement la page en local, ouvrez `404.html` directement. Un simple serveur local comme `python -m http.server` ne redirige pas automatiquement les URL inconnues vers ce fichier.

## Mettre à jour la veille

La page de veille présente son état des lieux et une structure de suivi. Les nouvelles analyses doivent être ajoutées manuellement après vérification de sources fiables. Ne pas présenter une faille comme exploitée dans la nature sans source qui l'établit ; distinguer une preuve de concept d'une exploitation confirmée. Les sources de départ sont liées dans `veille.html` : CERT-FR, NVD, CISA KEV, CVE Program, Microsoft MSRC et Zero Day Initiative.


## Icônes locales

Les icônes SVG sont conservées dans `assets/icons/` et utilisées localement : aucune bibliothèque d'icônes n'est chargée depuis un CDN, et plus aucun SVG n'est collé directement dans les pages HTML. Les formes suivent le style Lucide (jeu d'icônes open source distribué sous licence ISC) : https://lucide.dev/

Utilisation dans une page :

```html
<span class="i icon icon-mail" aria-hidden="true"></span>
```

Le nom après `icon-` est celui du fichier (`assets/icons/mail.svg`). Les fichiers sont tous noirs ; `style.css` les affiche en image de fond et les recolore avec un filtre (vert d'accent dans les cartes et les liens, blanc dans les boutons foncés). Cette méthode fonctionne aussi quand on ouvre les pages directement avec un double-clic (`file://`).

Pour ajouter une icône : déposer `nom.svg` (24 × 24, tracé noir) dans `assets/icons/`, puis ajouter dans `style.css` la ligne `.icon-nom{background-image:url(assets/icons/nom.svg)}`.

Si la couleur d'accent `--acc` change, il faut recalculer le filtre `--icon-acc` dans `style.css` (un générateur de filtre CSS à partir d'une couleur hexadécimale suffit).
