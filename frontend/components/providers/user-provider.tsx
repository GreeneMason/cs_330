'use client';

import { ReactNode, useEffect, useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { useQuery } from 'convex/react';
import { api } from '@/convex/_generated/api';
import { ProfileSetup } from '@/components/auth/profile-setup';

export function UserProvider({ children }: { children: ReactNode }) {
  const { user, isLoaded } = useUser();
  const [showProfileSetup, setShowProfileSetup] = useState(false);
  const [profileCheckComplete, setProfileCheckComplete] = useState(false);

  const convexUser = useQuery(
    api.users.getUserByClerkId,
    user ? { clerkId: user.id } : "skip"
  );

  useEffect(() => {
    // Only check once Clerk user is loaded
    if (!isLoaded || !user) {
      setProfileCheckComplete(true);
      return;
    }

    // If query is still loading, wait
    if (convexUser === undefined) {
      return;
    }

    // If user doesn't exist in Convex, show profile setup
    if (convexUser === null) {
      setShowProfileSetup(true);
    }

    setProfileCheckComplete(true);
  }, [isLoaded, user, convexUser]);

  const handleProfileComplete = () => {
    setShowProfileSetup(false);
  };

  // Don't render children until we've checked the user profile status
  if (!profileCheckComplete) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-8 h-8 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin mx-auto" />
          <p className="text-gray-600">Loading your profile...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      {children}
      {showProfileSetup && <ProfileSetup onComplete={handleProfileComplete} />}
    </>
  );
}