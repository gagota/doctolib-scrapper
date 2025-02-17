# doctolib-scrapper

This project scraps the website doctolib.fr, a french website meant to book doctors appointments.

You'll find the python file "_main.py". In it, put the link to the doctolib search you want to make, the name you give to your search, then play the script.
It will create a "doctors_information.yaml" file, with the relevant informations of all the doctors of your search.

You can also tweak the parameters as you wish. For example, if you only want to do the `gather_doctors_links` step, or the `find_docs_infos`, you can set it in the `parameters` object.
