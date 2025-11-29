"use client";

import { useEffect, useState } from "react";
import { connectMQTT } from "@/lib/mqtt";
import Header from "@/components/features/layout/Header";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const client = connectMQTT();

    client.on("connect", () => {
      setIsConnected(true);
    });

    client.on("offline", () => {
      setIsConnected(false);
    });

    client.on("error", () => {
      setIsConnected(false);
    });
  }, []);

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        <Header isConnected={isConnected} />
        {children}
      </div>
    </div>
  );
}
