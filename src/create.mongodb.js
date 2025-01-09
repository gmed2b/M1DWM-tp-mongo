
db.dropDatabase();

db.createCollection("website", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["ip_address", "date", "session_duration", "newsletter_subscription", "number_of_clicks"],
      properties: {
        ip_address: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        date: {
          bsonType: "date",
          description: "must be a date and is required"
        },
        session_duration: {
          bsonType: "int",
          description: "must be an integer and is required"
        },
        newsletter_subscription: {
          bsonType: "bool",
          description: "must be a boolean and is required"
        },
        number_of_clicks: {
          bsonType: "int",
          description: "must be an integer and is required"
        }
      }
    }
  }
});

db.createCollection("support", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["ticket_id", "user_id", "date", "category", "status"],
      properties: {
        ticket_id: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        user_id: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        date: {
          bsonType: "date",
          description: "must be a date and is required"
        },
        category: {
          enum: ["billing", "bug", "feature", "other"],
          description: "must be a string and is required"
        },
        status: {
          enum: ["open", "closed"],
          description: "must be either open or closed and is required"
        }
      }
    }
  }
});

db.createCollection("subscription", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "action_type", "subscription_type", "date"],
      properties: {
        user_id: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        action_type: {
          enum: ["subscribe", "unsubscribe", "renew"],
          description: "must be either subscribe or unsubscribe or renew and is required"
        },
        subscription_type: {
          enum: ["free", "pro", "premium"],
          description: "must be either free, pro or premium and is required"
        },
        date: {
          bsonType: "date",
          description: "must be a date and is required"
        }
      }
    }
  }
});

db.createCollection("mobile", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "date", "session_duration", "feature_clicks", "ai_card_modifications", "premium_features_usage"],
      properties: {
        user_id: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        date: {
          bsonType: "date",
          description: "must be a date and is required"
        },
        session_duration: {
          bsonType: "int",
          description: "must be an integer and is required"
        },
        feature_clicks: {
          bsonType: "object",
          required: ["feature_name", "clicks"],
          properties: {
            feature_name: {
              bsonType: "string",
              description: "must be a string and is required"
            },
            clicks: {
              bsonType: "int",
              description: "must be an integer and is required"
            }
          }
        },
        ai_card_modifications: {
          bsonType: "int",
          description: "must be an integer and is required"
        },
        premium_features_usage: {
          bsonType: "int",
          description: "must be an integer and is required"
        }
      }
    }
  }
});