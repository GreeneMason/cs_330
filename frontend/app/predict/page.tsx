"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Zap, User, TrendingUp, Loader2 } from "lucide-react";
import { FighterSelect } from "@/components/features/predict/fighter-select";

interface Fighter {
  name: string;
  recent_weight_class: string;
  recent_age: number | null;
  height: number | null;
  reach: number | null;
  stance: string;
  wins: number;
  losses: number;
}

interface PredictionResult {
  prediction: string;
  probability: number;
  confidence: number;
  winner: string;
  red_fighter: string;
  blue_fighter: string;
  individual_predictions: Record<string, number>;
}

export default function PredictPage() {
  const [redFighter, setRedFighter] = useState<Fighter | null>(null);
  const [blueFighter, setBlueFighter] = useState<Fighter | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async () => {
    if (!redFighter || !blueFighter) {
      setError("Please select both fighters");
      return;
    }

    if (redFighter.name === blueFighter.name) {
      setError("Please select different fighters");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          redFighter,
          blueFighter,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Prediction failed');
      }

      const result = await response.json();
      setPrediction(result.prediction);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Prediction failed');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8" style={{ backgroundColor: '#000000', minHeight: '100vh', padding: '20px' }}>
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight" style={{ color: '#ffffff' }}>
              Fight Prediction
            </h1>
            <p style={{ color: '#fca311' }}>
              Select existing UFC fighters to predict fight outcomes using our 91.33% accurate AI ensemble
            </p>
          </div>
          <Badge style={{ backgroundColor: '#fca311', color: '#000000' }}>
            <Zap className="h-3 w-3 mr-1" />
            Ready
          </Badge>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {/* Prediction Form */}
        <div className="md:col-span-2">
          <Card style={{ backgroundColor: '#14213d', color: '#ffffff', border: '1px solid #fca311' }}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2" style={{ color: '#ffffff' }}>
                <User className="h-5 w-5" style={{ color: '#fca311' }} />
                Fighter Selection
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid gap-6 md:grid-cols-2">
                {/* Red Fighter */}
                <div className="space-y-4">
                  <div className="text-sm font-medium" style={{ color: '#fca311' }}>
                    Red Fighter
                  </div>
                  <FighterSelect
                    value={redFighter?.name}
                    onSelect={setRedFighter}
                    placeholder="Select red fighter..."
                    side="red"
                  />
                </div>

                {/* Blue Fighter */}
                <div className="space-y-4">
                  <div className="text-sm font-medium" style={{ color: '#ffffff' }}>
                    Blue Fighter
                  </div>
                  <FighterSelect
                    value={blueFighter?.name}
                    onSelect={setBlueFighter}
                    placeholder="Select blue fighter..."
                    side="blue"
                  />
                </div>
              </div>

              {error && (
                <div className="p-4 rounded-lg" style={{ backgroundColor: '#dc2626', color: '#ffffff' }}>
                  {error}
                </div>
              )}

              <Button 
                onClick={handlePredict}
                disabled={loading || !redFighter || !blueFighter}
                size="lg" 
                className="w-full"
                style={{
                  backgroundColor: loading ? '#666666' : '#fca311',
                  color: '#000000',
                  border: 'none'
                }}
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Generating Prediction...
                  </>
                ) : (
                  <>
                    <Zap className="h-4 w-4 mr-2" />
                    Generate Prediction
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Prediction Result */}
        <div>
          <Card style={{ backgroundColor: '#ffffff', color: '#000000', border: '1px solid #fca311' }}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2" style={{ color: '#000000' }}>
                <TrendingUp className="h-5 w-5" style={{ color: '#fca311' }} />
                Prediction Result
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {loading ? (
                <div className="text-center">
                  <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" style={{ color: '#fca311' }} />
                  <div className="text-sm">Analyzing fighters...</div>
                </div>
              ) : prediction ? (
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold" style={{ 
                      color: prediction.winner === 'Red' ? '#fca311' : '#14213d' 
                    }}>
                      {prediction.winner === 'Red' ? redFighter?.name : blueFighter?.name}
                    </div>
                    <p className="text-sm mt-1">Predicted Winner</p>
                  </div>

                  <div className="space-y-3">
                    <div className="flex justify-between text-sm">
                      <span>Confidence:</span>
                      <span style={{ color: '#fca311' }}>
                        {(prediction.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Win Probability:</span>
                      <span style={{ color: '#fca311' }}>
                        {(prediction.probability * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  {prediction.individual_predictions && (
                    <div className="text-xs mt-4">
                      <p className="font-medium mb-2">Model Breakdown:</p>
                      <ul className="space-y-1">
                        {Object.entries(prediction.individual_predictions).map(([model, prob]) => (
                          <li key={model} className="flex justify-between">
                            <span>{model.replace('_', ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}:</span>
                            <span style={{ color: '#fca311' }}>{(prob * 100).toFixed(1)}%</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center">
                  <div className="text-2xl font-bold" style={{ color: '#666666' }}>
                    Select fighters
                  </div>
                  <p className="text-sm mt-2">
                    Choose red and blue fighters to see prediction results
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}