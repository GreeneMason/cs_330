'use client';

import { PredictionHistory } from '@/components/features/predictions/prediction-history';

export default function PredictionsPage() {
  return (
    <div className="min-h-screen" style={{ backgroundColor: '#000000' }}>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2" style={{ color: '#ffffff' }}>
            My Predictions
          </h1>
          <p className="text-lg" style={{ color: '#fca311' }}>
            Track your prediction accuracy over time
          </p>
        </div>

        <div className="max-w-6xl mx-auto">
          <PredictionHistory />
        </div>
      </div>
    </div>
  );
}