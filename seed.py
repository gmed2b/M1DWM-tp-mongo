from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialisation de Faker et connexion à MongoDB
fake = Faker()
client = MongoClient("mongodb://localhost:27017/")
db = client["tp_mongodb"]

# Génération de données pour la collection "website"
def generate_website_data(n):
    website_data = []
    for _ in range(n):
        website_data.append({
            "ip_address": fake.ipv4(),
            "date": fake.date_time_between(start_date="-1y", end_date="now"),
            "session_duration": random.randint(10, 3600),  # en secondes
            "newsletter_subscription": fake.boolean(chance_of_getting_true=30),
            "number_of_clicks": random.randint(1, 100)
        })
    db.website.insert_many(website_data)
    print(f"{n} documents insérés dans la collection 'website'.")

# Génération de données pour la collection "support"
def generate_support_data(n):
    support_data = []
    categories = ["billing", "bug", "feature", "other"]
    statuses = ["open", "closed"]
    for _ in range(n):
        support_data.append({
            "ticket_id": fake.uuid4(),
            "user_id": fake.uuid4(),
            "date": fake.date_time_between(start_date="-1y", end_date="now"),
            "category": random.choice(categories),
            "status": random.choice(statuses)
        })
    db.support.insert_many(support_data)
    print(f"{n} documents insérés dans la collection 'support'.")

# Génération de données pour la collection "subscription"
def generate_subscription_data(n):
    subscription_data = []
    actions = ["subscribe", "unsubscribe", "renew"]
    types = ["free", "pro", "premium"]
    for _ in range(n):
        subscription_data.append({
            "user_id": fake.uuid4(),
            "action_type": random.choice(actions),
            "subscription_type": random.choice(types),
            "date": fake.date_time_between(start_date="-1y", end_date="now")
        })
    db.subscription.insert_many(subscription_data)
    print(f"{n} documents insérés dans la collection 'subscription'.")

# Génération de données pour la collection "mobile"
def generate_mobile_data(n):
    mobile_data = []
    features = ["flashcards", "quiz", "analytics", "settings"]
    for _ in range(n):
        mobile_data.append({
            "user_id": fake.uuid4(),
            "date": fake.date_time_between(start_date="-1y", end_date="now"),
            "session_duration": random.randint(10, 7200),  # en secondes
            "feature_clicks": {
                "feature_name": random.choice(features),
                "clicks": random.randint(1, 50)
            },
            "ai_card_modifications": random.randint(0, 10),
            "premium_features_usage": random.randint(0, 5)
        })
    db.mobile.insert_many(mobile_data)
    print(f"{n} documents insérés dans la collection 'mobile'.")

# Appel des fonctions pour générer des données
generate_website_data(100)
generate_support_data(50)
generate_subscription_data(75)
generate_mobile_data(100)

print("Données générées et insérées avec succès !")
