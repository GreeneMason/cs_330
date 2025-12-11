'use client';

import { FighterDataMigration } from '@/components/admin/fighter-data-migration';

export default function AdminPage() {
  return (
    <div className="min-h-screen" style={{ backgroundColor: '#00043a' }}>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2" style={{ color: '#ffffff' }}>
            Admin Panel
          </h1>
          <p className="text-lg" style={{ color: '#ff002b' }}>
            Database management and migration tools
          </p>
        </div>

        <div className="space-y-8">
          <FighterDataMigration />
        </div>
      </div>
    </div>
  );
}