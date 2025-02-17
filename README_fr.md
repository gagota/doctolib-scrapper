Le but initial de ce projet va plus loin que seulement récupérer les données de doctolib. En effet, le but final est de pouvoir classer les praticiens dans un tableur, en fonction de certains critères. Celui qui m'intéresse le plus est l'accessibilité du praticien depuis chez moi. Comme je n'ai pas de voiture, certains praticiens sont difficilement accessibles en transports en commun.

Pour éviter la tâche rébarbative d'aller sur la page de chaque praticien, copier l'adresse, aller sur le site de transport en commun puis simuler un trajet depuis chez moi pour obtenir un temps total de trajet et un temps de marche, je me suis décidé à lancer ce projet.

La première étape est celle-ci, c'est à dire récupérer les informations essentielles sur doctolib.

Ensuite, il faut utiliser l'API de Google Maps pour simuler un trajet depuis chez moi vers le praticien, ce qui permet de calculer le temps de trajet.

La dernière étape est de mettre en forme les données récoltées et créées dans un google sheet, en utilisant son API.

La raison pour laquelle je n'ai pas mis ces 2 dernières parties est qu'elles utilisent les API de GCP, ce qui me demanderais d'expliquer comment le faire. Il faudrait aussi que je remanie mon code pour intégrer plus facilement les credentials de quelqu'un d'autre. Au vu de la complexité d'utilisation, je pense que peu de personnes (voir aucune) n'y serait intéressé.

Si jamais vous êtes tout de même intéressé par cette partie supplémentaire, faites le moi savoir sur reddit (lien de mon compte sur mon profil github).
