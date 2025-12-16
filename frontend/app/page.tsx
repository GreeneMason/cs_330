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
          background: 'radial-gradient(ellipse at center, #1a0000 0%, #000000 100%)',
        }}
      />
      <div className="flex items-center justify-center" style={{ minHeight: '100vh' }}>
        <Link href="/predict">
          <button
            className="group relative px-10 py-5 text-xl font-bold rounded-2xl transition-all duration-300 hover:scale-110 active:scale-95"
            style={{
              background: 'linear-gradient(135deg, #8B0000 0%, #B8860B 50%, #8B0000 100%)',
              color: '#FFD700',
              boxShadow: '0 0 30px rgba(184, 134, 11, 0.4), inset 0 2px 10px rgba(255, 215, 0, 0.2)',
              border: '2px solid #FFD700',
              textShadow: '0 0 10px rgba(255, 215, 0, 0.5)',
            }}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
          >
            <span className="flex items-center gap-3">
              <Zap className="w-6 h-6" style={{ filter: 'drop-shadow(0 0 5px #FFD700)' }} />
              Select Matchup
            </span>
            <div 
              className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 group-hover:animate-pulse"
              style={{
                background: 'radial-gradient(circle at center, rgba(255, 215, 0, 0.3) 0%, transparent 70%)',
                boxShadow: '0 0 80px rgba(184, 134, 11, 1), 0 0 120px rgba(255, 215, 0, 0.6)',
              }}
            />
          </button>
        </Link>
      </div>
    </>
  );
}
