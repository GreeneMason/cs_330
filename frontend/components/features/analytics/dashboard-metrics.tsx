import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, Target, Database, Clock } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string;
  description?: string;
  trend?: "up" | "down" | "neutral";
  icon?: React.ReactNode;
  cardStyle?: React.CSSProperties;
}

export function MetricCard({ title, value, description, trend, icon, cardStyle }: MetricCardProps) {
  return (
    <Card style={cardStyle}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium" style={cardStyle ? { color: 'inherit' } : undefined}>
          {title}
        </CardTitle>
        {icon && <div style={cardStyle ? { color: 'inherit', opacity: 0.8 } : undefined}>{icon}</div>}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold" style={cardStyle ? { color: 'inherit' } : undefined}>
          {value}
        </div>
        {description && (
          <p className="text-xs mt-1" style={cardStyle ? { color: 'inherit', opacity: 0.8 } : undefined}>
            {description}
          </p>
        )}
        {trend && (
          <div className="flex items-center mt-1">
            <TrendingUp className={`h-3 w-3 mr-1`} style={{
              color: cardStyle?.color === '#000000' ? '#002962' : '#ff002b'
            }} />
            <span className={`text-xs`} style={{
              color: cardStyle?.color === '#000000' ? '#002962' : '#ff002b'
            }}>
              {trend === "up" ? "Improving" : trend === "down" ? "Declining" : "Stable"}
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function DashboardMetrics() {
  // This data would normally come from your Convex backend
  // For now, we'll use the known ensemble performance data
  const metrics = {
    ensembleAccuracy: "91.33%",
    aucScore: "0.9724",
    trainingDate: "Nov 13, 2025",
    totalFeatures: 90,
    trainingFights: "5,951",
    modelsCount: 4
  };

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <MetricCard
        title="Ensemble Accuracy"
        value={metrics.ensembleAccuracy}
        description="Best performing model combination"
        trend="up"
        icon={<Target className="h-4 w-4" style={{ color: '#00043a' }} />}
        cardStyle={{ 
          background: '#ff002b',
          color: '#ffffff'
        }}
      />
      
      <MetricCard
        title="AUC Score"
        value={metrics.aucScore}
        description="Area under ROC curve"
        trend="up"
        icon={<TrendingUp className="h-4 w-4" style={{ color: '#ff002b' }} />}
        cardStyle={{ 
          background: '#002962',
          color: '#ffffff'
        }}
      />
      
      <MetricCard
        title="Training Data"
        value={metrics.trainingFights}
        description={`${metrics.totalFeatures} features analyzed`}
        icon={<Database className="h-4 w-4" style={{ color: '#000000' }} />}
        cardStyle={{ 
          background: '#ffffff',
          color: '#000000'
        }}
      />
      
      <MetricCard
        title="Last Updated"
        value={metrics.trainingDate}
        description={`${metrics.modelsCount} models active`}
        icon={<Clock className="h-4 w-4" style={{ color: '#ff002b' }} />}
        cardStyle={{ 
          background: '#00043a',
          color: '#ffffff',
          border: '1px solid #ff002b'
        }}
      />
    </div>
  );
}