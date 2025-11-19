"use client";

import { ThemeToggle } from "@/components/theme-toggle";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Settings, Activity, KeyRound } from "lucide-react";
import Link from "next/link";

export default function DashboardHeader({
  isConnected,
}: {
  isConnected: boolean;
}) {
  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mb-8">
      <div>
        <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
          🏠 Smart Home Dashboard
        </h1>
        <p className="text-sm md:text-base text-muted-foreground">
          Monitor your home in real-time
        </p>
      </div>
      <div className="flex flex-wrap gap-2 md:gap-3">
        <ThemeToggle />
        <Link href="/rfid">
          <Button variant="outline" className="gap-2">
            <KeyRound className="w-4 h-4" />
            <span className="hidden sm:inline">RFID Logs</span>
          </Button>
        </Link>
        <Link href="/controls">
          <Button variant="outline" className="gap-2">
            <Settings className="w-4 h-4" />
            <span className="hidden sm:inline">Controls</span>
          </Button>
        </Link>
        <Badge
          variant={isConnected ? "default" : "destructive"}
          className="h-8 px-3 md:px-4"
        >
          <Activity className="w-4 h-4 mr-1 md:mr-2" />
          <span className="hidden sm:inline">
            {isConnected ? "Connected" : "Disconnected"}
          </span>
          <span className="sm:hidden">
            {isConnected ? "✓" : "✗"}
          </span>
        </Badge>
      </div>
    </div>
  );
}
