import pandas as pd
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split

# Charger les données
df = pd.read_csv('C:/Users/PC/Desktop/GI3/Ai/project AI/ai/ai/datastore.csv', header=None, names=['Category', 'Transaction_Id'])

# Fonction pour prétraiter le texte
def preprocess_text(text):
    # Supprimer les espaces en début et en fin de chaîne
    text = text.strip()
    # Mettre la chaîne en minuscules
    text = text.lower()
    # Remplacer les espaces par des tirets
    text = text.replace(" ", "-")
    return text

# Appliquer la prétraitement sur les catégories
df['Processed_Category'] = df['Category'].apply(preprocess_text)


# Préparer les phrases pour Word2Vec en ajoutant les transaction_ids
sentences = df.groupby('Transaction_Id')['Processed_Category'].apply(list).tolist()

# Entraîner le modèle Word2Vec
model = Word2Vec(sentences=sentences, vector_size=100, window=10, min_count=1, workers=4, epochs=100)

# Enregistrer le modèle
model.save("word2veclunettes_model.model")

# Charger le modèle Word2Vec
model = Word2Vec.load("word2veclunettes_model.model")

# Exemple : Obtenir des mots similaires pour un mot clé donné
target_keyword = "Lunettes-de-soleil"
target_keyword_work = preprocess_text(target_keyword)
target_transaction_id = df[df['Processed_Category'] == target_keyword_work]['Transaction_Id'].values[0]

# Obtenez des mots similaires basés sur la transaction_id
similar_words = model.wv.most_similar(f"{target_keyword_work}", topn=5)

# Afficher les résultats
print(f"Words related to '{target_keyword}' with the same transaction_id '{target_transaction_id}':")
for word, similarity in similar_words:
    print(f"{word.split('-')[0]}: {similarity}")
