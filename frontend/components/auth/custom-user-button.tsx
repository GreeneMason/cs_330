'use client';

import { useUser } from '@clerk/nextjs';
import { useQuery } from 'convex/react';
import { api } from '@/convex/_generated/api';
import { UserButton as ClerkUserButton } from '@clerk/nextjs';

interface UserIconProps {
  username: string;
  iconColor: string;
  size?: 'sm' | 'md' | 'lg';
}

export function UserIcon({ username, iconColor, size = 'md' }: UserIconProps) {
  const sizeClasses = {
    sm: 'w-6 h-6 text-xs',
    md: 'w-8 h-8 text-sm',
    lg: 'w-12 h-12 text-base'
  };

  const getInitials = (name: string): string => {
    return name.slice(0, 2).toUpperCase() || 'U';
  };

  return (
    <div 
      className={`${sizeClasses[size]} rounded-full flex items-center justify-center text-white font-semibold`}
      style={{ backgroundColor: iconColor }}
    >
      {getInitials(username)}
    </div>
  );
}

export function CustomUserButton() {
  const { user, isLoaded } = useUser();
  const convexUser = useQuery(
    api.users.getUserByClerkId, 
    user ? { clerkId: user.id } : "skip"
  );

  if (!isLoaded || !user) {
    return <ClerkUserButton />;
  }

  // If we have custom user data from Convex, show custom icon
  if (convexUser) {
    return (
      <div className="relative w-8 h-8">
        <div className="absolute inset-0 z-0 pointer-events-none">
          <UserIcon 
            username={convexUser.username} 
            iconColor={convexUser.iconColor}
            size="md"
          />
        </div>
        <div className="relative z-10 opacity-0 w-full h-full">
          <ClerkUserButton 
            appearance={{
              elements: {
                rootBox: "w-full h-full",
                userButtonTrigger: "w-full h-full",
                avatarBox: "w-full h-full"
              }
            }}
          />
        </div>
      </div>
    );
  }

  // Fallback to default Clerk UserButton
  return (
    <ClerkUserButton 
      appearance={{
        elements: {
          avatarBox: "h-8 w-8",
          userButtonPopoverCard: "bg-slate-800 border border-orange-400",
          userButtonPopoverActionButton: "text-white hover:bg-slate-700"
        }
      }}
    />
  );
}