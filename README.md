# amazinggame

Jeu de course dans un labyrinthe, avec une phase d'exploration puis une phase de course.

## Principe du jeu

Chaque joueur pilote un agent dans un labyrinthe.

1. **Exploration** : pendant 3 minutes, les joueurs découvrent le labyrinthe.
2. **Course** : après l'exploration, les joueurs repartent du début et tentent d'atteindre l'arrivée.

Paramètres principaux :

- Durée exploration : `180` secondes
- Durée course : `60` secondes
- Taille du labyrinthe : `15x15`

Le jeu se termine quand :

- un joueur gagne la course, ou
- le temps maximal est atteint.

## Règles de score

Le score depend principalement :

- du nombre de cases visitées pendant l'exploration,
- d'un bonus lié au temps de course,
- d'un bonus de fin pour un joueur qui termine la course.

## Commandes joueur (protocole)

Le client joueur envoie des lignes texte au serveur. Commandes supportées :

- `ACCELERATE` : accélère de 0.1
- `DECELERATE` : décélère de 0.1 (ne descend pas en dessous de 0)
- `TURN_RIGHT` : tourne de 10° à droite
- `TURN_LEFT` : tourne de 10° à gauche
- `GET_SENSORS` : récupère les infos des capteurs (cf ci-après)

Réponses typiques :

- `OK` : commande acceptée
- `KO` : commande invalide
- `BLOCKED` : commande reçue mais le joueur ne peut pas agir en ce moment

### Blocages

| Cause                             | Durée       | Effet                                            |
| --------------------------------- | ----------- | ------------------------------------------------ |
| Trop d'erreurs de commandes (> 3) | Permanent   | Joueur déconnecté par le serveur                 |
| Collision avec un mur             | 10 secondes | Le joueur reprend automatiquement après la pause |

Pendant un blocage temporaire (mur), les commandes reçoivent `BLOCKED` en réponse mais le joueur **n'est pas déconnecté** et reprend normalement à la fin de la pause.

## Format des capteurs (`GET_SENSORS`)

La réponse est une ligne avec:

`time exploration x y orientation speed front right rear left`

avec (les nombres à virgules ont deux décimales) :

- `time` étant la date en secondes depuis le début du jeu (à virgule)
- `exploration` vaut `1` en phase exploration, sinon `0`
- `x`/`y` position du joueur (à virgule)
- `orientation` en degrés, sens trigonométrique
- `speed` vitesse courante en largeur de cellule par seconde (à virgule)
- `front/right/rear/left` distances aux murs (à virgule)

## Installation et pre-requis

- Python `>= 3.14`
- `uv`

Installation locale :

```bash
uv sync
```

## Commandes utiles

### Lancer un serveur de jeu

```bash
uv run python -m amazinggame.game.server
```

Options principales :

- `-a`, `--address` (défaut: `localhost`)
- `-p`, `--port` (défaut: `16210`)
- `-t`, `--timeout` temps d'attente pour laisser entrer d'autres joueurs
- `-f`, `--fast` mode rapide

Exemple:

```bash
uv run python -m amazinggame.game.server -p 16210 -t 10
```

### Lancer le viewer (spectateur graphique)

```bash
uv run python -m amazinggame.viewer -p 16210
```

Options:

- `-a`, `--address`
- `-p`, `--port`
- `-s`, `--small-window`


### Lancer un client d'exemple C

Compilation :

```bash
gcc -Wall -o sample_player_client sample_player_client.c
```

Execution:

```bash
./sample_player_client 127.0.0.1 16210 MonBot
```

### Scenario de competition local

Le script [competition.sh](competition.sh) lance un scenario complet (serveur, viewer, bots de test) :

```bash
bash competition.sh
```

## Qualité et tests

Exécuter la suite de vérification complète :

```bash
prek run --all-files
```
