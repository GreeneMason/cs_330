import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

// Create a new prediction
export const createPrediction = mutation({
  args: {
    clerkId: v.string(),
    fighter1Name: v.string(),
    fighter2Name: v.string(),
    predictedWinner: v.string(), // fighter1Name or fighter2Name
    confidence: v.number(), // 0-100
    predictionMethod: v.string(),
    modelVersion: v.optional(v.string()),
    reasoning: v.optional(v.string()),
    eventName: v.optional(v.string()),
    eventDate: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    // Get user by Clerk ID
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) {
      throw new Error("User not found");
    }

    const { clerkId, ...predictionData } = args;
    
    const predictionId = await ctx.db.insert("predictions", {
      userId: user._id,
      ...predictionData,
      isResolved: false,
      createdAt: Date.now(),
    });

    return predictionId;
  },
});

// Get user's predictions by Clerk ID
export const getUserPredictions = query({
  args: { 
    clerkId: v.string(), 
    limit: v.optional(v.number()),
    resolved: v.optional(v.boolean())
  },
  handler: async (ctx, args) => {
    // Get user by Clerk ID
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) {
      return [];
    }

    const limit = args.limit || 50;
    let query = ctx.db
      .query("predictions")
      .filter((q) => q.eq(q.field("userId"), user._id));

    if (args.resolved !== undefined) {
      query = query.filter((q) => q.eq(q.field("isResolved"), args.resolved));
    }

    return await query
      .order("desc")
      .take(limit);
  },
});

// Get user's prediction statistics
export const getUserPredictionStats = query({
  args: { clerkId: v.string() },
  handler: async (ctx, args) => {
    // Get user by Clerk ID
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) {
      return {
        totalPredictions: 0,
        correctPredictions: 0,
        accuracy: 0,
        pendingPredictions: 0,
        averageConfidence: 0,
        recentPredictions: [],
      };
    }

    const predictions = await ctx.db
      .query("predictions")
      .filter((q) => q.eq(q.field("userId"), user._id))
      .collect();

    const totalPredictions = predictions.length;
    const resolvedPredictions = predictions.filter(p => p.isResolved);
    const correctPredictions = resolvedPredictions.filter(p => p.actualResult === p.predictedWinner);
    const pendingPredictions = predictions.filter(p => !p.isResolved).length;
    
    const accuracy = resolvedPredictions.length > 0 
      ? (correctPredictions.length / resolvedPredictions.length) * 100 
      : 0;

    const averageConfidence = totalPredictions > 0 
      ? predictions.reduce((sum, p) => sum + p.confidence, 0) / totalPredictions 
      : 0;

    // Get recent 5 predictions for quick view
    const recentPredictions = predictions
      .sort((a, b) => b.createdAt - a.createdAt)
      .slice(0, 5);

    return {
      totalPredictions,
      correctPredictions: correctPredictions.length,
      accuracy: Math.round(accuracy * 100) / 100,
      pendingPredictions,
      averageConfidence: Math.round(averageConfidence * 100) / 100,
      recentPredictions,
    };
  },
});

// Update prediction with actual result
export const updatePredictionResult = mutation({
  args: {
    predictionId: v.id("predictions"),
    actualResult: v.string(), // The actual winner's name
    resultMethod: v.optional(v.string()),
    round: v.optional(v.number()),
    time: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const prediction = await ctx.db.get(args.predictionId);
    if (!prediction) {
      throw new Error("Prediction not found");
    }

    const { predictionId, ...updateData } = args;

    await ctx.db.patch(predictionId, {
      ...updateData,
      isResolved: true,
      resolvedAt: Date.now(),
    });

    return { success: true };
  },
});

// Delete a prediction (user can only delete their own)
export const deletePrediction = mutation({
  args: {
    predictionId: v.id("predictions"),
    clerkId: v.string(),
  },
  handler: async (ctx, args) => {
    // Get user by Clerk ID
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) {
      throw new Error("User not found");
    }

    const prediction = await ctx.db.get(args.predictionId);
    if (!prediction) {
      throw new Error("Prediction not found");
    }

    // Check if user owns this prediction
    if (prediction.userId !== user._id) {
      throw new Error("Not authorized to delete this prediction");
    }

    await ctx.db.delete(args.predictionId);
    return { success: true };
  },
});

// Get recent predictions across all users (for admin/analytics)
export const getRecentPredictions = query({
  args: { limit: v.optional(v.number()) },
  handler: async (ctx, args) => {
    const limit = args.limit || 20;
    return await ctx.db
      .query("predictions")
      .order("desc")
      .take(limit);
  },
});