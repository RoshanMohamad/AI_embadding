import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Shopping Assistant | Smart Product Discovery",
  description: "Intelligent shopping assistant powered by AI. Find products using natural language, get personalized recommendations, and chat with our knowledge base.",
  keywords: ["AI shopping", "semantic search", "product recommendations", "RAG", "e-commerce"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.Node;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
