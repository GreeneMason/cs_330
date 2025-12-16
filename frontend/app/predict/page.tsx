"use client";

import { PredictionForm } from "@/components/features/predictions/prediction-form";

export default function PredictPage() {
  return (
    <>
      <div 
        className="fixed inset-0 -z-10"
        style={{ 
          backgroundColor: '#00043a', 
          backgroundImage: `
            radial-gradient(circle at bottom left, rgba(255, 0, 43, 0.15) 0%, transparent 50%),
            radial-gradient(circle at top right, rgba(64, 123, 167, 0.15) 0%, transparent 50%)
          `,
        }}
      />
      <div className="space-y-8" style={{ minHeight: '100vh', padding: '20px' }}>
        <div className="flex flex-col gap-4">
        <div className="flex justify-center text-center">
          <div>
            <h1 className="font-bold tracking-tight" style={{ color: '#ffffff', fontSize: '2.625rem' }}>
              Fight Prediction
            </h1>
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