# Doctolib Scraper

Doctolib Scraper is a python program that scraps doctors informations into a yaml file.

The program is meant to be run locally.


## Motivation

The initial goal of this project goes beyond simply scraping data from Doctolib. The ultimate objective is to classify practitioners in a spreadsheet based on certain criteria. The most important one for me is accessibility from my home. Since I don’t own a car, some practitioners are difficult to reach via public transportation.

To avoid the tedious task of manually checking each practitioner's page, copying their address, going to the public transport website, simulating a route from my home, and retrieving the total travel time and walking time, I decided to create this project.

The first step is to collect essential information from Doctolib.

Next, I need to use the Google Maps API to simulate a route from my home to the practitioner's location, allowing me to calculate the travel time.

The final step is to format and store the gathered and computed data in a Google Sheet using its API.

I haven’t included the last two parts because they rely on GCP APIs, which would require explaining how to set them up. I’d also need to refactor my code to better integrate someone else’s credentials. Given the complexity of using these APIs, I believe very few people (if any) would be interested in this functionality.

However, if you're interested in this additional feature, feel free to reach out to me on Reddit (you’ll find my profile link on my GitHub profile).



Le but initial de ce projet va plus loin que seulement récupérer les données de doctolib. En effet, le but final est de pouvoir classer les praticiens dans un tableur, en fonction de certains critères. Celui qui m'intéresse le plus est l'accessibilité du praticien depuis chez moi. Comme je n'ai pas de voiture, certains praticiens sont difficilement accessibles en transports en commun.

Pour éviter la tâche rébarbative d'aller sur la page de chaque praticien, copier l'adresse, aller sur le site de transport en commun puis simuler un trajet depuis chez moi pour obtenir un temps total de trajet et un temps de marche, je me suis décidé à lancer ce projet.

La première étape est celle-ci, c'est à dire récupérer les informations essentielles sur doctolib.

Ensuite, il faut utiliser l'API de Google Maps pour simuler un trajet depuis chez moi vers le praticien, ce qui permet de calculer le temps de trajet.

La dernière étape est de mettre en forme les données récoltées et créées dans un google sheet, en utilisant son API.

La raison pour laquelle je n'ai pas mis ces 2 dernières parties est qu'elles utilisent les API de GCP, ce qui me demanderais d'expliquer comment le faire. Il faudrait aussi que je remanie mon code pour intégrer plus facilement les credentials de quelqu'un d'autre. Au vu de la complexité d'utilisation, je pense que peu de personnes (voir aucune) n'y serait intéressé.

Si jamais vous êtes tout de même intéressé par cette partie supplémentaire, faites le moi savoir sur reddit (lien de mon compte sur mon profil github).

## Installation

If you don't have python on your computer, install it.

Clone the project

```bash
  git clone https://github.com/gagota/doctolib-scrapper.git
```

Go to the project directory

```bash
  cd doctolib-scrapper
```

Create and activate a virtual environment (Optional, recommended)

```bash
  python -m venv doctolib_env
```
```bash
  . .\doctolib_env\Scripts\activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```    
## Usage 

First, you need to make your search on doctolib.fr.

![Doctolib main page](screenshots/doctolib_main_page.PNG)

Then, when on the search page, copy the url of the page.

![Doctolib search page](screenshots/doctolib_search_page.PNG)

Open '_main.py' (in the 'src' folder) with your prefered IDE (like VS Code).

Paste the url in the `doctolib_search_url` variable.

[Script '_main.py' paste url in `doctolib_search_url`]

Enter a search name in the `search_name` variable. It will be the name of the folder containing the gathered data.

[Change `search_name`]

You can tweak the parameters as you like in the `parameters` object.

Play the script, and watch the magic happen before your eyes ;)
