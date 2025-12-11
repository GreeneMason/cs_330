'use client';

import { useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { useQuery, useMutation } from 'convex/react';
import { api } from '@/convex/_generated/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BarChart3, Trophy, Clock, TrendingUp, Eye, Trash2, AlertCircle } from 'lucide-react';
import { format } from 'date-fns';

interface PredictionCardProps {
  prediction: any;
  onDelete?: (id: string) => void;
  showDeleteButton?: boolean;
}

function PredictionCard({ prediction, onDelete, showDeleteButton = false }: PredictionCardProps) {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (!onDelete) return;
    setIsDeleting(true);
    try {
      await onDelete(prediction._id);
    } finally {
      setIsDeleting(false);
    }
  };

  const getStatusBadge = () => {
    if (!prediction.isResolved) {
      return (
        <Badge variant="outline" style={{ borderColor: '#f59e0b', color: '#f59e0b' }}>
          <Clock className="h-3 w-3 mr-1" />
          Pending
        </Badge>
      );
    }

    const isCorrect = prediction.actualResult === prediction.predictedWinner;
    return (
      <Badge 
        variant={isCorrect ? "default" : "destructive"}
        style={isCorrect ? { backgroundColor: '#10b981', color: '#ffffff' } : {}}
      >
        {isCorrect ? '✓ Correct' : '✗ Incorrect'}
      </Badge>
    );
  };

  return (
    <Card className="mb-4" style={{ background: '#002962', border: '1px solid #ff002b' }}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Trophy className="h-5 w-5" style={{ color: '#ff002b' }} />
            <div>
              <CardTitle className="text-base" style={{ color: '#ffffff' }}>
                {prediction.fighter1Name} vs {prediction.fighter2Name}
              </CardTitle>
              <CardDescription style={{ color: '#ff002b' }}>
                {prediction.eventName || 'Fight Event'}
              </CardDescription>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {getStatusBadge()}
            {showDeleteButton && !prediction.isResolved && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleDelete}
                disabled={isDeleting}
                style={{ borderColor: '#ef4444', color: '#ef4444' }}
              >
                {isDeleting ? (
                  <div className="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin" />
                ) : (
                  <Trash2 className="h-3 w-3" />
                )}
              </Button>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-400">Predicted Winner</p>
            <p className="font-semibold" style={{ color: '#ffffff' }}>{prediction.predictedWinner}</p>
          </div>
          <div>
            <p className="text-gray-400">Confidence</p>
            <p className="font-semibold" style={{ color: '#ffffff' }}>{prediction.confidence}%</p>
          </div>
          <div>
            <p className="text-gray-400">Method</p>
            <p className="font-semibold" style={{ color: '#ffffff' }}>{prediction.predictionMethod}</p>
          </div>
          <div>
            <p className="text-gray-400">Date</p>
            <p className="font-semibold" style={{ color: '#ffffff' }}>
              {format(new Date(prediction.createdAt), 'MMM dd, yyyy')}
            </p>
          </div>
          {prediction.isResolved && (
            <>
              <div>
                <p className="text-gray-400">Actual Winner</p>
                <p className="font-semibold" style={{ color: '#ffffff' }}>{prediction.actualResult}</p>
              </div>
              <div>
                <p className="text-gray-400">Result Method</p>
                <p className="font-semibold" style={{ color: '#ffffff' }}>
                  {prediction.resultMethod || 'N/A'}
                </p>
              </div>
            </>
          )}
        </div>
        {prediction.reasoning && (
          <div className="mt-3 pt-3 border-t border-gray-600">
            <p className="text-gray-400 text-xs">Reasoning</p>
            <p className="text-sm" style={{ color: '#ffffff' }}>{prediction.reasoning}</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function PredictionHistory() {
  const { user } = useUser();
  const [activeTab, setActiveTab] = useState('all');
  
  const predictionStats = useQuery(
    api.predictions.getUserPredictionStats,
    user ? { clerkId: user.id } : "skip"
  );

  const allPredictions = useQuery(
    api.predictions.getUserPredictions,
    user ? { clerkId: user.id, limit: 100 } : "skip"
  );

  const pendingPredictions = useQuery(
    api.predictions.getUserPredictions,
    user ? { clerkId: user.id, limit: 50, resolved: false } : "skip"
  );

  const resolvedPredictions = useQuery(
    api.predictions.getUserPredictions,
    user ? { clerkId: user.id, limit: 50, resolved: true } : "skip"
  );

  const deletePrediction = useMutation(api.predictions.deletePrediction);

  const handleDeletePrediction = async (predictionId: string) => {
    if (!user) return;
    try {
      await deletePrediction({
        predictionId: predictionId as any,
        clerkId: user.id,
      });
    } catch (error) {
      console.error('Failed to delete prediction:', error);
    }
  };

  if (!predictionStats || !allPredictions) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center space-y-4">
          <div className="w-8 h-8 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin mx-auto" />
          <p className="text-gray-600">Loading prediction history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Statistics Overview */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Predictions</CardTitle>
            <BarChart3 className="h-4 w-4" style={{ color: '#ff002b' }} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{predictionStats.totalPredictions}</div>
          </CardContent>
        </Card>

        <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Accuracy</CardTitle>
            <Trophy className="h-4 w-4" style={{ color: '#ff002b' }} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{predictionStats.accuracy}%</div>
            <p className="text-xs text-muted-foreground">
              {predictionStats.correctPredictions} correct
            </p>
          </CardContent>
        </Card>

        <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending</CardTitle>
            <Clock className="h-4 w-4" style={{ color: '#ff002b' }} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{predictionStats.pendingPredictions}</div>
            <p className="text-xs text-muted-foreground">Awaiting results</p>
          </CardContent>
        </Card>

        <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Confidence</CardTitle>
            <TrendingUp className="h-4 w-4" style={{ color: '#ff002b' }} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{predictionStats.averageConfidence}%</div>
            <p className="text-xs text-muted-foreground">Average certainty</p>
          </CardContent>
        </Card>
      </div>

      {/* Prediction Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="all">All Predictions ({allPredictions?.length || 0})</TabsTrigger>
          <TabsTrigger value="pending">Pending ({predictionStats.pendingPredictions})</TabsTrigger>
          <TabsTrigger value="resolved">Resolved ({predictionStats.correctPredictions + (predictionStats.totalPredictions - predictionStats.correctPredictions - predictionStats.pendingPredictions)})</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          {allPredictions?.length === 0 ? (
            <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
              <CardContent className="text-center py-12">
                <Trophy className="h-12 w-12 mx-auto mb-4" style={{ color: '#ff002b' }} />
                <h3 className="text-lg font-medium mb-2">No Predictions Yet</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Start making predictions to track your forecasting skills!
                </p>
                <Button style={{ backgroundColor: '#ff002b', color: '#ffffff' }}>
                  Make Your First Prediction
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              {allPredictions?.map((prediction) => (
                <PredictionCard 
                  key={prediction._id} 
                  prediction={prediction}
                  onDelete={handleDeletePrediction}
                  showDeleteButton={true}
                />
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="pending" className="space-y-4">
          {pendingPredictions?.length === 0 ? (
            <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
              <CardContent className="text-center py-8">
                <Clock className="h-8 w-8 mx-auto mb-3" style={{ color: '#ff002b' }} />
                <p>No pending predictions</p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              {pendingPredictions?.map((prediction) => (
                <PredictionCard 
                  key={prediction._id} 
                  prediction={prediction}
                  onDelete={handleDeletePrediction}
                  showDeleteButton={true}
                />
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="resolved" className="space-y-4">
          {resolvedPredictions?.length === 0 ? (
            <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
              <CardContent className="text-center py-8">
                <Eye className="h-8 w-8 mx-auto mb-3" style={{ color: '#ff002b' }} />
                <p>No resolved predictions yet</p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              {resolvedPredictions?.map((prediction) => (
                <PredictionCard 
                  key={prediction._id} 
                  prediction={prediction}
                />
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}