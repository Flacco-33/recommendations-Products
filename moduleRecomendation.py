def get_user_recommendations(user_id, train_data, user_similarity_df, num_recommendations=5):
    # Verificar si el usuario está en los datos de entrenamiento
    if user_id not in train_data.index:
        print(f"El usuario {user_id} no tiene historial de compras.")
        top_products = train_data.sum().nlargest(num_recommendations).index
        return list(top_products)

    # Obtener la fila de similitud del usuario
    user_similarity_row = user_similarity_df.loc[user_id]

    # Obtener usuarios similares ordenados por similitud, excluyendo al propio usuario
    similar_users = user_similarity_row.drop(user_id).sort_values(ascending=False)

    # Generar las recomendaciones basadas en los usuarios similares
    recommendations = []
    user_purchased_products = set(train_data.loc[user_id][train_data.loc[user_id] > 0].index)

    for similar_user_id in similar_users.index:
        similar_user_history = train_data.loc[similar_user_id]
        similar_user_purchased_products = set(similar_user_history[similar_user_history > 0].index)

        # Recomendar productos que el usuario similar ha comprado pero el usuario actual no
        recommended_products = similar_user_purchased_products - user_purchased_products
        recommendations.extend(recommended_products)

        # Limitar el número de recomendaciones
        if len(recommendations) >= num_recommendations:
            break

   # Eliminar duplicados y limitar el número de recomendaciones
    recommendations = list(set(recommendations))
    if len(recommendations) < num_recommendations:
        remaining_recommendations = num_recommendations - len(recommendations)
        top_products = train_data.sum().nlargest(remaining_recommendations).index
        recommendations.extend(top_products)

    recommendations = recommendations[:num_recommendations]  # Limitar el número total de recomendaciones

    return recommendations

    return recommendations
