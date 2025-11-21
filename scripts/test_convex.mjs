import { ConvexHttpClient } from "convex/browser";

const client = new ConvexHttpClient("https://vivid-gull-673.convex.cloud");

// Test creating a fighter
const testFighter = {
  name: "Jon Jones",
  weightClass: "Heavyweight", 
  wins: 27,
  losses: 1,
  draws: 0,
  height: 193.04,
  weight: 106.59,
  reach: 215.9,
  stance: "Orthodox",
  age: 36
};

console.log("Testing fighter creation...");

try {
  const result = await client.mutation("fighters:createFighter", testFighter);
  console.log("✅ Fighter created successfully:", result);
  
  // Test listing fighters
  const fighters = await client.query("fighters:listFighters", {});
  console.log("✅ Current fighters in database:", fighters.length);
  
} catch (error) {
  console.error("❌ Error:", error.message);
}

console.log("Test completed!");