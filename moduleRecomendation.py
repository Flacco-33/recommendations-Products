def get_user_recommendations(user_id, train_data, user_similarity_df, num_recommendations=5):
    if user_id not in train_data.index:
        print(f"El usuario {user_id} no tiene historial de compras.")
        top_products = train_data.sum().nlargest(num_recommendations).index
        return list(top_products)

    user_similarity_row = user_similarity_df.loc[user_id]
    similar_users = user_similarity_row.drop(user_id).sort_values(ascending=False)

    recommendations = []
    user_purchased_products = set(train_data.loc[user_id][train_data.loc[user_id] > 0].index)

    for similar_user_id in similar_users.index:
        similar_user_history = train_data.loc[similar_user_id]
        similar_user_purchased_products = set(similar_user_history[similar_user_history > 0].index)
        recommended_products = similar_user_purchased_products - user_purchased_products
        recommendations.extend(recommended_products)

        if len(recommendations) >= num_recommendations:
            break

    recommendations = list(set(recommendations))[:num_recommendations]
    return recommendations
