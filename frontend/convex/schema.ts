import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Users table - stores user information from Clerk
  users: defineTable({
    clerkId: v.string(),
    email: v.string(),
    username: v.string(),
    iconColor: v.string(), // Hex color for user's icon background
    acceptedTerms: v.boolean(),
    acceptedTermsAt: v.number(),
    createdAt: v.number(),
    updatedAt: v.number(),
    preferences: v.optional(v.object({
      favoriteWeightClass: v.optional(v.string()),
      notifications: v.optional(v.boolean()),
      theme: v.optional(v.string()),
    })),
  })
    .index("by_clerk_id", ["clerkId"])
    .index("by_email", ["email"])
    .index("by_username", ["username"]),

  // Fighters table - stores fighter data
  fighters: defineTable({
    name: v.string(),
    nickname: v.optional(v.string()),
    weightClass: v.string(),
    record: v.object({
      wins: v.number(),
      losses: v.number(),
      draws: v.optional(v.number()),
    }),
    stats: v.object({
      height: v.optional(v.number()), // in cm
      weight: v.optional(v.number()), // in kg
      reach: v.optional(v.number()), // in cm
      stance: v.optional(v.string()),
      age: v.optional(v.number()),
    }),
    performance: v.optional(v.object({
      strikeLandedPerMinute: v.optional(v.number()), // SLpM_total
      strikeAbsorbedPerMinute: v.optional(v.number()), // SApM_total
      strikeAccuracy: v.optional(v.number()), // sig_str_acc_total
      strikeDefense: v.optional(v.number()), // str_def_total
      takedownAccuracy: v.optional(v.number()), // td_acc_total
      takedownDefense: v.optional(v.number()), // td_def_total
      submissionAverage: v.optional(v.number()), // sub_avg
      takedownAverage: v.optional(v.number()), // td_avg
    })),
    isActive: v.boolean(),
    lastFightDate: v.optional(v.number()),
    totalFights: v.optional(v.number()),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_name", ["name"])
    .index("by_weight_class", ["weightClass"])
    .index("by_active", ["isActive"])
    .searchIndex("search_name", {
      searchField: "name",
    }),

  // Predictions table - stores user predictions
  predictions: defineTable({
    userId: v.id("users"),
    fighter1Id: v.optional(v.id("fighters")), // Optional for flexibility
    fighter2Id: v.optional(v.id("fighters")), // Optional for flexibility
    fighter1Name: v.string(), // Denormalized for easy display
    fighter2Name: v.string(), // Denormalized for easy display
    predictedWinner: v.string(), // fighter1Name or fighter2Name (actual name)
    confidence: v.number(), // 0-100
    predictionMethod: v.string(), // "manual", "ml_model", "ensemble", etc.
    modelVersion: v.optional(v.string()),
    reasoning: v.optional(v.string()),
    eventName: v.optional(v.string()),
    eventDate: v.optional(v.number()),
    isResolved: v.boolean(),
    actualResult: v.optional(v.string()), // The actual winner's name
    resultMethod: v.optional(v.string()), // "KO", "TKO", "SUB", "DEC", etc.
    round: v.optional(v.number()),
    time: v.optional(v.string()),
    createdAt: v.number(),
    resolvedAt: v.optional(v.number()),
  })
    .index("by_user", ["userId"])
    .index("by_user_created", ["userId", "createdAt"])
    .index("by_fighters", ["fighter1Name", "fighter2Name"])
    .index("by_resolved", ["isResolved"])
    .index("by_event", ["eventName", "eventDate"]),

  // Events table - stores UFC events
  events: defineTable({
    name: v.string(),
    date: v.number(),
    location: v.optional(v.string()),
    venue: v.optional(v.string()),
    isCompleted: v.boolean(),
    fights: v.array(v.object({
      fighter1Id: v.id("fighters"),
      fighter2Id: v.id("fighters"),
      fighter1Name: v.string(),
      fighter2Name: v.string(),
      weightClass: v.string(),
      isMainEvent: v.boolean(),
      result: v.optional(v.object({
        winner: v.string(), // "fighter1", "fighter2", "draw"
        method: v.string(), // "KO", "TKO", "SUB", "DEC", etc.
        round: v.number(),
        time: v.string(),
      })),
    })),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_date", ["date"])
    .index("by_completed", ["isCompleted"]),

  // User analytics - stores user prediction performance
  userAnalytics: defineTable({
    userId: v.id("users"),
    totalPredictions: v.number(),
    correctPredictions: v.number(),
    accuracy: v.number(), // percentage
    bestWeightClass: v.optional(v.string()),
    worstWeightClass: v.optional(v.string()),
    predictionsByWeightClass: v.object({}), // Dynamic object for weight class stats
    streak: v.object({
      current: v.number(),
      longest: v.number(),
      type: v.string(), // "win" or "loss"
    }),
    monthlyStats: v.array(v.object({
      month: v.string(), // "2025-11"
      predictions: v.number(),
      correct: v.number(),
      accuracy: v.number(),
    })),
    lastUpdated: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_accuracy", ["accuracy"]),

  // System settings and configurations
  settings: defineTable({
    key: v.string(),
    value: v.any(),
    description: v.optional(v.string()),
    updatedAt: v.number(),
  })
    .index("by_key", ["key"]),
});