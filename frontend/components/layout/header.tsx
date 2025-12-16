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
        <div className="flex items-center space-x-4 px-4 py-2 rounded-full backdrop-blur-md" style={{
          background: 'linear-gradient(135deg, #0B5345 0%, #064635 100%)',
          border: '1px solid #FFD700',
          boxShadow: '0 0 20px rgba(184, 134, 11, 0.3)'
        }}>
          <div className="flex items-center space-x-2">
            <h1 className="text-xl font-bold" style={{
              color: '#FFD700',
              textShadow: '0 0 10px rgba(255, 215, 0, 0.5)'
            }}>
              Predictr
            </h1>
            <Badge  
              variant="secondary" 
              className="text-xs"
              style={{ 
                background: 'linear-gradient(135deg, #B8860B 0%, #FFD700 100%)',
                color: '#000000',
                border: 'none',
                fontWeight: 'bold'
              }}
            >
              AI-Powered
            </Badge>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex items-center space-x-2">
          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(135deg, #8B0000 0%, #000000 100%)',
            backdropFilter: 'blur(8px)',
            border: '1px solid #B8860B',
            boxShadow: '0 2px 10px rgba(184, 134, 11, 0.2)'
          }}>
            <Link 
              href="/" 
              className="flex items-center space-x-2"
              style={{ color: '#FFD700' }}
            >
              <span>Home</span>
            </Link>
          </Button>
          
          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(135deg, #064635 0%, #032D23 100%)',
            backdropFilter: 'blur(8px)',
            border: '1px solid #B8860B',
            boxShadow: '0 2px 10px rgba(184, 134, 11, 0.2)'
          }}>
            <Link 
              href="/predict" 
              className="flex items-center space-x-2"
              style={{ color: '#FFD700' }}
            >
              <span>Predict</span>
            </Link>
          </Button>

          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(135deg, #064635 0%, #032D23 100%)',
            backdropFilter: 'blur(8px)',
            border: '1px solid #B8860B',
            boxShadow: '0 2px 10px rgba(184, 134, 11, 0.2)'
          }}>
            <Link 
              href="/predictions" 
              className="flex items-center space-x-2"
              style={{ color: '#FFD700' }}
            >
              <span>My Predictions</span>
            </Link>
          </Button>
          
          <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
            background: 'linear-gradient(135deg, #064635 0%, #032D23 100%)',
            backdropFilter: 'blur(8px)',
            border: '1px solid #B8860B',
            boxShadow: '0 2px 10px rgba(184, 134, 11, 0.2)'
          }}>
            <Link 
              href="/profile" 
              className="flex items-center space-x-2"
              style={{ color: '#FFD700' }}
            >
              <span>Profile</span>
            </Link>
          </Button>

          {isDevUser && (
            <Button variant="ghost" size="sm" asChild className="rounded-full transition-all hover:scale-105" style={{
              background: 'linear-gradient(135deg, #064635 0%, #032D23 100%)',
              backdropFilter: 'blur(8px)',
              border: '1px solid #B8860B',
              boxShadow: '0 2px 10px rgba(184, 134, 11, 0.2)'
            }}>
              <Link 
                href="/dev-mode" 
                className="flex items-center space-x-2"
                style={{ color: '#FFD700' }}
              >
                <span>Dev Mode</span>
              </Link>
            </Button>
          )}
        </nav>

        {/* Status Badge and User Authentication */}
        <div className="flex items-center space-x-4 px-4 py-2 rounded-full backdrop-blur-md" style={{
          background: 'linear-gradient(135deg, #0B5345 0%, #064635 100%)',
          border: '1px solid #FFD700',
          boxShadow: '0 0 20px rgba(184, 134, 11, 0.3)'
        }}>
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
                    borderColor: '#FFD700', 
                    color: '#FFD700',
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
            className="text-black font-bold"
            style={{ 
              background: 'linear-gradient(135deg, #B8860B 0%, #FFD700 100%)',
              border: 'none'
            }}
          >
            <div 
              className="h-2 w-2 rounded-full mr-1 animate-pulse"
              style={{ backgroundColor: '#228B22' }}
            ></div>
            Models Ready
          </Badge>
        </div>
      </div>
    </header>
  );
}