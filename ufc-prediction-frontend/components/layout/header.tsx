import Link from "next/link";
import { Activity, BarChart3, Settings, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function Header() {
  return (
    <header 
      className="sticky top-0 z-50 w-full border-b backdrop-blur supports-[backdrop-filter]:bg-background/60"
      style={{ 
        backgroundColor: '#14213d', 
        borderBottomColor: '#fca311' 
      }}
    >
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        {/* Logo and Title */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Zap className="h-6 w-6" style={{ color: '#fca311' }} />
            <h1 className="text-xl font-bold" style={{ color: '#ffffff' }}>
              UFC Predictor
            </h1>
            <Badge 
              variant="secondary" 
              className="text-xs"
              style={{ 
                backgroundColor: '#f1c47b', 
                color: '#0a111f',
                border: 'none' 
              }}
            >
              AI-Powered
            </Badge>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex items-center space-x-1">
          <Button variant="ghost" size="sm" asChild>
            <Link 
              href="/" 
              className="flex items-center space-x-2 hover:bg-opacity-20"
              style={{ color: '#ffffff' }}
            >
              <Activity className="h-4 w-4" />
              <span>Dashboard</span>
            </Link>
          </Button>
          
          <Button variant="ghost" size="sm" asChild>
            <Link 
              href="/predict" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <Zap className="h-4 w-4" />
              <span>Predict</span>
            </Link>
          </Button>
          
          <Button variant="ghost" size="sm" asChild>
            <Link 
              href="/analytics" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <BarChart3 className="h-4 w-4" />
              <span>Analytics</span>
            </Link>
          </Button>
          
          <Button variant="ghost" size="sm" asChild>
            <Link 
              href="/settings" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <Settings className="h-4 w-4" />
              <span>Settings</span>
            </Link>
          </Button>
        </nav>

        {/* Status Badge */}
        <div className="flex items-center space-x-2">
          <Badge 
            className="text-white"
            style={{ backgroundColor: '#fca311', border: 'none' }}
          >
            <div 
              className="h-2 w-2 rounded-full mr-1 animate-pulse"
              style={{ backgroundColor: '#f1c47b' }}
            ></div>
            Models Ready
          </Badge>
        </div>
      </div>
    </header>
  );
}