from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import sql

# Configuration de la connexion PostgreSQL
DB_CONFIG = {
    "dbname": "mindlet_tp",
    "user": "mindlet",
    "password": "MindletForever",
    "host": "localhost",
    "port": "5499"
}
# Initialisation de Faker et connexion à MongoDB
fake = Faker()

def main():

    # Connexion à la base de données PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    print("Connexion réussie à la base de données PostgreSQL.")

    # Connexion à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["tp_mongodb"]
    print("Connexion réussie à la base de données MongoDB.")

    # Génération de données PostgreSQL
    delete_pg_tables(conn)

    users_ids = generate_users_data(conn, 50)

    for user_id in users_ids:
        no_of_collections = random.randint(20, 50)
        collections = generate_collections_data(conn, no_of_collections, user_id)

        for collection_id in collections:
            no_of_cards = random.randint(50, 80)
            generate_cards_data(conn, no_of_cards, collection_id)

    # Suppression des collections existantes
    client.drop_database("tp_mongodb")
    generate_website_data(db, 100)
    generate_support_data(db, 50, users_ids)
    generate_subscription_data(db, 75, users_ids)
    generate_mobile_data(db, 100, users_ids)

    print("Données générées et insérées avec succès !")



# Génération de données pour la collection "website"
def generate_website_data(db, n):
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
def generate_support_data(db, n, users_ids):
    support_data = []
    categories = ["billing", "bug", "feature", "other"]
    statuses = ["open", "closed"]
    for _ in range(n):
        support_data.append({
            "ticket_id": fake.uuid4(),
            "user_id": random.choice(users_ids),
            "date": fake.date_time_between(start_date="-1y", end_date="now"),
            "category": random.choice(categories),
            "status": random.choice(statuses)
        })
    db.support.insert_many(support_data)
    print(f"{n} documents insérés dans la collection 'support'.")

# Génération de données pour la collection "subscription"
def generate_subscription_data(db, n, users_ids):
    subscription_data = []
    actions = ["subscribe", "unsubscribe", "renew"]
    types = ["free", "pro", "premium"]
    for _ in range(n):
        subscription_data.append({
            "user_id": random.choice(users_ids),
            "action_type": random.choice(actions),
            "subscription_type": random.choice(types),
            "date": fake.date_time_between(start_date="-1y", end_date="now")
        })
    db.subscription.insert_many(subscription_data)
    print(f"{n} documents insérés dans la collection 'subscription'.")

# Génération de données pour la collection "mobile"
def generate_mobile_data(db, n, users_ids):
    mobile_data = []
    features = ["flashcards", "quiz", "analytics", "settings"]
    for _ in range(n):
        mobile_data.append({
            "user_id": random.choice(users_ids),
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


def generate_users_data(conn, n):
    users_ids = []
    with conn.cursor() as cur:
        for _ in range(n):
            cur.execute("""
                INSERT INTO users (email, username)
                VALUES (%s, %s)
                RETURNING user_id;
            """, (
                fake.email(),
                fake.user_name()
            ))
            result = cur.fetchone()
            users_ids.append(result[0])
        conn.commit()
        print(f"{n} utilisateurs insérés dans la table 'users'.")
    return users_ids


def generate_collections_data(conn, n, owner_id):
    collections_ids = []
    with conn.cursor() as cur:
        for _ in range(n):
            cur.execute("""
                INSERT INTO collections (title, description, owner_id)
                VALUES (%s, %s, %s)
                RETURNING collection_id;
            """, (
                fake.sentence(),
                fake.text(),
                owner_id
            ))
            result = cur.fetchone()
            collections_ids.append(result[0])
        conn.commit()
        print(f"{n} collections insérées dans la table 'collections'.")
    return collections_ids


def generate_cards_data(conn, n, collection_id):
    with conn.cursor() as cur:
        for _ in range(n):
            cur.execute("""
                INSERT INTO cards (front, back, collection_id)
                VALUES (%s, %s, %s);
            """, (
                fake.sentence(),
                fake.sentence(),
                collection_id
            ))
        conn.commit()
        print(f"{n} cartes insérées dans la table 'cards'.")


def delete_pg_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM cards;
            DELETE FROM collections;
            DELETE FROM users;
        """)
        conn.commit()
        print("Tables supprimées avec succès.")

if __name__ == "__main__":
    main()