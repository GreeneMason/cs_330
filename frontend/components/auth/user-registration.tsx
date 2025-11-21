'use client';

import { useState } from 'react';
import { useSignUp } from '@clerk/nextjs';
import { useMutation } from 'convex/react';
import { api } from '@/convex/_generated/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
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

interface FormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  iconColor: string;
  acceptedTerms: boolean;
}

export function UserRegistration() {
  const { signUp, setActive } = useSignUp();
  const createUser = useMutation(api.users.createUser);
  
  const [formData, setFormData] = useState<FormData>({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    iconColor: ICON_COLORS[0].value,
    acceptedTerms: false,
  });
  
  const [errors, setErrors] = useState<Partial<FormData>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [showVerification, setShowVerification] = useState(false);
  const [verificationCode, setVerificationCode] = useState('');

  const validateForm = (): boolean => {
    const newErrors: Partial<FormData> = {};

    // Username validation
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    } else if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    } else if (!/^[a-zA-Z0-9_]+$/.test(formData.username)) {
      newErrors.username = 'Username can only contain letters, numbers, and underscores';
    }

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      newErrors.password = 'Password must contain uppercase, lowercase, and number';
    }

    // Confirm password validation
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    // Terms validation
    if (!formData.acceptedTerms) {
      newErrors.acceptedTerms = 'You must accept the terms and conditions' as any;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSignUp = async () => {
    if (!validateForm()) return;

    setIsLoading(true);
    try {
      const result = await signUp?.create({
        emailAddress: formData.email,
        password: formData.password,
        username: formData.username,
      });

      if (result) {
        await result.prepareEmailAddressVerification({ strategy: 'email_code' });
        setShowVerification(true);
      }
    } catch (error: any) {
      setErrors({
        email: error.errors?.[0]?.message || 'Failed to create account'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerification = async () => {
    if (!verificationCode.trim()) return;

    setIsLoading(true);
    try {
      const result = await signUp?.attemptEmailAddressVerification({
        code: verificationCode,
      });

      if (result?.status === 'complete') {
        // Create user in Convex database
        await createUser({
          clerkId: result.createdUserId!,
          email: formData.email,
          username: formData.username,
          iconColor: formData.iconColor,
          acceptedTerms: formData.acceptedTerms,
          acceptedTermsAt: Date.now(),
        });

        await setActive({ session: result.createdSessionId });
      }
    } catch (error: any) {
      setErrors({
        email: error.errors?.[0]?.message || 'Invalid verification code'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getInitials = (username: string): string => {
    return username.slice(0, 2).toUpperCase() || 'U';
  };

  if (showVerification) {
    return (
      <Card className="w-full max-w-md mx-auto">
        <CardHeader className="text-center">
          <CardTitle className="flex items-center justify-center space-x-2">
            <User className="h-5 w-5" />
            <span>Verify Email</span>
          </CardTitle>
          <CardDescription>
            Enter the verification code sent to {formData.email}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="verification">Verification Code</Label>
            <Input
              id="verification"
              value={verificationCode}
              onChange={(e) => setVerificationCode(e.target.value)}
              placeholder="Enter 6-digit code"
              maxLength={6}
            />
          </div>

          {errors.email && (
            <div className="flex items-center space-x-2 text-red-600 text-sm">
              <AlertCircle className="h-4 w-4" />
              <span>{errors.email}</span>
            </div>
          )}

          <Button 
            onClick={handleVerification}
            disabled={isLoading || !verificationCode.trim()}
            className="w-full"
          >
            {isLoading ? 'Verifying...' : 'Verify & Create Account'}
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <CardTitle className="flex items-center justify-center space-x-2">
          <User className="h-5 w-5" />
          <span>Create Account</span>
        </CardTitle>
        <CardDescription>
          Join UFC Predictor to track your predictions
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Username */}
        <div>
          <Label htmlFor="username">Username</Label>
          <Input
            id="username"
            value={formData.username}
            onChange={(e) => setFormData(prev => ({ ...prev, username: e.target.value }))}
            placeholder="Choose a unique username"
          />
          {errors.username && (
            <div className="flex items-center space-x-2 text-red-600 text-sm mt-1">
              <AlertCircle className="h-4 w-4" />
              <span>{errors.username}</span>
            </div>
          )}
        </div>

        {/* Email */}
        <div>
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            value={formData.email}
            onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
            placeholder="your@email.com"
          />
          {errors.email && (
            <div className="flex items-center space-x-2 text-red-600 text-sm mt-1">
              <AlertCircle className="h-4 w-4" />
              <span>{errors.email}</span>
            </div>
          )}
        </div>

        {/* Password */}
        <div>
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            value={formData.password}
            onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
            placeholder="Secure password"
          />
          {errors.password && (
            <div className="flex items-center space-x-2 text-red-600 text-sm mt-1">
              <AlertCircle className="h-4 w-4" />
              <span>{errors.password}</span>
            </div>
          )}
        </div>

        {/* Confirm Password */}
        <div>
          <Label htmlFor="confirmPassword">Confirm Password</Label>
          <Input
            id="confirmPassword"
            type="password"
            value={formData.confirmPassword}
            onChange={(e) => setFormData(prev => ({ ...prev, confirmPassword: e.target.value }))}
            placeholder="Repeat password"
          />
          {errors.confirmPassword && (
            <div className="flex items-center space-x-2 text-red-600 text-sm mt-1">
              <AlertCircle className="h-4 w-4" />
              <span>{errors.confirmPassword}</span>
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
          <p className="text-xs text-gray-600 mt-2">
            This will be your profile icon with your initials
          </p>
        </div>

        {/* Terms and Conditions */}
        <div className="flex items-start space-x-2">
          <Checkbox
            id="terms"
            checked={formData.acceptedTerms}
            onCheckedChange={(checked) => 
              setFormData(prev => ({ ...prev, acceptedTerms: !!checked }))
            }
          />
          <Label htmlFor="terms" className="text-sm leading-relaxed">
            I accept the{' '}
            <button type="button" className="text-blue-600 hover:underline">
              Terms of Service
            </button>{' '}
            and{' '}
            <button type="button" className="text-blue-600 hover:underline">
              Privacy Policy
            </button>
          </Label>
        </div>
        {errors.acceptedTerms && (
          <div className="flex items-center space-x-2 text-red-600 text-sm">
            <AlertCircle className="h-4 w-4" />
            <span>{errors.acceptedTerms}</span>
          </div>
        )}

        {/* Preview */}
        {formData.username && (
          <div className="p-3 border rounded-lg bg-gray-50">
            <p className="text-sm font-medium mb-2">Preview:</p>
            <div className="flex items-center space-x-3">
              <div 
                className="w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold"
                style={{ backgroundColor: formData.iconColor }}
              >
                {getInitials(formData.username)}
              </div>
              <div>
                <p className="font-medium">{formData.username}</p>
                <p className="text-xs text-gray-600">{formData.email}</p>
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <Button 
          onClick={handleSignUp}
          disabled={isLoading}
          className="w-full"
        >
          {isLoading ? 'Creating Account...' : 'Create Account'}
        </Button>
      </CardContent>
    </Card>
  );
}