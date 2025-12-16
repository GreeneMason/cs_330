import Link from "next/link";
import { ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Footer() {
  return (
    <footer 
      className="w-full backdrop-blur-sm mt-auto"
      style={{ 
        background: 'linear-gradient(180deg, transparent 0%, rgba(0, 4, 58, 0.6) 100%)',
        borderTop: '1px solid rgba(255, 0, 43, 0.2)'
      }}
    >
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          {/* Left side - Branding */}
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium" style={{ color: '#ffffff' }}>
              Predictr
            </span>
            <span className="text-xs" style={{ color: '#ff002b' }}>
              © 2025
            </span>
          </div>

          {/* Center - Description */}
          <div className="text-center">
            <p className="text-xs" style={{ color: '#ffffff', opacity: 0.7 }}>
              AI-Powered UFC Fight Predictions
            </p>
            <p className="text-xs mt-1" style={{ color: '#ffffff', opacity: 0.5 }}>
              Training Data: January 1993 - December 2025
            </p>
          </div>

          {/* Right side - Meet the Dev button */}
          <Link href="https://masongreene.dev" target="_blank" rel="noopener noreferrer">
            <Button
              variant="outline"
              size="sm"
              className="group rounded-full transition-all duration-300 hover:scale-105"
              style={{
                background: 'linear-gradient(135deg, rgba(255, 0, 43, 0.1) 0%, rgba(0, 78, 137, 0.1) 100%)',
                borderColor: '#ff002b',
                color: '#ffffff',
                backdropFilter: 'blur(8px)'
              }}
            >
              <span className="flex items-center gap-2">
                Meet the Dev
                <ExternalLink className="h-3 w-3 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
              </span>
            </Button>
          </Link>
        </div>
      </div>
    </footer>
  );
}
