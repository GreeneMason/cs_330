import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ClerkProvider } from '@clerk/nextjs';
import { ConvexClientProvider } from '@/components/providers/convex-provider';
import { UserProvider } from '@/components/providers/user-provider';
import { Header } from "@/components/layout/header";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Fight Predictor - AI-Powered Fight Analysis",
  description: "Advanced machine learning ensemble for fight prediction with 91.33% accuracy",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        style={{ backgroundColor: '#000000', minHeight: '100vh' }}
      >
        <ClerkProvider>
          <ConvexClientProvider>
            <UserProvider>
              <Header />
              <main className="container mx-auto px-4 py-8 text-center" style={{ backgroundColor: 'transparent' }}>
                {children}
              </main>
            </UserProvider>
          </ConvexClientProvider>
        </ClerkProvider>
      </body>
    </html>
  );
}
