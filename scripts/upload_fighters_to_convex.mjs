import { ConvexHttpClient } from "convex/browser";
import { api } from "../frontend/convex/_generated/api.js";
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read Convex URL from environment or config
const CONVEX_URL = process.env.CONVEX_URL || "https://keen-cat-12.convex.cloud";

async function uploadFightersToConvex() {
  console.log("=== Uploading Fighter Data to Convex ===");
  
  // Initialize Convex client
  const client = new ConvexHttpClient(CONVEX_URL);
  
  // Read the migration data
  const migrationDataPath = path.join(__dirname, 'fighter_migration_data.json');
  
  if (!fs.existsSync(migrationDataPath)) {
    console.error(`Migration data file not found at: ${migrationDataPath}`);
    console.error('Please run the Python migration script first:');
    console.error('python scripts/migrate_fighters_to_convex.py');
    process.exit(1);
  }
  
  let fighterData;
  try {
    const jsonData = fs.readFileSync(migrationDataPath, 'utf8');
    fighterData = JSON.parse(jsonData);
    console.log(`Loaded ${fighterData.length} fighters from migration file`);
  } catch (error) {
    console.error('Error reading migration data:', error);
    process.exit(1);
  }
  
  // Upload in batches to avoid timeouts
  const batchSize = 50;
  const totalBatches = Math.ceil(fighterData.length / batchSize);
  let totalUploaded = 0;
  
  console.log(`Uploading in ${totalBatches} batches of ${batchSize} fighters each...`);
  
  for (let i = 0; i < totalBatches; i++) {
    const start = i * batchSize;
    const end = Math.min(start + batchSize, fighterData.length);
    const batch = fighterData.slice(start, end);
    
    console.log(`\nUploading batch ${i + 1}/${totalBatches} (fighters ${start + 1}-${end})...`);
    
    try {
      const result = await client.mutation(api.fighters.bulkInsertFighters, {
        fighters: batch
      });
      
      console.log(`✅ Batch ${i + 1} completed: ${result.inserted} fighters inserted`);
      totalUploaded += result.inserted;
      
      // Show some uploaded fighter names
      if (result.fighters.length > 0) {
        const sampleNames = result.fighters.slice(0, 3).map(f => f.name).join(', ');
        console.log(`   Sample: ${sampleNames}${result.fighters.length > 3 ? '...' : ''}`);
      }
      
      // Small delay between batches to be nice to the server
      await new Promise(resolve => setTimeout(resolve, 500));
      
    } catch (error) {
      console.error(`❌ Error uploading batch ${i + 1}:`, error.message);
      
      // Try to get more details about the error
      if (error.data) {
        console.error('Error details:', error.data);
      }
      
      // Continue with next batch instead of failing completely
      console.log('Continuing with next batch...');
    }
  }
  
  console.log(`\n=== Migration Complete ===`);
  console.log(`Total fighters uploaded: ${totalUploaded}/${fighterData.length}`);
  
  if (totalUploaded < fighterData.length) {
    console.log(`⚠️  ${fighterData.length - totalUploaded} fighters were skipped (likely duplicates or errors)`);
  }
  
  // Verify the upload by getting fighter stats
  try {
    console.log('\nVerifying upload...');
    const stats = await client.query(api.fighters.getFighterStats, {});
    console.log(`✅ Verification successful: ${stats.total} fighters now in database`);
    console.log(`   Active fighters: ${stats.active}`);
    console.log(`   Weight classes: ${Object.keys(stats.byWeightClass).length}`);
    
    // Show weight class distribution
    console.log('\nWeight class distribution:');
    Object.entries(stats.byWeightClass)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .forEach(([weightClass, count]) => {
        console.log(`   ${weightClass}: ${count} fighters`);
      });
      
  } catch (error) {
    console.error('Error verifying upload:', error.message);
  }
}

// Run the upload
uploadFightersToConvex()
  .then(() => {
    console.log('\n🎉 Fighter migration completed successfully!');
    process.exit(0);
  })
  .catch((error) => {
    console.error('\n💥 Migration failed:', error);
    process.exit(1);
  });