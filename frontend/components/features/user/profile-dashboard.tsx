'use client';

import { useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { useQuery, useMutation } from 'convex/react';
import { api } from '@/convex/_generated/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { User, Palette, BarChart3, Trophy, Calendar, Mail } from 'lucide-react';
import { UserIcon } from '@/components/auth/custom-user-button';

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

export function ProfileDashboard() {
  const { user } = useUser();
  const convexUser = useQuery(
    api.users.getUserByClerkId,
    user ? { clerkId: user.id } : "skip"
  );
  const userStats = useQuery(
    api.users.getUserStats,
    user ? { clerkId: user.id } : "skip"
  );
  const updateUser = useMutation(api.users.updateUser);

  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    username: '',
    iconColor: '',
  });

  const handleEdit = () => {
    if (convexUser) {
      setEditData({
        username: convexUser.username,
        iconColor: convexUser.iconColor,
      });
      setIsEditing(true);
    }
  };

  const handleSave = async () => {
    if (!user || !convexUser) return;

    try {
      await updateUser({
        clerkId: user.id,
        updates: editData,
      });
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update profile:', error);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditData({ username: '', iconColor: '' });
  };

  if (!convexUser || !userStats) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center space-y-4">
          <div className="w-8 h-8 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin mx-auto" />
          <p className="text-gray-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="profile">Profile & Settings</TabsTrigger>
          <TabsTrigger value="stats">Prediction Stats</TabsTrigger>
        </TabsList>

        <TabsContent value="profile" className="space-y-6">
          {/* Profile Overview */}
          <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center space-x-2">
                  <User className="h-5 w-5" style={{ color: '#ff002b' }} />
                  <span>Profile Information</span>
                </CardTitle>
                {!isEditing && (
                  <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={handleEdit}
                    style={{ borderColor: '#ff002b', color: '#ff002b' }}
                  >
                    Edit Profile
                  </Button>
                )}
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {!isEditing ? (
                <>
                  {/* Display Mode */}
                  <div className="flex items-center space-x-4">
                    <UserIcon 
                      username={convexUser.username}
                      iconColor={convexUser.iconColor}
                      size="lg"
                    />
                    <div>
                      <h3 className="text-xl font-semibold" style={{ color: '#ffffff' }}>
                        {convexUser.username}
                      </h3>
                      <p className="text-sm" style={{ color: '#ff002b' }}>
                        {user?.primaryEmailAddress?.emailAddress}
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-3 border rounded-lg" style={{ borderColor: '#ff002b', backgroundColor: '#00043a' }}>
                      <div className="flex items-center space-x-2 mb-2">
                        <Calendar className="h-4 w-4" style={{ color: '#ff002b' }} />
                        <span className="text-sm font-medium">Member Since</span>
                      </div>
                      <p className="text-sm" style={{ color: '#ffffff' }}>
                        {new Date(convexUser.createdAt).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="p-3 border rounded-lg" style={{ borderColor: '#ff002b', backgroundColor: '#00043a' }}>
                      <div className="flex items-center space-x-2 mb-2">
                        <Mail className="h-4 w-4" style={{ color: '#ff002b' }} />
                        <span className="text-sm font-medium">Email Verified</span>
                      </div>
                      <Badge style={{ backgroundColor: '#10b981', color: '#ffffff' }}>
                        Verified
                      </Badge>
                    </div>
                  </div>
                </>
              ) : (
                <>
                  {/* Edit Mode */}
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="edit-username" style={{ color: '#ffffff' }}>Username</Label>
                      <Input
                        id="edit-username"
                        value={editData.username}
                        onChange={(e) => setEditData(prev => ({ ...prev, username: e.target.value }))}
                        style={{ backgroundColor: '#00043a', borderColor: '#ff002b', color: '#ffffff' }}
                      />
                    </div>

                    <div>
                      <Label style={{ color: '#ffffff' }}>Icon Color</Label>
                      <div className="grid grid-cols-4 gap-2 mt-2">
                        {ICON_COLORS.map((color) => (
                          <button
                            key={color.value}
                            type="button"
                            onClick={() => setEditData(prev => ({ ...prev, iconColor: color.value }))}
                            className={`relative p-3 rounded-lg border-2 transition-all hover:scale-105 ${
                              editData.iconColor === color.value 
                                ? "border-[#ff002b] shadow-lg" 
                                : "border-gray-600 hover:border-gray-400"
                            }`}
                            style={{ backgroundColor: color.light }}
                          >
                            <div 
                              className="w-8 h-8 rounded-full mx-auto flex items-center justify-center text-white font-semibold text-sm"
                              style={{ backgroundColor: color.value }}
                            >
                              {editData.username.slice(0, 2).toUpperCase() || 'U'}
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="flex space-x-2 pt-4">
                      <Button 
                        onClick={handleSave}
                        style={{ backgroundColor: '#ff002b', color: '#ffffff' }}
                      >
                        Save Changes
                      </Button>
                      <Button 
                        variant="outline" 
                        onClick={handleCancel}
                        style={{ borderColor: '#ff002b', color: '#ff002b' }}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="stats" className="space-y-6">
          {/* Prediction Statistics */}
          <div className="grid gap-4 md:grid-cols-3">
            <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Predictions</CardTitle>
                <BarChart3 className="h-4 w-4" style={{ color: '#ff002b' }} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{userStats.stats.totalPredictions}</div>
                <p className="text-xs text-muted-foreground">All time</p>
              </CardContent>
            </Card>

            <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Accuracy Rate</CardTitle>
                <Trophy className="h-4 w-4" style={{ color: '#ff002b' }} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{userStats.stats.accuracy}%</div>
                <p className="text-xs text-muted-foreground">
                  {userStats.stats.correctPredictions}/{userStats.stats.totalPredictions} correct
                </p>
              </CardContent>
            </Card>

            <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Rank</CardTitle>
                <User className="h-4 w-4" style={{ color: '#ff002b' }} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {userStats.stats.totalPredictions > 0 ? 'Active' : 'Rookie'}
                </div>
                <p className="text-xs text-muted-foreground">Prediction status</p>
              </CardContent>
            </Card>
          </div>

          {/* Coming Soon: Detailed Stats */}
          <Card style={{ background: '#002962', color: '#ffffff', border: '1px solid #ff002b' }}>
            <CardHeader>
              <CardTitle>Prediction History</CardTitle>
              <CardDescription style={{ color: '#ff002b' }}>
                Your detailed prediction analytics and history
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Trophy className="h-12 w-12 mx-auto mb-4" style={{ color: '#ff002b' }} />
                <h3 className="text-lg font-medium mb-2">Coming Soon</h3>
                <p className="text-sm text-muted-foreground">
                  Detailed prediction history and analytics will be available once you start making predictions!
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}