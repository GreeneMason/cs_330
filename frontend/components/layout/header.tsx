import Link from "next/link";
import { Activity, BarChart3, Settings, Trophy, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { SignInButton, SignedIn, SignedOut } from '@clerk/nextjs';
import { CustomUserButton } from '@/components/auth/custom-user-button';

export function Header() {
  return (
    <header 
      className="sticky top-0 z-50 w-full backdrop-blur-sm"
      style={{ 
        background: 'transparent',
        border: 'none'
      }}
    >
      <div className="container mx-auto flex h-16 items-center justify-between px-4 mt-2">
        {/* Logo and Title */}
        <div className="flex items-center space-x-4 bg-black/40 px-4 py-2 rounded-full border border-[#fca311]/30 backdrop-blur-md">
          <div className="flex items-center space-x-2">
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-[#fca311]">
              Fight Predictor
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
        <nav className="flex items-center space-x-2">
          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(180deg, rgba(20, 33, 61, 0.2) 0%, rgba(0, 0, 0, 0.2) 100%)',
            backdropFilter: 'blur(8px)',
            border: 'none',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
          }}>
            <Link 
              href="/" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <Activity className="h-4 w-4 text-[#fca311]" />
              <span>Dashboard</span>
            </Link>
          </Button>
          
          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(180deg, rgba(20, 33, 61, 0.2) 0%, rgba(0, 0, 0, 0.2) 100%)',
            backdropFilter: 'blur(8px)',
            border: 'none',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
          }}>
            <Link 
              href="/predict" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <Zap className="h-4 w-4 text-[#fca311]" />
              <span>Predict</span>
            </Link>
          </Button>

          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(180deg, rgba(20, 33, 61, 0.2) 0%, rgba(0, 0, 0, 0.2) 100%)',
            backdropFilter: 'blur(8px)',
            border: 'none',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
          }}>
            <Link 
              href="/predictions" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <Trophy className="h-4 w-4 text-[#fca311]" />
              <span>My Predictions</span>
            </Link>
          </Button>
          
          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(180deg, rgba(20, 33, 61, 0.2) 0%, rgba(0, 0, 0, 0.2) 100%)',
            backdropFilter: 'blur(8px)',
            border: 'none',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
          }}>
            <Link 
              href="/analytics" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <BarChart3 className="h-4 w-4 text-[#fca311]" />
              <span>Analytics</span>
            </Link>
          </Button>
          
          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(180deg, rgba(20, 33, 61, 0.2) 0%, rgba(0, 0, 0, 0.2) 100%)',
            backdropFilter: 'blur(8px)',
            border: 'none',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
          }}>
            <Link 
              href="/profile" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <Settings className="h-4 w-4 text-[#fca311]" />
              <span>Profile</span>
            </Link>
          </Button>
        </nav>

        {/* Status Badge and User Authentication */}
        <div className="flex items-center space-x-4 bg-black/40 px-4 py-2 rounded-full border border-[#fca311]/30 backdrop-blur-md">
          {/* Authentication */}
          <SignedOut>
            <div className="flex items-center space-x-2">
              <Button 
                variant="ghost" 
                size="sm" 
                asChild
                style={{ color: '#ffffff' }}
                className="hover:bg-opacity-20"
              >
                <Link href="/register">
                  Create Account
                </Link>
              </Button>
              <SignInButton>
                <Button 
                  variant="outline" 
                  size="sm"
                  style={{ 
                    borderColor: '#fca311', 
                    color: '#fca311',
                    backgroundColor: 'transparent'
                  }}
                  className="hover:bg-opacity-10"
                >
                  Sign In
                </Button>
              </SignInButton>
            </div>
          </SignedOut>
          <SignedIn>
            <CustomUserButton />
          </SignedIn>

          {/* Status Badge */}
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