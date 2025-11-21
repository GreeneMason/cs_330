import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

// Create a new UFC event
export const createEvent = mutation({
  args: {
    name: v.string(),
    date: v.number(),
    location: v.optional(v.string()),
    venue: v.optional(v.string()),
    fights: v.array(v.object({
      fighter1Id: v.id("fighters"),
      fighter2Id: v.id("fighters"),
      fighter1Name: v.string(),
      fighter2Name: v.string(),
      weightClass: v.string(),
      isMainEvent: v.boolean(),
    })),
  },
  handler: async (ctx, args) => {
    return await ctx.db.insert("events", {
      ...args,
      isCompleted: false,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    });
  },
});

// Get upcoming events
export const getUpcomingEvents = query({
  args: { limit: v.optional(v.number()) },
  handler: async (ctx, args) => {
    const limit = args.limit || 10;
    const now = Date.now();
    
    return await ctx.db
      .query("events")
      .filter((q) => 
        q.and(
          q.gte(q.field("date"), now),
          q.eq(q.field("isCompleted"), false)
        )
      )
      .order("asc")
      .take(limit);
  },
});

// Get past events
export const getPastEvents = query({
  args: { limit: v.optional(v.number()) },
  handler: async (ctx, args) => {
    const limit = args.limit || 20;
    
    return await ctx.db
      .query("events")
      .filter((q) => q.eq(q.field("isCompleted"), true))
      .order("desc")
      .take(limit);
  },
});

// Get event by ID
export const getEventById = query({
  args: { eventId: v.id("events") },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.eventId);
  },
});

// Update event results
export const updateEventResults = mutation({
  args: {
    eventId: v.id("events"),
    fightResults: v.array(v.object({
      fighter1Id: v.id("fighters"),
      fighter2Id: v.id("fighters"),
      result: v.object({
        winner: v.string(), // "fighter1", "fighter2", "draw"
        method: v.string(), // "KO", "TKO", "SUB", "DEC", etc.
        round: v.number(),
        time: v.string(),
      }),
    })),
  },
  handler: async (ctx, args) => {
    const event = await ctx.db.get(args.eventId);
    if (!event) throw new Error("Event not found");

    // Update the fights with results
    const updatedFights = event.fights.map(fight => {
      const fightResult = args.fightResults.find(result => 
        (result.fighter1Id === fight.fighter1Id && result.fighter2Id === fight.fighter2Id) ||
        (result.fighter1Id === fight.fighter2Id && result.fighter2Id === fight.fighter1Id)
      );
      
      if (fightResult) {
        return {
          ...fight,
          result: fightResult.result,
        };
      }
      return fight;
    });

    // Mark event as completed
    await ctx.db.patch(args.eventId, {
      fights: updatedFights,
      isCompleted: true,
      updatedAt: Date.now(),
    });

    // Auto-resolve any predictions for this event
    await resolveEventPredictions(ctx, args.eventId, updatedFights);

    return args.eventId;
  },
});

// Get events by date range
export const getEventsByDateRange = query({
  args: { 
    startDate: v.number(), 
    endDate: v.number() 
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("events")
      .filter((q) => 
        q.and(
          q.gte(q.field("date"), args.startDate),
          q.lte(q.field("date"), args.endDate)
        )
      )
      .order("asc")
      .collect();
  },
});

// Get fight card for an event
export const getEventFightCard = query({
  args: { eventId: v.id("events") },
  handler: async (ctx, args) => {
    const event = await ctx.db.get(args.eventId);
    if (!event) return null;

    // Sort fights with main event first
    const sortedFights = [...event.fights].sort((a, b) => {
      if (a.isMainEvent && !b.isMainEvent) return -1;
      if (!a.isMainEvent && b.isMainEvent) return 1;
      return 0;
    });

    return {
      ...event,
      fights: sortedFights,
    };
  },
});

// Helper function to resolve predictions when event is completed
async function resolveEventPredictions(ctx: any, eventId: any, fights: any[]) {
  for (const fight of fights) {
    if (!fight.result) continue;

    // Find all predictions for this fight
    const predictions = await ctx.db
      .query("predictions")
      .filter((q: any) => 
        q.and(
          q.or(
            q.and(
              q.eq(q.field("fighter1Id"), fight.fighter1Id),
              q.eq(q.field("fighter2Id"), fight.fighter2Id)
            ),
            q.and(
              q.eq(q.field("fighter1Id"), fight.fighter2Id),
              q.eq(q.field("fighter2Id"), fight.fighter1Id)
            )
          ),
          q.eq(q.field("isResolved"), false)
        )
      )
      .collect();

    // Resolve each prediction
    for (const prediction of predictions) {
      let actualResult: string;
      
      // Determine actual result based on fight outcome
      if (fight.result.winner === "draw") {
        actualResult = "draw";
      } else if (fight.result.winner === "fighter1") {
        // Check if prediction fighter1 matches fight fighter1
        actualResult = prediction.fighter1Id === fight.fighter1Id ? "fighter1" : "fighter2";
      } else {
        // winner === "fighter2"
        actualResult = prediction.fighter2Id === fight.fighter2Id ? "fighter2" : "fighter1";
      }

      // Update the prediction
      await ctx.db.patch(prediction._id, {
        actualResult,
        resultMethod: fight.result.method,
        round: fight.result.round,
        time: fight.result.time,
        isResolved: true,
        resolvedAt: Date.now(),
      });
    }
  }
}