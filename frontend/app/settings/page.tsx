import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Settings, User, Bell } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
            <p className="text-muted-foreground">
              Configure your Fight Predictor experience and preferences
            </p>
          </div>
        </div>
      </div>

      {/* Settings Sections */}
      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5" />
              Account Settings
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Manage your account information, subscription, and billing preferences.
            </p>
            <Badge variant="outline" className="mt-4">Authentication Coming Soon</Badge>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5" />
              Notifications
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Configure notifications for new predictions, model updates, and system alerts.
            </p>
            <Badge variant="outline" className="mt-4">Coming Soon</Badge>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              Model Preferences
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Customize which models to include in predictions and set confidence thresholds.
            </p>
            <Badge variant="outline" className="mt-4">Coming Soon</Badge>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}