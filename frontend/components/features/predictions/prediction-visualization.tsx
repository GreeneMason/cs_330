'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, Cell
} from 'recharts';
import { Activity, Brain } from 'lucide-react';

interface FighterStats {
  age: number;
  height: number;
  weight: number;
  reach: number;
  stance: string;
  wins_total: number;
  losses_total: number;
  SLpM_total: number;
  SApM_total: number;
  sig_str_acc_total: number;
  td_acc_total: number;
  str_def_total: number;
  td_def_total: number;
  sub_avg: number;
  td_avg: number;
}

interface PredictionResult {
  prediction: 'Red' | 'Blue';
  probability: number;
  confidence: number;
  feature_importance: Record<string, number>;
  red_fighter: string;
  blue_fighter: string;
  red_fighter_stats: FighterStats;
  blue_fighter_stats: FighterStats;
}

interface ModelResult {
  name: string;
  winner: string;
  probability: number;
  confidence: number;
  accuracy: string;
}

interface PredictionVisualizationProps {
  result: PredictionResult;
  models?: Record<string, ModelResult>;
}

export function PredictionVisualization({ result, models }: PredictionVisualizationProps) {
  const isRedWinner = result.prediction.includes('Red');
  const winnerName = isRedWinner ? result.red_fighter : result.blue_fighter;
  const loserName = isRedWinner ? result.blue_fighter : result.red_fighter;
  const confidencePercent = Math.round(result.confidence * 100);

  // Prepare data for Radar Chart
  const radarData = [
    {
      subject: 'Striking Acc',
      A: result.red_fighter_stats.sig_str_acc_total * 100,
      B: result.blue_fighter_stats.sig_str_acc_total * 100,
      fullMark: 100,
    },
    {
      subject: 'Grappling Acc',
      A: result.red_fighter_stats.td_acc_total * 100,
      B: result.blue_fighter_stats.td_acc_total * 100,
      fullMark: 100,
    },
    {
      subject: 'Strike Def',
      A: result.red_fighter_stats.str_def_total * 100,
      B: result.blue_fighter_stats.str_def_total * 100,
      fullMark: 100,
    },
    {
      subject: 'Takedown Def',
      A: result.red_fighter_stats.td_def_total * 100,
      B: result.blue_fighter_stats.td_def_total * 100,
      fullMark: 100,
    },
    {
      subject: 'Win Rate',
      A: (result.red_fighter_stats.wins_total / (result.red_fighter_stats.wins_total + result.red_fighter_stats.losses_total || 1)) * 100,
      B: (result.blue_fighter_stats.wins_total / (result.blue_fighter_stats.wins_total + result.blue_fighter_stats.losses_total || 1)) * 100,
      fullMark: 100,
    },
  ];

  // Prepare data for Feature Importance
  const featureData = result.feature_importance 
    ? Object.entries(result.feature_importance)
        .sort(([, a], [, b]) => Math.abs(b) - Math.abs(a))
        .slice(0, 5)
        .map(([key, value]) => ({
          name: key.replace(/_/g, ' '),
          value: Math.abs(value),
          originalValue: value,
        }))
    : [];

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* Main Result Card */}
      <Card 
        className="border-2 border-[#ff002b] bg-[#00043a]/50 backdrop-blur-sm"
        style={{ boxShadow: '0 0 25px rgba(255, 0, 43, 0.25)' }}
      >
        <CardHeader className="text-center pb-2">
          <CardTitle className="text-4xl font-black text-white tracking-tighter uppercase">
            {winnerName}
          </CardTitle>
          <p className="text-gray-400 text-sm uppercase tracking-widest mt-2">Predicted Winner</p>
        </CardHeader>
      </Card>

      {/* Models Grid */}
      {models && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(models).map(([key, model]) => {
            let modelWinnerName = model.winner;
            let winnerColorClass = 'text-white';

            if (model.winner.includes('Red')) {
              modelWinnerName = result.red_fighter;
              winnerColorClass = 'text-red-500';
            } else if (model.winner.includes('Blue')) {
              modelWinnerName = result.blue_fighter;
              winnerColorClass = 'text-blue-500';
            }

            return (
              <Card 
                key={key} 
                className="border border-[#ff002b]/50 bg-[#00043a]/30"
                style={{ boxShadow: '0 0 15px rgba(255, 0, 43, 0.15)' }}
              >
                <CardHeader className="pb-2">
                  <CardTitle className="text-lg font-bold text-white">{model.name}</CardTitle>
                  <CardDescription className="text-[#ff002b]">{model.accuracy} Accuracy</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-gray-400">Winner:&nbsp;</span>
                    <span className={`font-bold ${winnerColorClass} truncate max-w-[150px] text-right`}>
                      {modelWinnerName}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Confidence:&nbsp;</span>
                    <span className="text-white">{(model.confidence * 100).toFixed(1)}%</span>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      <Tabs defaultValue="stats" className="w-full">
        <TabsList className="grid w-full grid-cols-2 bg-[#00043a]/50 border border-[#ff002b]/30">
          <TabsTrigger value="stats" className="data-[state=active]:bg-[#ff002b] data-[state=active]:text-white">
            <Activity className="w-4 h-4 mr-2" />
            Fighter Comparison
          </TabsTrigger>
          <TabsTrigger value="factors" className="data-[state=active]:bg-[#ff002b] data-[state=active]:text-white">
            <Brain className="w-4 h-4 mr-2" />
            Key Factors
          </TabsTrigger>
        </TabsList>

        <TabsContent value="stats" className="mt-4">
          {/* Fighter Comparison */}
          <Card className="bg-black/50 border-gray-800">
            <CardHeader>
              <CardTitle className="text-lg text-white flex items-center">
                <Activity className="w-4 h-4 mr-2 text-[#ff002b]" />
                Fighter Comparison
              </CardTitle>
            </CardHeader>
        <CardContent className="pt-6">
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                <PolarGrid stroke="#333" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#999', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar
                  name={result.red_fighter}
                  dataKey="A"
                  stroke="#ef4444"
                  fill="#ef4444"
                  fillOpacity={0.3}
                />
                <Radar
                  name={result.blue_fighter}
                  dataKey="B"
                  stroke="#3b82f6"
                  fill="#3b82f6"
                  fillOpacity={0.3}
                />
                <Legend />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#000', border: '1px solid #333' }}
                  itemStyle={{ color: '#fff' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
          
          {/* Tale of the Tape Grid */}
          <div className="grid grid-cols-3 gap-4 mt-6 text-center text-sm">
            <div className="text-red-500 font-bold">{result.red_fighter_stats.age}</div>
            <div className="text-gray-500">Age</div>
            <div className="text-blue-500 font-bold">{result.blue_fighter_stats.age}</div>

            <div className="text-red-500 font-bold">{result.red_fighter_stats.height} cm</div>
            <div className="text-gray-500">Height</div>
            <div className="text-blue-500 font-bold">{result.blue_fighter_stats.height} cm</div>

            <div className="text-red-500 font-bold">{result.red_fighter_stats.reach} cm</div>
            <div className="text-gray-500">Reach</div>
            <div className="text-blue-500 font-bold">{result.blue_fighter_stats.reach} cm</div>
          </div>
        </CardContent>
      </Card>
      </TabsContent>

      <TabsContent value="factors" className="mt-4">
        <Card className="bg-black/50 border-gray-800">
          <CardHeader>
            <CardTitle className="text-lg text-white">Why the AI chose {winnerName}</CardTitle>
          </CardHeader>
          <CardContent>
            {featureData.length > 0 ? (
              <>
                <div className="h-[300px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart layout="vertical" data={featureData} margin={{ left: 20 }}>
                      <XAxis type="number" hide />
                      <YAxis 
                        dataKey="name" 
                        type="category" 
                        width={150} 
                        tick={{ fill: '#999', fontSize: 12 }} 
                      />
                      <Tooltip 
                        cursor={{ fill: 'transparent' }}
                        contentStyle={{ backgroundColor: '#000', border: '1px solid #333' }}
                        itemStyle={{ color: '#ff002b' }}
                      />
                      <Bar dataKey="value" fill="#ff002b" radius={[0, 4, 4, 0]}>
                        {featureData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fillOpacity={0.8} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <p className="text-xs text-gray-500 mt-4 text-center">
                  * Shows the top 5 most influential factors in this prediction
                </p>
              </>
            ) : (
              <div className="flex h-[300px] items-center justify-center text-muted-foreground">
                Feature importance data not available for this model.
              </div>
            )}
          </CardContent>
        </Card>
      </TabsContent>
      </Tabs>
    </div>
  );
}
