import "./globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "GovMate",
  description: "Community AI agents for accessing government and community services",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900">
        <main className="container mx-auto px-4 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}