'use client';

import Link from "next/link";
import { Zap } from "lucide-react";
import { useState } from "react";

export default function Dashboard() {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <>
      <div 
        className="fixed inset-0 -z-10"
        style={{ 
          backgroundColor: '#00043a',
        }}
      />
      <div className="flex items-center justify-center" style={{ minHeight: '100vh' }}>
        <Link href="/predict">
          <button
            className="group relative px-10 py-5 text-xl font-bold text-white rounded-2xl transition-all duration-300 hover:scale-110 active:scale-95 hover:shadow-[0_0_60px_rgba(255,0,43,0.8),0_0_100px_rgba(255,0,43,0.5)]"
            style={{
              background: 'linear-gradient(135deg, #ff002b 0%, #c00021 100%)',
              boxShadow: '0 0 40px rgba(255, 0, 43, 0.6), 0 0 80px rgba(255, 0, 43, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.2)',
              border: '2px solid rgba(255, 255, 255, 0.3)',
            }}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
          >
            <span className="flex items-center gap-3">
              <Zap className="w-6 h-6" />
              Select Matchup
            </span>
            <div 
              className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              style={{
                background: 'radial-gradient(circle at center, rgba(255, 255, 255, 0.2) 0%, transparent 70%)',
                animation: 'pulse 2s ease-in-out infinite',
              }}
            />
          </button>
        </Link>
      </div>
    </>
  );
}
