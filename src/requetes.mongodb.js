
// Nombre totale d'abonnements par type
use("tp_mongodb");
db.subscription.aggregate([
  {
    $group: {
      _id: "$subscription_type",
      total: { $sum: 1 }
    }
  },
  { $sort: { total: -1 } }
]);

// Total des tickets par catégorie et par jour
use("tp_mongodb");
db.support.aggregate([
  {
    $group: {
      _id: {
        category: "$category",
        date: {
          $dateToString: {
            format: "%Y-%m-%d",
            date: "$date"
          }
        }
      },
      totalTickets: { $sum: 1 }
    }
  },
  { $sort: { "_id.week": 1 } }
]);

// Temps moyen passé sur le site par semaine
use("tp_mongodb");
db.website.aggregate([
  {
    $group: {
      _id: {
        $dateToString: {
          format: "%Y-%m-%d",
          date: "$date"
        }
      },
      avgTimeSpent: { $avg: "$session_duration" }
    }
  },
  { $sort: { "_id": 1 } }
]);

// Fonctionnalités les plus cliquées
use("tp_mongodb");
db.mobile.aggregate([
  { $unwind: "$feature_clicks" },
  {
    $group: {
      _id: "$feature_clicks.feature_name",
      totalClicks: { $sum: "$feature_clicks.click_count" }
    }
  },
  { $sort: { totalClicks: -1 } }
]);

// Proportion des utilisateurs qui modifient des cartes générées par l’IA
use("tp_mongodb");
db.mobile.aggregate([
  {
    $group: {
      _id: "$user_id",
      totalModifications: { $sum: "$ai_card_modifications" }
    }
  },
  {
    $group: {
      _id: null,
      totalUsers: { $sum: 1 },
      usersWithModifications: {
        $sum: {
          $cond: [{ $gt: ["$totalModifications", 0] }, 1, 0]
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      totalUsers: 1,
      usersWithModifications: 1,
      proportionModified: {
        $multiply: [{ $divide: ["$usersWithModifications", "$totalUsers"] }, 100]
      }
    }
  }
]);
