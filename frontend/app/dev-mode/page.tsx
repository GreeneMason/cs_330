'use client';

import { useUser } from '@clerk/nextjs';
import { SystemStatus } from "@/components/system/system-status";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, AlertTriangle } from "lucide-react";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function DevModePage() {
  const { user, isLoaded } = useUser();
  const router = useRouter();
  const [isAuthorized, setIsAuthorized] = useState(false);

  useEffect(() => {
    if (isLoaded) {
      const primaryEmail = user?.primaryEmailAddress?.emailAddress;
      if (primaryEmail === 'masonmgreene@gmail.com') {
        setIsAuthorized(true);
      } else {
        // Redirect unauthorized users
        router.push('/');
      }
    }
  }, [isLoaded, user, router]);

  if (!isLoaded || !isAuthorized) {
    return (
      <>
        <div 
          className="fixed inset-0 -z-10"
          style={{ 
            backgroundColor: '#000000', 
            backgroundImage: 'radial-gradient(circle at 50% 0%, rgba(60, 60, 60, 0.4) 0%, transparent 60%)',
          }}
        />
        <div className="flex items-center justify-center min-h-screen">
          <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
            <CardContent className="p-6">
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" style={{ color: '#ff002b' }} />
                <p>Checking authorization...</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </>
    );
  }

  return (
    <>
      <div 
        className="fixed inset-0 -z-10"
        style={{ 
          backgroundColor: '#00043a', 
          backgroundImage: 'radial-gradient(circle at 50% 0%, rgba(0, 78, 137, 0.4) 0%, transparent 60%)',
        }}
      />
      <div className="space-y-8" style={{ minHeight: '100vh', padding: '20px' }}>
        {/* Header */}
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight" style={{ color: '#ffffff' }}>
                Developer Mode
              </h1>
              <p style={{ color: '#ff002b' }}>
                System monitoring and diagnostics
              </p>
            </div>
            <Badge style={{ 
              backgroundColor: '#c00021', 
              color: '#ffffff',
              border: 'none'
            }}>
              Admin Only
            </Badge>
          </div>
        </div>

        {/* System Status Check */}
        <SystemStatus />

        {/* System Status Details */}
        <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2" style={{ color: '#ffffff' }}>
              <TrendingUp className="h-5 w-5" style={{ color: '#ff002b' }} />
              System Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <div className="flex items-center justify-between p-4 border rounded-lg" style={{ 
                borderColor: '#ff002b',
                backgroundColor: '#00043a'
              }}>
                <div>
                  <p className="text-sm font-medium" style={{ color: '#ffffff' }}>Ensemble Model</p>
                  <p className="text-xs" style={{ color: '#ff002b' }}>4 models active</p>
                </div>
                <Badge style={{ 
                  backgroundColor: '#ff002b', 
                  color: '#ffffff',
                  border: 'none'
                }}>
                  Ready
                </Badge>
              </div>
              <div className="flex items-center justify-between p-4 border rounded-lg" style={{ 
                borderColor: '#ff002b',
                backgroundColor: '#00043a'
              }}>
                <div>
                  <p className="text-sm font-medium" style={{ color: '#ffffff' }}>Data Pipeline</p>
                  <p className="text-xs" style={{ color: '#ff002b' }}>5,951 training samples</p>
                </div>
                <Badge style={{ 
                  backgroundColor: '#ff002b', 
                  color: '#ffffff',
                  border: 'none'
                }}>
                  Updated
                </Badge>
              </div>
              <div className="flex items-center justify-between p-4 border rounded-lg" style={{ 
                borderColor: '#ff002b',
                backgroundColor: '#00043a'
              }}>
                <div>
                  <p className="text-sm font-medium" style={{ color: '#ffffff' }}>Predictions</p>
                  <p className="text-xs" style={{ color: '#ff002b' }}>Real-time inference</p>
                </div>
                <Badge style={{ 
                  backgroundColor: '#ff002b', 
                  color: '#ffffff',
                  border: 'none'
                }}>
                  Active
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
