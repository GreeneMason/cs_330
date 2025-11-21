"use client";

import { PredictionForm } from "@/components/features/predictions/prediction-form";

export default function PredictPage() {
  return (
    <>
      <div 
        className="fixed inset-0 -z-10"
        style={{ 
          backgroundColor: '#000000', 
          backgroundImage: `
            radial-gradient(circle at bottom left, rgba(239, 68, 68, 0.15) 0%, transparent 50%),
            radial-gradient(circle at top right, rgba(59, 130, 246, 0.15) 0%, transparent 50%)
          `,
        }}
      />
      <div className="space-y-8" style={{ minHeight: '100vh', padding: '20px' }}>
        <div className="flex flex-col gap-4">
        <div className="flex justify-center text-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight" style={{ color: '#ffffff' }}>
              Fight Prediction
            </h1>
            <p style={{ color: '#fca311' }}>
              Select existing fighters to predict fight outcomes using our 91.33% accurate AI ensemble
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto">
        <PredictionForm />
      </div>
    </div>
    </>
  );
}