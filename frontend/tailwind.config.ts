import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // UFC Fight Predictor Brand Colors
        'ufc': {
          'black': '#000000',
          'rich-black': '#0a111f',
          'oxford-blue': '#14213d',
          'golden-brown': '#886227',
          'orange': '#fca311',
          'sunset': '#f1c47b',
          'platinum': '#e5e5e5',
          'white-smoke': '#f2f2f2',
          'white': '#ffffff',
        },
        // Semantic color mappings
        'brand': {
          'primary': '#fca311',      // Orange Web
          'secondary': '#886227',    // Golden Brown
          'accent': '#f1c47b',       // Sunset
          'dark': '#0a111f',         // Rich Black
          'darker': '#14213d',       // Oxford Blue
          'light': '#f2f2f2',        // White Smoke
          'lighter': '#e5e5e5',      // Platinum
        },
        // Chart colors for data visualization
        'chart': {
          '1': '#fca311',  // Orange Web
          '2': '#886227',  // Golden Brown
          '3': '#14213d',  // Oxford Blue
          '4': '#f1c47b',  // Sunset
          '5': '#0a111f',  // Rich Black
        },
        // Status colors
        'status': {
          'success': '#fca311',    // Orange Web
          'warning': '#886227',    // Golden Brown
          'info': '#14213d',       // Oxford Blue
          'neutral': '#e5e5e5',    // Platinum
        }
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-geist-mono)", "monospace"],
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-in": "fadeIn 0.5s ease-in-out",
        "slide-up": "slideUp 0.3s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
} satisfies Config;