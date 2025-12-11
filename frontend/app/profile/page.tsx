import { ProfileDashboard } from '@/components/features/user/profile-dashboard';

export default function ProfilePage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight" style={{ color: '#ffffff' }}>
            My Profile
          </h1>
          <p style={{ color: '#ff002b' }}>
            Manage your account settings and view your prediction stats
          </p>
        </div>
      </div>

      <ProfileDashboard />
    </div>
  );
}