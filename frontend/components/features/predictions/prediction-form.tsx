'use client';

import { useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { useMutation } from 'convex/react';
import { api } from '@/convex/_generated/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { FighterSearch } from '@/components/features/fighters/fighter-search';
import { PredictionVisualization } from './prediction-visualization';
import { AlertCircle, Trophy, Brain, Target } from 'lucide-react';

interface PredictionFormData {
  fighter1Name: string;
  fighter2Name: string;
  predictedWinner: string;
}

export function PredictionForm({ onSuccess }: { onSuccess?: () => void }) {
  const { user } = useUser();
  const createPrediction = useMutation(api.predictions.createPrediction);
  
  const [formData, setFormData] = useState<PredictionFormData>({
    fighter1Name: '',
    fighter2Name: '',
    predictedWinner: '',
  });
  
  const [errors, setErrors] = useState<Record<string, string | undefined>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isGeneratingAI, setIsGeneratingAI] = useState(false);
  const [aiPrediction, setAiPrediction] = useState<any>(null);

  const generateAIPrediction = async () => {
    if (!formData.fighter1Name || !formData.fighter2Name) {
      setErrors(prev => ({
        ...prev,
        fighter1Name: !formData.fighter1Name ? 'Required for AI' : undefined,
        fighter2Name: !formData.fighter2Name ? 'Required for AI' : undefined
      }));
      return;
    }

    setIsGeneratingAI(true);
    setAiPrediction(null);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          redFighter: formData.fighter1Name,
          blueFighter: formData.fighter2Name,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get prediction');
      }

      const data = await response.json();
      setAiPrediction(data);
      
      const result = data.prediction;
      const winnerName = result.prediction === 'Red' ? result.red_fighter : result.blue_fighter;

      // Auto-fill form with AI suggestion if user hasn't selected yet
      if (!formData.predictedWinner) {
        updateFormData('predictedWinner', winnerName);
      }

    } catch (error) {
      console.error('AI Prediction error:', error);
      // You might want to show a toast or error message here
    } finally {
      setIsGeneratingAI(false);
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string | undefined> = {};

    if (!formData.fighter1Name.trim()) {
      newErrors.fighter1Name = 'Fighter 1 name is required';
    }
    
    if (!formData.fighter2Name.trim()) {
      newErrors.fighter2Name = 'Fighter 2 name is required';
    }
    
    if (formData.fighter1Name.toLowerCase() === formData.fighter2Name.toLowerCase()) {
      newErrors.fighter2Name = 'Fighters must be different';
    }

    if (!formData.predictedWinner) {
      newErrors.predictedWinner = 'Please select a winner';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!user || !validateForm()) return;

    setIsSubmitting(true);
    try {
      // Use AI prediction data if available, otherwise defaults
      const confidence = aiPrediction?.prediction?.confidence 
        ? Math.round(aiPrediction.prediction.confidence * 100) 
        : 50;
        
      const reasoning = aiPrediction?.prediction 
        ? `AI Model Prediction: ${aiPrediction.prediction.prediction} (${(aiPrediction.prediction.confidence * 100).toFixed(1)}% confidence).`
        : undefined;

      await createPrediction({
        clerkId: user.id,
        fighter1Name: formData.fighter1Name.trim(),
        fighter2Name: formData.fighter2Name.trim(),
        predictedWinner: formData.predictedWinner,
        confidence: confidence,
        predictionMethod: 'ml_model',
        reasoning: reasoning,
      });

      // Reset form
      setFormData({
        fighter1Name: '',
        fighter2Name: '',
        predictedWinner: '',
      });
      setAiPrediction(null);

      if (onSuccess) onSuccess();
    } catch (error) {
      console.error('Failed to create prediction:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const updateFormData = (field: keyof PredictionFormData, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const selectWinner = (fighterName: string) => {
    updateFormData('predictedWinner', fighterName);
  };

  return (
    <Card className="w-full max-w-2xl mx-auto" style={{ 
      background: '#14213d', 
      border: '1px solid #fca311',
      boxShadow: '0 0 20px rgba(252, 163, 17, 0.15)'
    }}>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2" style={{ color: '#ffffff' }}>
          <Trophy className="h-5 w-5" style={{ color: '#fca311' }} />
          <span>Make a Prediction</span>
        </CardTitle>
        <CardDescription style={{ color: '#fca311' }}>
          Predict the outcome of an upcoming fight
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Fighters */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="fighter1" className="text-lg font-bold uppercase tracking-widest mb-2 block" style={{ 
                background: 'linear-gradient(to right, #ef4444, #f97316)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                textShadow: '0 0 20px rgba(239, 68, 68, 0.3)'
              }}>
                Red Corner
              </Label>
              <FighterSearch
                value={formData.fighter1Name}
                onChange={(value) => updateFormData('fighter1Name', value)}
                placeholder="Search Red Corner Fighter..."
                error={errors.fighter1Name}
              />
              {errors.fighter1Name && (
                <div className="flex items-center space-x-2 text-red-600 text-sm mt-1">
                  <AlertCircle className="h-4 w-4" />
                  <span>{errors.fighter1Name}</span>
                </div>
              )}
            </div>

            <div>
              <Label htmlFor="fighter2" className="text-lg font-bold uppercase tracking-widest mb-2 block" style={{ 
                background: 'linear-gradient(to right, #3b82f6, #06b6d4)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                textShadow: '0 0 20px rgba(59, 130, 246, 0.3)'
              }}>
                Blue Corner
              </Label>
              <FighterSearch
                value={formData.fighter2Name}
                onChange={(value) => updateFormData('fighter2Name', value)}
                placeholder="Search Blue Corner Fighter..."
                error={errors.fighter2Name}
              />
              {errors.fighter2Name && (
                <div className="flex items-center space-x-2 text-red-600 text-sm mt-1">
                  <AlertCircle className="h-4 w-4" />
                  <span>{errors.fighter2Name}</span>
                </div>
              )}
            </div>
          </div>

          {/* AI Prediction Section */}
          <div className="flex flex-col items-center space-y-4 py-2">
            <Button
              type="button"
              onClick={generateAIPrediction}
              disabled={isGeneratingAI || !formData.fighter1Name || !formData.fighter2Name}
              className="w-full md:w-auto px-8"
              style={{ 
                backgroundColor: '#000000', 
                border: '1px solid #fca311',
                color: '#fca311'
              }}
            >
              {isGeneratingAI ? (
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                  <span>Analyzing Matchup...</span>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Brain className="h-4 w-4" />
                  <span>Generate AI Prediction</span>
                </div>
              )}
            </Button>

            {aiPrediction && aiPrediction.prediction && (
              <PredictionVisualization 
                result={aiPrediction.prediction} 
                models={aiPrediction.models}
              />
            )}
          </div>

          {/* Winner Selection */}
          {formData.fighter1Name && formData.fighter2Name && (
            <div>
              <Label style={{ color: '#ffffff' }}>Predicted Winner *</Label>
              <div className="grid grid-cols-2 gap-3 mt-2">
                <Button
                  type="button"
                  variant={formData.predictedWinner === formData.fighter1Name ? "default" : "outline"}
                  onClick={() => selectWinner(formData.fighter1Name)}
                  className="h-16 text-left justify-start"
                  style={{
                    backgroundColor: formData.predictedWinner === formData.fighter1Name ? '#fca311' : 'transparent',
                    borderColor: '#fca311',
                    color: formData.predictedWinner === formData.fighter1Name ? '#000000' : '#fca311'
                  }}
                >
                  <div>
                    <div className="font-medium">{formData.fighter1Name}</div>
                    <div className="text-xs opacity-70">Click to select</div>
                  </div>
                </Button>
                
                <Button
                  type="button"
                  variant={formData.predictedWinner === formData.fighter2Name ? "default" : "outline"}
                  onClick={() => selectWinner(formData.fighter2Name)}
                  className="h-16 text-left justify-start"
                  style={{
                    backgroundColor: formData.predictedWinner === formData.fighter2Name ? '#fca311' : 'transparent',
                    borderColor: '#fca311',
                    color: formData.predictedWinner === formData.fighter2Name ? '#000000' : '#fca311'
                  }}
                >
                  <div>
                    <div className="font-medium">{formData.fighter2Name}</div>
                    <div className="text-xs opacity-70">Click to select</div>
                  </div>
                </Button>
              </div>
              {errors.predictedWinner && (
                <div className="flex items-center space-x-2 text-red-600 text-sm mt-1">
                  <AlertCircle className="h-4 w-4" />
                  <span>{errors.predictedWinner}</span>
                </div>
              )}
            </div>
          )}

          {/* Submit */}
          <div className="flex items-center justify-between pt-4">
            <div className="flex items-center space-x-2">
              <Brain className="h-4 w-4" style={{ color: '#fca311' }} />
              <span className="text-sm" style={{ color: '#fca311' }}>
                Track your prediction accuracy
              </span>
            </div>
            
            <Button
              type="submit"
              disabled={isSubmitting || !formData.fighter1Name || !formData.fighter2Name || !formData.predictedWinner}
              style={{ backgroundColor: '#fca311', color: '#000000' }}
            >
              {isSubmitting ? (
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                  <span>Saving...</span>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Save Prediction</span>
                </div>
              )}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}