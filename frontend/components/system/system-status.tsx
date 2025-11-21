'use client';

import { useEffect, useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { useQuery } from 'convex/react';
import { api } from '@/convex/_generated/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, XCircle, AlertCircle, Server, Database, Shield } from 'lucide-react';

interface SystemStatus {
  backend: boolean;
  convex: boolean;
  clerk: boolean;
}

export function SystemStatus() {
  const { isSignedIn, isLoaded: clerkLoaded } = useUser();
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    backend: false,
    convex: false,
    clerk: false
  });

  // Test Convex connection
  const testConvexQuery = useQuery(api.fighters.listFighters, {});

  // Test backend connection
  useEffect(() => {
    async function testBackend() {
      try {
        const response = await fetch('http://localhost:8000/health');
        setSystemStatus(prev => ({
          ...prev,
          backend: response.ok
        }));
      } catch (error) {
        setSystemStatus(prev => ({
          ...prev,
          backend: false
        }));
      }
    }

    testBackend();
  }, []);

  // Update Convex status based on query
  useEffect(() => {
    setSystemStatus(prev => ({
      ...prev,
      convex: testConvexQuery !== undefined && testConvexQuery !== null
    }));
  }, [testConvexQuery]);

  // Update Clerk status
  useEffect(() => {
    if (clerkLoaded) {
      setSystemStatus(prev => ({
        ...prev,
        clerk: true
      }));
    }
  }, [clerkLoaded]);

  const getStatusIcon = (status: boolean) => {
    return status ? (
      <CheckCircle className="h-4 w-4 text-green-600" />
    ) : (
      <XCircle className="h-4 w-4 text-red-600" />
    );
  };

  const getStatusBadge = (status: boolean, label: string) => {
    return (
      <Badge 
        variant={status ? "default" : "destructive"}
        className="flex items-center space-x-1"
      >
        {getStatusIcon(status)}
        <span>{status ? 'Connected' : 'Disconnected'}</span>
      </Badge>
    );
  };

  const allSystemsGo = Object.values(systemStatus).every(status => status);

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Server className="h-5 w-5" />
          <span>System Status</span>
          {allSystemsGo ? (
            <Badge variant="default" className="ml-2 text-green-600 border-green-600">
              All Systems Go
            </Badge>
          ) : (
            <Badge variant="destructive" className="ml-2">
              Issues Detected
            </Badge>
          )}
        </CardTitle>
        <CardDescription>
          Real-time status of all system components
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Backend API Status */}
        <div className="flex items-center justify-between p-4 border rounded-lg">
          <div className="flex items-center space-x-3">
            <Server className="h-5 w-5 text-blue-600" />
            <div>
              <p className="font-medium">Backend API</p>
              <p className="text-sm text-muted-foreground">Flask server on port 8000</p>
            </div>
          </div>
          {getStatusBadge(systemStatus.backend, 'Backend')}
        </div>

        {/* Convex Database Status */}
        <div className="flex items-center justify-between p-4 border rounded-lg">
          <div className="flex items-center space-x-3">
            <Database className="h-5 w-5 text-purple-600" />
            <div>
              <p className="font-medium">Convex Database</p>
              <p className="text-sm text-muted-foreground">Real-time database connection</p>
            </div>
          </div>
          {getStatusBadge(systemStatus.convex, 'Convex')}
        </div>

        {/* Clerk Authentication Status */}
        <div className="flex items-center justify-between p-4 border rounded-lg">
          <div className="flex items-center space-x-3">
            <Shield className="h-5 w-5 text-green-600" />
            <div>
              <p className="font-medium">Clerk Authentication</p>
              <p className="text-sm text-muted-foreground">
                {isSignedIn ? 'User authenticated' : 'Not signed in'}
              </p>
            </div>
          </div>
          {getStatusBadge(systemStatus.clerk, 'Clerk')}
        </div>

        {/* Debug Info */}
        <div className="pt-4 border-t">
          <details className="cursor-pointer">
            <summary className="text-sm font-medium text-muted-foreground hover:text-foreground">
              Debug Information
            </summary>
            <div className="mt-2 p-3 bg-muted/50 rounded text-xs font-mono space-y-1">
              <div>Backend Health: {systemStatus.backend ? '✓' : '✗'}</div>
              <div>Convex Query: {testConvexQuery ? `${Array.isArray(testConvexQuery) ? testConvexQuery.length : 'loaded'}` : 'loading...'}</div>
              <div>Clerk Loaded: {clerkLoaded ? '✓' : '✗'}</div>
              <div>User Signed In: {isSignedIn ? '✓' : '✗'}</div>
              <div>Environment: {process.env.NODE_ENV}</div>
            </div>
          </details>
        </div>
      </CardContent>
    </Card>
  );
}