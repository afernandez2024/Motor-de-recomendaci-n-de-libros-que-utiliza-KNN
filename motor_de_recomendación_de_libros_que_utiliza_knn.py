# -*- coding: utf-8 -*-
"""Motor de recomendación de libros que utiliza KNN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1P35Vg_PgViFJLGWkj0PYTY7YQnyWWSWS
"""

# import libraries (you may add additional imports but you may not have to)
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Cargar los archivos CSV
ratings_file = '/content/BX-Book-Ratings.csv'
books_file = '/content/BX-Books.csv'
users_file = '/content/BX-Users.csv'

ratings_df = pd.read_csv(ratings_file, delimiter=';', encoding='ISO-8859-1')

books_df = pd.read_csv(books_file, delimiter=';', encoding='ISO-8859-1', on_bad_lines='skip')

users_df = pd.read_csv(users_file, delimiter=';', encoding='ISO-8859-1', on_bad_lines='skip')

# Limpiar el conjunto de calificaciones filtrando usuarios con menos de 200 calificaciones y libros con menos de 100 calificaciones
user_ratings_count = ratings_df.groupby('User-ID').size()
book_ratings_count = ratings_df.groupby('ISBN').size()

# Filtrar usuarios con al menos 200 calificaciones y libros con al menos 100 calificaciones
valid_users = user_ratings_count[user_ratings_count >= 200].index
valid_books = book_ratings_count[book_ratings_count >= 100].index

# Filtrar el conjunto de calificaciones para incluir solo usuarios y libros válidos
filtered_ratings_df = ratings_df[(ratings_df['User-ID'].isin(valid_users)) & (ratings_df['ISBN'].isin(valid_books))]

# Crear una matriz pivote donde los usuarios son las columnas y los libros son las filas
book_user_matrix = filtered_ratings_df.pivot(index='ISBN', columns='User-ID', values='Book-Rating').fillna(0)

# Entrenar el modelo de Nearest Neighbors utilizando la métrica de similitud coseno
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(book_user_matrix)

def get_recommends(book_title):
    # Obtener el ISBN del título de libro dado
    book_isbn = books_df[books_df['Book-Title'] == book_title]['ISBN'].values
    if len(book_isbn) == 0:
        return f"El libro '{book_title}' no se encuentra en el conjunto de datos."

    # Encontrar el índice del libro en la matriz pivote
    book_index = book_user_matrix.index.get_loc(book_isbn[0])

    # Utilizar el modelo para encontrar los vecinos más cercanos
    distances, indices = model.kneighbors(book_user_matrix.iloc[book_index, :].values.reshape(1, -1), n_neighbors=6)

    # Obtener los títulos de los libros recomendados y sus distancias
    recommendations = []
    for i in range(1, len(indices.flatten())):
        similar_book_isbn = book_user_matrix.index[indices.flatten()[i]]
        similar_book_title = books_df[books_df['ISBN'] == similar_book_isbn]['Book-Title'].values[0]
        recommendations.append([similar_book_title, distances.flatten()[i]])

    # Retornar el libro consultado y los libros recomendados
    return [book_title, recommendations]

# Ejemplo de uso con el libro "The Queen of the Damned (Vampire Chronicles (Paperback))"
get_recommends("The Queen of the Damned (Vampire Chronicles (Paperback))")