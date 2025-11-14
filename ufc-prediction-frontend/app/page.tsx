import { DashboardMetrics } from "@/components/features/analytics/dashboard-metrics";
import { ModelPerformanceChart, ModelWeightsChart } from "@/components/features/analytics/model-performance-charts";
import { QuickActions } from "@/components/features/analytics/quick-actions";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, Zap } from "lucide-react";

export default function Dashboard() {
  return (
    <div className="space-y-8" style={{ backgroundColor: '#000000', minHeight: '100vh', padding: '20px' }}>
      {/* Welcome Section */}
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight" style={{ color: '#ffffff' }}>
              UFC Fight Predictor
            </h1>
            <p style={{ color: '#fca311' }}>
              Advanced AI ensemble achieving 91.33% prediction accuracy
            </p>
          </div>
          <Badge style={{ 
            backgroundColor: '#fca311', 
            color: '#000000',
            border: 'none'
          }}>
            <Zap className="h-3 w-3 mr-1" />
            Models Active
          </Badge>
        </div>
      </div>

      {/* Performance Metrics */}
      <DashboardMetrics />

      {/* Charts Section */}
      <div className="grid gap-6 md:grid-cols-2">
        <ModelPerformanceChart />
        <ModelWeightsChart />
      </div>

      {/* System Status */}
      <Card style={{ background: '#14213d', color: '#ffffff', border: '1px solid #fca311' }}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2" style={{ color: '#ffffff' }}>
            <TrendingUp className="h-5 w-5" style={{ color: '#fca311' }} />
            System Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="flex items-center justify-between p-4 border rounded-lg" style={{ 
              borderColor: '#fca311',
              backgroundColor: '#000000'
            }}>
              <div>
                <p className="text-sm font-medium" style={{ color: '#ffffff' }}>Ensemble Model</p>
                <p className="text-xs" style={{ color: '#fca311' }}>4 models active</p>
              </div>
              <Badge style={{ 
                backgroundColor: '#fca311', 
                color: '#000000',
                border: 'none'
              }}>
                Ready
              </Badge>
            </div>
            <div className="flex items-center justify-between p-4 border rounded-lg" style={{ 
              borderColor: '#fca311',
              backgroundColor: '#000000'
            }}>
              <div>
                <p className="text-sm font-medium" style={{ color: '#ffffff' }}>Data Pipeline</p>
                <p className="text-xs" style={{ color: '#fca311' }}>5,951 training samples</p>
              </div>
              <Badge style={{ 
                backgroundColor: '#fca311', 
                color: '#000000',
                border: 'none'
              }}>
                Updated
              </Badge>
            </div>
            <div className="flex items-center justify-between p-4 border rounded-lg" style={{ 
              borderColor: '#fca311',
              backgroundColor: '#000000'
            }}>
              <div>
                <p className="text-sm font-medium" style={{ color: '#ffffff' }}>Predictions</p>
                <p className="text-xs" style={{ color: '#fca311' }}>Real-time inference</p>
              </div>
              <Badge style={{ 
                backgroundColor: '#fca311', 
                color: '#000000',
                border: 'none'
              }}>
                Active
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <QuickActions />
    </div>
  );
}
