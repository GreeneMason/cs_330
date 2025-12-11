'use client';

import Link from "next/link";
import { Activity, BarChart3, Settings, Trophy, Zap, Terminal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { SignInButton, SignedIn, SignedOut, useUser } from '@clerk/nextjs';
import { CustomUserButton } from '@/components/auth/custom-user-button';

export function Header() {
  const { user } = useUser();
  const isDevUser = user?.primaryEmailAddress?.emailAddress === 'masonmgreene@gmail.com';

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
        <div className="flex items-center space-x-4 bg-[#00043a]/40 px-4 py-2 rounded-full border border-[#ff002b]/30 backdrop-blur-md">
          <div className="flex items-center space-x-2">
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-[#ff002b]">
              Predictr
            </h1>
            <Badge  
              variant="secondary" 
              className="text-xs"
              style={{ 
                backgroundColor: '#ff002b', 
                color: '#ffffff',
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
            background: 'linear-gradient(180deg, rgba(0, 78, 137, 0.2) 0%, rgba(0, 4, 58, 0.2) 100%)',
            backdropFilter: 'blur(8px)',
            border: 'none',
            boxShadow: '0 2px 10px rgba(0,4,58,0.1)'
          }}>
            <Link 
              href="/" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <span>Home</span>
            </Link>
          </Button>
          
          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(180deg, rgba(0, 78, 137, 0.2) 0%, rgba(0, 4, 58, 0.2) 100%)',
            backdropFilter: 'blur(8px)',
            border: 'none',
            boxShadow: '0 2px 10px rgba(0,4,58,0.1)'
          }}>
            <Link 
              href="/predict" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <span>Predict</span>
            </Link>
          </Button>

          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(180deg, rgba(0, 78, 137, 0.2) 0%, rgba(0, 4, 58, 0.2) 100%)',
            backdropFilter: 'blur(8px)',
            border: 'none',
            boxShadow: '0 2px 10px rgba(0,4,58,0.1)'
          }}>
            <Link 
              href="/predictions" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <span>My Predictions</span>
            </Link>
          </Button>
          
          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(180deg, rgba(0, 78, 137, 0.2) 0%, rgba(0, 4, 58, 0.2) 100%)',
            backdropFilter: 'blur(8px)',
            border: 'none',
            boxShadow: '0 2px 10px rgba(0,4,58,0.1)'
          }}>
            <Link 
              href="/profile" 
              className="flex items-center space-x-2"
              style={{ color: '#ffffff' }}
            >
              <span>Profile</span>
            </Link>
          </Button>

          {isDevUser && (
            <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
              background: 'linear-gradient(180deg, rgba(192, 0, 33, 0.2) 0%, rgba(0, 4, 58, 0.2) 100%)',
              backdropFilter: 'blur(8px)',
              border: 'none',
              boxShadow: '0 2px 10px rgba(192, 0, 33, 0.1)'
            }}>
              <Link 
                href="/dev-mode" 
                className="flex items-center space-x-2"
                style={{ color: '#ffffff' }}
              >
                <span>Dev Mode</span>
              </Link>
            </Button>
          )}
        </nav>

        {/* Status Badge and User Authentication */}
        <div className="flex items-center space-x-4 bg-[#00043a]/40 px-4 py-2 rounded-full border border-[#ff002b]/30 backdrop-blur-md">
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
                    borderColor: '#ff002b', 
                    color: '#ff002b',
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
            style={{ backgroundColor: '#ff002b', border: 'none' }}
          >
            <div 
              className="h-2 w-2 rounded-full mr-1 animate-pulse"
              style={{ backgroundColor: '#c00021' }}
            ></div>
            Models Ready
          </Badge>
        </div>
      </div>
    </header>
  );
}