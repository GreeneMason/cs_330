'use client';

import { useUser } from '@clerk/nextjs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, XCircle, User } from 'lucide-react';

export function AuthTest() {
  const { isSignedIn, user, isLoaded } = useUser();

  if (!isLoaded) {
    return (
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <User className="h-5 w-5" />
            <span>Authentication Status</span>
          </CardTitle>
          <CardDescription>Loading authentication state...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse">
            <div className="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-gray-300 rounded w-1/2"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <User className="h-5 w-5" />
          <span>Authentication Status</span>
        </CardTitle>
        <CardDescription>Current Clerk authentication state</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium">Signed In:</span>
          <Badge variant={isSignedIn ? "default" : "destructive"} className="flex items-center space-x-1">
            {isSignedIn ? (
              <>
                <CheckCircle className="h-3 w-3" />
                <span>Yes</span>
              </>
            ) : (
              <>
                <XCircle className="h-3 w-3" />
                <span>No</span>
              </>
            )}
          </Badge>
        </div>

        {isSignedIn && user && (
          <>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">User ID:</span>
              <span className="text-sm text-muted-foreground font-mono">
                {user.id.substring(0, 8)}...
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Email:</span>
              <span className="text-sm text-muted-foreground">
                {user.primaryEmailAddress?.emailAddress || 'Not provided'}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Name:</span>
              <span className="text-sm text-muted-foreground">
                {user.fullName || user.firstName || 'Not provided'}
              </span>
            </div>
          </>
        )}

        <div className="pt-4 border-t">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Clerk Status:</span>
            <Badge variant="outline" className="text-green-600 border-green-600">
              <CheckCircle className="h-3 w-3 mr-1" />
              Initialized
            </Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}