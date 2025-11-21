'use client';

import { useState } from 'react';
import { useMutation } from 'convex/react';
import { api } from '@/convex/_generated/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Upload, CheckCircle, AlertCircle, Database } from 'lucide-react';

export function FighterDataMigration() {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [uploadResults, setUploadResults] = useState<any>(null);
  const [currentBatch, setCurrentBatch] = useState(0);
  const [totalBatches, setTotalBatches] = useState(0);

  const bulkInsertFighters = useMutation(api.fighters.bulkInsertFighters);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setUploadStatus('uploading');
    setCurrentBatch(0);

    try {
      // Read the JSON file
      const text = await file.text();
      const fighterData = JSON.parse(text);

      console.log(`Loaded ${fighterData.length} fighters from file`);

      // Upload in batches
      const batchSize = 10;
      const batches = [];
      
      for (let i = 0; i < fighterData.length; i += batchSize) {
        batches.push(fighterData.slice(i, i + batchSize));
      }

      setTotalBatches(batches.length);

      let totalUploaded = 0;
      const results = [];

      for (let i = 0; i < batches.length; i++) {
        setCurrentBatch(i + 1);
        
        try {
          const result = await bulkInsertFighters({ fighters: batches[i] });
          totalUploaded += result.inserted;
          results.push({
            batch: i + 1,
            inserted: result.inserted,
            fighters: result.fighters.slice(0, 3).map((f: any) => f.name) // Sample names
          });

          console.log(`Batch ${i + 1}/${batches.length}: ${result.inserted} fighters inserted`);
          
          // Small delay between batches
          if (i < batches.length - 1) {
            await new Promise(resolve => setTimeout(resolve, 500));
          }
        } catch (error) {
          console.error(`Error in batch ${i + 1}:`, error);
          results.push({
            batch: i + 1,
            error: error.message,
            inserted: 0
          });
        }
      }

      setUploadResults({
        totalFighters: fighterData.length,
        totalUploaded,
        results
      });
      setUploadStatus('success');

    } catch (error) {
      console.error('Upload failed:', error);
      setUploadStatus('error');
      setUploadResults({ error: error.message });
    } finally {
      setIsUploading(false);
    }
  };

  const downloadMigrationData = async () => {
    try {
      // This would be the migration data created by the Python script
      const response = await fetch('/fighter_migration_data.json');
      if (!response.ok) {
        alert('Migration data file not found. Please run the Python migration script first.');
        return;
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'fighter_migration_data.json';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
      alert('Could not download migration data. Please ensure the Python script has been run.');
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto" style={{ background: '#14213d', border: '1px solid #fca311' }}>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2" style={{ color: '#ffffff' }}>
          <Database className="h-5 w-5" style={{ color: '#fca311' }} />
          <span>Fighter Data Migration</span>
        </CardTitle>
        <CardDescription style={{ color: '#fca311' }}>
          Upload fighter data from the CSV extraction to Convex database
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {uploadStatus === 'idle' && (
          <div className="space-y-4">
            <div className="text-sm" style={{ color: '#ffffff' }}>
              <h3 className="font-semibold mb-2">Migration Steps:</h3>
              <ol className="list-decimal list-inside space-y-1 ml-4">
                <li>Run the Python script to extract fighter data from CSV</li>
                <li>Upload the generated JSON file using the button below</li>
                <li>Wait for the batch upload to complete</li>
              </ol>
            </div>

            <div className="flex flex-col space-y-3">
              <div className="text-sm" style={{ color: '#fca311' }}>
                Expected file: <code>fighter_migration_data.json</code> from the Python migration script
              </div>
              
              <input
                type="file"
                accept=".json"
                onChange={handleFileUpload}
                className="hidden"
                id="migration-file"
              />
              
              <label
                htmlFor="migration-file"
                className="inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium cursor-pointer"
                style={{ 
                  backgroundColor: '#fca311', 
                  color: '#000000',
                  border: '1px solid #fca311'
                }}
              >
                <Upload className="h-4 w-4 mr-2" />
                Select Migration Data File
              </label>
            </div>
          </div>
        )}

        {uploadStatus === 'uploading' && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2" style={{ color: '#fca311' }}>
              <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
              <span>Uploading fighters to Convex...</span>
            </div>
            
            {totalBatches > 0 && (
              <div className="space-y-2">
                <div className="text-sm" style={{ color: '#ffffff' }}>
                  Batch {currentBatch} of {totalBatches}
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div 
                    className="h-2 rounded-full transition-all duration-300"
                    style={{ 
                      backgroundColor: '#fca311',
                      width: `${(currentBatch / totalBatches) * 100}%`
                    }}
                  />
                </div>
              </div>
            )}
          </div>
        )}

        {uploadStatus === 'success' && uploadResults && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-green-500">
              <CheckCircle className="h-5 w-5" />
              <span className="font-semibold">Migration Completed Successfully!</span>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800 p-3 rounded-md">
                <div className="text-sm text-gray-400">Total Fighters</div>
                <div className="text-2xl font-bold" style={{ color: '#fca311' }}>
                  {uploadResults.totalFighters}
                </div>
              </div>
              
              <div className="bg-gray-800 p-3 rounded-md">
                <div className="text-sm text-gray-400">Successfully Uploaded</div>
                <div className="text-2xl font-bold text-green-500">
                  {uploadResults.totalUploaded}
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <h4 className="font-semibold" style={{ color: '#ffffff' }}>Batch Results:</h4>
              <div className="max-h-64 overflow-y-auto space-y-1">
                {uploadResults.results.map((result: any, index: number) => (
                  <div 
                    key={index} 
                    className="flex items-center justify-between text-sm p-2 bg-gray-800 rounded"
                  >
                    <span style={{ color: '#ffffff' }}>
                      Batch {result.batch}
                    </span>
                    {result.error ? (
                      <span className="text-red-400">{result.error}</span>
                    ) : (
                      <span className="text-green-400">
                        {result.inserted} fighters ({result.fighters.join(', ')}...)
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {uploadStatus === 'error' && uploadResults && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-red-500">
              <AlertCircle className="h-5 w-5" />
              <span className="font-semibold">Migration Failed</span>
            </div>
            
            <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-md p-4">
              <div className="text-sm text-red-400">
                {uploadResults.error || 'An unknown error occurred during migration'}
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}