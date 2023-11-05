from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from urllib.parse import unquote, urljoin
from django.core.paginator import Paginator


def affiche(request):
    smartphones = []
    base_url = 'https://www.jumia.com.tn/smartphones/'
    for p in range(1,15):
                                                 # Récupérer le numéro de page à partir de la requête
     page_number = request.GET.get('page', 1)
                             # l'URL de la page à partir de l'URL de base et du numéro de page
    url = f'{base_url}?page={p}'
    
    response = requests.get(url)
                              # Faire la requête HTTP et le scraping des données pour la première page uniquement
                                         # response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('article', {'class': 'prd _fb col c-prd'})

    # Parcourir tous les éléments de smartphone trouvés
    for item in items:
        # Extraire le nom, le prix et l'image de chaque élément
        name = item.find('h3', {'class': 'name'})
        price = item.find('div', {'class': 'prc'})
        image = item.find('img', {'class': 'img'}).get('data-src')
        link= item.find('a', {'class': 'core'}).get('href')

        # Formater le nom et le prix en supprimant les espaces et en majuscules
        name = name.text.strip().title() if name else ''
        price = price.text.strip() if price       else ''
        image=image
        link=urljoin(base_url,link)
        
        # Stocker le smartphone extrait 
        smartphone = {
            'name': name,
            'price': price,
            'image': image,
            'link':link
        }

        # Ajouter le smartphone extrait à la liste des smartphones
        smartphones.append(smartphone)

    # Filtrer les smartphones en fonction des critères de recherche


    # Paginer les smartphones filtrés
    paginator = Paginator(smartphones, 30)
    page_obj = paginator.get_page(page_number)

    # envoyer "affiche.html" avec lla page de smartphones demandée
    return render(request, 'affiche.html', {'page_obj': page_obj})


def filtrer_par_prix(request):
    smartphones = []
    for p in range(1,15):
         base_url = 'https://www.jumia.com.tn/smartphones/'

                                             # Récupérer le numéro de page à partir de la requête
    page_number = int(request.GET.get('page', 1))
                             # Récupérer le prix max
    prix_max = request.GET.get('prix_max')

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('article', {'class': 'prd _fb col c-prd'})

    for item in items:
        name = item.find('h3', {'class': 'name'})
        price = item.find('div', {'class': 'prc'})
        image = item.find('img', {'class': 'img'}).get('data-src')

        name = name.text.strip().title() 
        price = price.text.strip() 
        image = image

                                                    # Supprimer les symboles non numériques du prix
        price = ''.join(filter(lambda x: x.isdigit() or x == '.', price))

          #stockage des données extraites 
        smartphone = {
            'name': name,
            'price': price,
            'image': image
        }

        smartphones.append(smartphone)


 # Filtrer les smartphones en fonction du prix max
    filtered_smartphones = smartphones

    if prix_max:
        filtered_smartphones = [smartphone for smartphone in smartphones if smartphone['price'] and float(smartphone['price']) <= float(prix_max)]

    paginator = Paginator(filtered_smartphones, 30)
    page_obj = paginator.get_page(page_number)
    
# Renvoyer la page affiche.html avec les smartphones filtrés et paginés
    return render(request, 'affiche.html', {'page_obj': page_obj, 'prix_max': prix_max})


def filtrer_par_marque(request):
    smartphones = []

    for p in range(1,14):
        base_url = 'https://www.jumia.com.tn/smartphones/'

    page_number = int(request.GET.get('page', 1)) # Récupère le numéro de page de l'URL ou utilise 1 par défaut
    marque = request.GET.get('marque')

    url = f'{base_url}?page={page_number}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('article', {'class': 'prd _fb col c-prd'})

 #  récupère  dechaque élément HTML son nom, son prix et son image
    for item in items:
        name = item.find('h3', {'class': 'name'})
        price = item.find('div', {'class': 'prc'})
        image = item.find('img', {'class': 'img'}).get('data-src')

        name = name.text.strip().title() if name else ''
        price = price.text.strip() if price   else ''
        image = image

        smartphone = {
            'name': name,
            'price': price,
            'image': image
        }
  # Ajoute le smartphone à la liste s'il correspond à la marque filtrée ou si aucune marque n'est spécifiée
        if marque and marque.lower() in name.lower():
            smartphones.append(smartphone)
        elif not marque:
            smartphones.append(smartphone)

    paginator = Paginator(smartphones, 30)
    page_obj = paginator.get_page(page_number)

    return render(request, 'affiche.html', {'page_obj': page_obj, 'marque': marque})



def details(request):
    image = request.GET.get('image')
    link = request.GET.get('link')
    price = request.GET.get('price')
    name = request.GET.get('name')

    context = {
        'image' : image,
        'link':link,
        'name':name,
        'price':price
    }

    return render(request, 'details.html', context)
