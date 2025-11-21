'use client';

import { useState, useEffect } from 'react';
import { useUser } from '@clerk/nextjs';
import { useMutation, useQuery } from 'convex/react';
import { api } from '@/convex/_generated/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { AlertCircle, User, Palette } from 'lucide-react';
import { cn } from '@/lib/utils';

const ICON_COLORS = [
  { name: 'Blue', value: '#3b82f6', light: '#dbeafe' },
  { name: 'Green', value: '#10b981', light: '#d1fae5' },
  { name: 'Purple', value: '#8b5cf6', light: '#e9d5ff' },
  { name: 'Red', value: '#ef4444', light: '#fee2e2' },
  { name: 'Orange', value: '#f59e0b', light: '#fed7aa' },
  { name: 'Pink', value: '#ec4899', light: '#fce7f3' },
  { name: 'Indigo', value: '#6366f1', light: '#e0e7ff' },
  { name: 'Teal', value: '#14b8a6', light: '#ccfbf1' },
];

interface ProfileSetupData {
  username: string;
  iconColor: string;
}

export function ProfileSetup({ onComplete }: { onComplete: () => void }) {
  const { user } = useUser();
  const createUser = useMutation(api.users.createUser);
  
  const [formData, setFormData] = useState<ProfileSetupData>({
    username: '',
    iconColor: ICON_COLORS[0].value,
  });
  
  const [errors, setErrors] = useState<Partial<ProfileSetupData>>({});
  const [isLoading, setIsLoading] = useState(false);

  // Auto-generate username suggestion from Clerk data
  useEffect(() => {
    if (user && !formData.username) {
      const suggestion = user.firstName 
        ? `${user.firstName.toLowerCase()}${Math.floor(Math.random() * 999)}`
        : `user${Math.floor(Math.random() * 9999)}`;
      setFormData(prev => ({ ...prev, username: suggestion }));
    }
  }, [user, formData.username]);

  const validateUsername = (username: string) => {
    if (!username.trim()) {
      setErrors(prev => ({ ...prev, username: 'Username is required' }));
      return false;
    } 
    
    if (username.length < 3) {
      setErrors(prev => ({ ...prev, username: 'Username must be at least 3 characters' }));
      return false;
    } 
    
    if (!/^[a-zA-Z0-9_]+$/.test(username)) {
      setErrors(prev => ({ ...prev, username: 'Username can only contain letters, numbers, and underscores' }));
      return false;
    }

    setErrors(prev => ({ ...prev, username: undefined }));
    return true;
  };

  const handleUsernameChange = (value: string) => {
    setFormData(prev => ({ ...prev, username: value }));
    // Clear existing errors
    if (errors.username) {
      setErrors(prev => ({ ...prev, username: undefined }));
    }
  };

  const handleSetupComplete = async () => {
    if (!user) return;

    const isValid = validateUsername(formData.username);
    if (!isValid) return;

    setIsLoading(true);
    try {
      await createUser({
        clerkId: user.id,
        email: user.primaryEmailAddress?.emailAddress || '',
        username: formData.username,
        iconColor: formData.iconColor,
        acceptedTerms: true, // Auto-accept for existing users
        acceptedTermsAt: Date.now(),
      });

      onComplete();
    } catch (error: any) {
      setErrors({
        username: error.message || 'Failed to create profile'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getInitials = (username: string): string => {
    return username.slice(0, 2).toUpperCase() || 'U';
  };

  if (!user) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <Card className="w-full max-w-md mx-4">
        <CardHeader className="text-center">
          <CardTitle className="flex items-center justify-center space-x-2">
            <User className="h-5 w-5" />
            <span>Complete Your Profile</span>
          </CardTitle>
          <CardDescription>
            Welcome! Let's set up your UFC Predictor profile
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Username */}
          <div>
            <Label htmlFor="username">Choose a Username</Label>
            <div className="relative">
              <Input
                id="username"
                value={formData.username}
                onChange={(e) => handleUsernameChange(e.target.value)}
                onBlur={() => validateUsername(formData.username)}
                placeholder="Your unique username"
              />
            </div>
            {errors.username && (
              <div className="flex items-center space-x-2 text-red-600 text-sm mt-1">
                <AlertCircle className="h-4 w-4" />
                <span>{errors.username}</span>
              </div>
            )}
          </div>

          {/* Icon Color Selection */}
          <div>
            <Label className="flex items-center space-x-2">
              <Palette className="h-4 w-4" />
              <span>Profile Icon Color</span>
            </Label>
            <div className="grid grid-cols-4 gap-2 mt-2">
              {ICON_COLORS.map((color) => (
                <button
                  key={color.value}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, iconColor: color.value }))}
                  className={cn(
                    "relative p-3 rounded-lg border-2 transition-all hover:scale-105",
                    formData.iconColor === color.value 
                      ? "border-gray-800 shadow-lg" 
                      : "border-gray-200 hover:border-gray-400"
                  )}
                  style={{ backgroundColor: color.light }}
                >
                  <div 
                    className="w-8 h-8 rounded-full mx-auto flex items-center justify-center text-white font-semibold text-sm"
                    style={{ backgroundColor: color.value }}
                  >
                    {getInitials(formData.username)}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Preview */}
          {formData.username && (
            <div className="p-3 border rounded-lg bg-gray-50">
              <p className="text-sm font-medium mb-2">Your Profile Preview:</p>
              <div className="flex items-center space-x-3">
                <div 
                  className="w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold"
                  style={{ backgroundColor: formData.iconColor }}
                >
                  {getInitials(formData.username)}
                </div>
                <div>
                  <p className="font-medium">{formData.username}</p>
                  <p className="text-xs text-gray-600">{user.primaryEmailAddress?.emailAddress}</p>
                </div>
              </div>
            </div>
          )}

          {/* Terms Notice */}
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-800">
              By completing your profile, you agree to our Terms of Service and Privacy Policy.
            </p>
          </div>

          {/* Complete Button */}
          <Button 
            onClick={handleSetupComplete}
            disabled={isLoading || !formData.username || !!errors.username}
            className="w-full"
          >
            {isLoading ? 'Setting up...' : 'Complete Profile'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}