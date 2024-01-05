import csv
from selenium import webdriver
from bs4 import BeautifulSoup


# Spécifiez le chemin complet du WebDriver Chrome ici
#path_to_chromedriver = '/chemin/vers/chromedriver'

url = 'https://www.eyebuydirect.com/'
driver = webdriver.Chrome() # Assurez-vous d'avoir ChromeDriver installé et dans votre PATH
driver.get(url)

# Attendre que la page soit entièrement chargée (peut nécessiter des ajustements)
driver.implicitly_wait(10)

soup = BeautifulSoup(driver.page_source, 'html.parser')
product_list = soup.find('div', class_='product-list')

# Parcourir la liste des produits
products = []
for product in product_list.find_all('div', class_='product-item'):
    # Extraire les informations du produit
    product_name = product.find('a', class_='product-name').text.strip()
    product_image = product.find('img')['src']
    product_price = product.find('span', class_='product-price').text
    product_brand = product.find('span', class_='product-brand').text

    # Ajouter le produit à la liste
    products.append({
        'name': product_name,
        'image': product_image,
        'price': product_price,
        'brand': product_brand,
    })

# Enregistrer les données dans un fichier CSV
with open('products.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'image', 'price', 'brand'])
    for product in products:
        writer.writerow([product['name'], product['image'], product['price'], product['brand']])
