import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// Create a new fighter
export const createFighter = mutation({
  args: {
    name: v.string(),
    nickname: v.optional(v.string()),
    weightClass: v.string(),
    wins: v.number(),
    losses: v.number(),
    draws: v.optional(v.number()),
    height: v.optional(v.number()),
    weight: v.optional(v.number()),
    reach: v.optional(v.number()),
    stance: v.optional(v.string()),
    age: v.optional(v.number()),
    performance: v.optional(v.object({
      strikeLandedPerMinute: v.optional(v.number()),
      strikeAbsorbedPerMinute: v.optional(v.number()),
      strikeAccuracy: v.optional(v.number()),
      strikeDefense: v.optional(v.number()),
      takedownAccuracy: v.optional(v.number()),
      takedownDefense: v.optional(v.number()),
      submissionAverage: v.optional(v.number()),
      takedownAverage: v.optional(v.number()),
    })),
    lastFightDate: v.optional(v.number()),
    totalFights: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    
    // Check if fighter already exists
    const existingFighter = await ctx.db
      .query("fighters")
      .filter((q) => q.eq(q.field("name"), args.name))
      .first();

    if (existingFighter) {
      throw new Error(`Fighter ${args.name} already exists`);
    }

    return await ctx.db.insert("fighters", {
      name: args.name,
      nickname: args.nickname,
      weightClass: args.weightClass,
      record: {
        wins: args.wins,
        losses: args.losses,
        draws: args.draws || 0,
      },
      stats: {
        height: args.height,
        weight: args.weight,
        reach: args.reach,
        stance: args.stance,
        age: args.age,
      },
      performance: args.performance,
      isActive: true,
      lastFightDate: args.lastFightDate,
      totalFights: args.totalFights,
      createdAt: now,
      updatedAt: now,
    });
  },
});

// Bulk insert fighters (for migration)
export const bulkInsertFighters = mutation({
  args: {
    fighters: v.array(v.object({
      name: v.string(),
      nickname: v.optional(v.string()),
      weightClass: v.string(),
      wins: v.number(),
      losses: v.number(),
      draws: v.optional(v.number()),
      height: v.optional(v.number()),
      weight: v.optional(v.number()),
      reach: v.optional(v.number()),
      stance: v.optional(v.string()),
      age: v.optional(v.number()),
      performance: v.optional(v.object({
        strikeLandedPerMinute: v.optional(v.number()),
        strikeAbsorbedPerMinute: v.optional(v.number()),
        strikeAccuracy: v.optional(v.number()),
        strikeDefense: v.optional(v.number()),
        takedownAccuracy: v.optional(v.number()),
        takedownDefense: v.optional(v.number()),
        submissionAverage: v.optional(v.number()),
        takedownAverage: v.optional(v.number()),
      })),
      lastFightDate: v.optional(v.number()),
      totalFights: v.optional(v.number()),
    })),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    const results = [];

    for (const fighterData of args.fighters) {
      // Check if fighter already exists
      const existingFighter = await ctx.db
        .query("fighters")
        .withIndex("by_name", (q) => q.eq("name", fighterData.name))
        .first();

      if (existingFighter) {
        console.log(`Fighter ${fighterData.name} already exists, skipping`);
        continue;
      }

      try {
        const fighterId = await ctx.db.insert("fighters", {
          name: fighterData.name,
          nickname: fighterData.nickname,
          weightClass: fighterData.weightClass,
          record: {
            wins: fighterData.wins,
            losses: fighterData.losses,
            draws: fighterData.draws || 0,
          },
          stats: {
            height: fighterData.height,
            weight: fighterData.weight,
            reach: fighterData.reach,
            stance: fighterData.stance,
            age: fighterData.age,
          },
          performance: fighterData.performance,
          isActive: true,
          lastFightDate: fighterData.lastFightDate,
          totalFights: fighterData.totalFights,
          createdAt: now,
          updatedAt: now,
        });
        
        results.push({ name: fighterData.name, id: fighterId });
      } catch (error) {
        console.error(`Failed to insert fighter ${fighterData.name}:`, error);
      }
    }

    return { inserted: results.length, fighters: results };
  },
});

// Get all fighters
export const listFighters = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db
      .query("fighters")
      .order("desc")
      .collect();
  },
});

// Get fighters by weight class
export const getFightersByWeightClass = query({
  args: {
    weightClass: v.string(),
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("fighters")
      .withIndex("by_weight_class", (q) => q.eq("weightClass", args.weightClass))
      .collect();
  },
});

// Search fighters by name
export const searchFighters = query({
  args: {
    searchTerm: v.string(),
  },
  handler: async (ctx, args) => {
    if (!args.searchTerm) return [];

    return await ctx.db
      .query("fighters")
      .withSearchIndex("search_name", (q) => 
        q.search("name", args.searchTerm)
      )
      .take(10);
  },
});

// Get fighter by name
export const getFighterByName = query({
  args: {
    name: v.string(),
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("fighters")
      .filter((q) => q.eq(q.field("name"), args.name))
      .first();
  },
});

// Get fighter statistics
export const getFighterStats = query({
  args: {},
  handler: async (ctx) => {
    const fighters = await ctx.db
      .query("fighters")
      .collect();

    const weightClassCounts: Record<string, number> = {};
    let activeFighters = 0;
    let totalFighters = fighters.length;

    fighters.forEach(fighter => {
      weightClassCounts[fighter.weightClass] = (weightClassCounts[fighter.weightClass] || 0) + 1;
      if (fighter.isActive) activeFighters++;
    });

    return {
      total: totalFighters,
      active: activeFighters,
      inactive: totalFighters - activeFighters,
      byWeightClass: weightClassCounts,
    };
  },
});