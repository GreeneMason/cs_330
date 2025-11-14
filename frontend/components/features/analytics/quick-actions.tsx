import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Zap, BarChart3, RefreshCw, Settings } from "lucide-react";

export function QuickActions() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Button asChild size="lg" className="h-20 flex-col gap-2">
            <Link href="/predict">
              <Zap className="h-6 w-6" />
              <span>Make Prediction</span>
            </Link>
          </Button>
          
          <Button asChild variant="outline" size="lg" className="h-20 flex-col gap-2">
            <Link href="/analytics">
              <BarChart3 className="h-6 w-6" />
              <span>View Analytics</span>
            </Link>
          </Button>
          
          <Button variant="outline" size="lg" className="h-20 flex-col gap-2">
            <RefreshCw className="h-6 w-6" />
            <span>Refresh Data</span>
          </Button>
          
          <Button asChild variant="outline" size="lg" className="h-20 flex-col gap-2">
            <Link href="/settings">
              <Settings className="h-6 w-6" />
              <span>Settings</span>
            </Link>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}