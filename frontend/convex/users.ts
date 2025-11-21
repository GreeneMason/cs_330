import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// Create a new user profile
export const createUser = mutation({
  args: {
    clerkId: v.string(),
    email: v.string(),
    username: v.string(),
    iconColor: v.string(),
    acceptedTerms: v.boolean(),
    acceptedTermsAt: v.number(),
  },
  handler: async (ctx, args) => {
    // Check if user already exists
    const existingUser = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (existingUser) {
      throw new Error("User already exists");
    }

    // Check if username is taken
    const existingUsername = await ctx.db
      .query("users")
      .withIndex("by_username", (q) => q.eq("username", args.username))
      .first();

    if (existingUsername) {
      throw new Error("Username is already taken");
    }

    const now = Date.now();
    
    return await ctx.db.insert("users", {
      clerkId: args.clerkId,
      email: args.email,
      username: args.username,
      iconColor: args.iconColor,
      acceptedTerms: args.acceptedTerms,
      acceptedTermsAt: args.acceptedTermsAt,
      createdAt: now,
      updatedAt: now,
      preferences: {
        notifications: true,
        theme: "dark",
      },
    });
  },
});

// Get user by Clerk ID
export const getUserByClerkId = query({
  args: { clerkId: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();
  },
});

// Check if username is available
export const checkUsernameAvailable = query({
  args: { username: v.string() },
  handler: async (ctx, args) => {
    const existingUser = await ctx.db
      .query("users")
      .withIndex("by_username", (q) => q.eq("username", args.username))
      .first();
    
    return !existingUser;
  },
});

// Update user profile
export const updateUser = mutation({
  args: {
    clerkId: v.string(),
    updates: v.object({
      username: v.optional(v.string()),
      iconColor: v.optional(v.string()),
      preferences: v.optional(v.object({
        favoriteWeightClass: v.optional(v.string()),
        notifications: v.optional(v.boolean()),
        theme: v.optional(v.string()),
      })),
    }),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) {
      throw new Error("User not found");
    }

    // If updating username, check availability
    if (args.updates.username && args.updates.username !== user.username) {
      const existingUsername = await ctx.db
        .query("users")
        .withIndex("by_username", (q) => q.eq("username", args.updates.username!))
        .first();

      if (existingUsername) {
        throw new Error("Username is already taken");
      }
    }

    return await ctx.db.patch(user._id, {
      ...args.updates,
      updatedAt: Date.now(),
    });
  },
});

// Get user stats (predictions, accuracy, etc.)
export const getUserStats = query({
  args: { clerkId: v.string() },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) {
      return null;
    }

    // Get user's predictions (simplified for now)
    const totalPredictions = 0; // TODO: implement when predictions are ready
    const correctPredictions = 0;
    const accuracy = 0;

    return {
      user,
      stats: {
        totalPredictions,
        correctPredictions,
        accuracy,
        joinedAt: user.createdAt,
      },
    };
  },
});

// Delete user
export const deleteUser = mutation({
  args: { clerkId: v.string() },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) {
      throw new Error("User not found");
    }

    await ctx.db.delete(user._id);
    return { success: true };
  },
});

// Get all users (admin only)
export const getAllUsers = query({
  handler: async (ctx) => {
    return await ctx.db.query("users").collect();
  },
});