import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BarChart3, TrendingUp, Database } from "lucide-react";

export default function AnalyticsPage() {
  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Analytics & Insights</h1>
            <p className="text-muted-foreground">
              Deep dive into model performance and prediction analytics
            </p>
          </div>
          <Badge className="bg-blue-100 text-blue-800 border-blue-300">
            <BarChart3 className="h-3 w-3 mr-1" />
            Live Data
          </Badge>
        </div>
      </div>

      {/* Coming Soon Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Model Performance Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Track accuracy improvements over time and identify patterns in model performance.
            </p>
            <Badge variant="outline" className="mt-4">Coming Soon</Badge>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="h-5 w-5" />
              Prediction History
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Review past predictions, accuracy rates, and detailed breakdowns by fighter categories.
            </p>
            <Badge variant="outline" className="mt-4">Coming Soon</Badge>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Feature Importance
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Understand which fighter attributes matter most for accurate predictions.
            </p>
            <Badge variant="outline" className="mt-4">Coming Soon</Badge>
          </CardContent>
        </Card>
      </div>

      {/* Placeholder for future charts */}
      <Card>
        <CardHeader>
          <CardTitle>Advanced Analytics Dashboard</CardTitle>
        </CardHeader>
        <CardContent className="h-64 flex items-center justify-center">
          <div className="text-center">
            <BarChart3 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Advanced Analytics Coming Soon</h3>
            <p className="text-muted-foreground">
              We're building comprehensive analytics to help you understand prediction patterns,
              model performance trends, and fighter statistics in depth.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}