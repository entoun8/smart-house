"use client";

import { ThemeToggle } from "@/components/theme-toggle";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { LayoutDashboard, Power } from "lucide-react";
import Link from "next/link";

interface ControlsHeaderProps {
  isConnected: boolean;
  lastCommand: string;
}

export default function ControlsHeader({
  isConnected,
  lastCommand,
}: ControlsHeaderProps) {
  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mb-8">
      <div>
        <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
          🎮 Device Controls
        </h1>
        <p className="text-sm md:text-base text-muted-foreground">
          Control your smart home remotely
        </p>
      </div>
      <div className="flex flex-wrap gap-2 md:gap-3">
        <ThemeToggle />
        <Link href="/">
          <Button variant="outline" className="gap-2">
            <LayoutDashboard className="w-4 h-4" />
            <span className="hidden sm:inline">Dashboard</span>
          </Button>
        </Link>
        <Badge
          variant={isConnected ? "default" : "destructive"}
          className="h-8 px-3 md:px-4"
        >
          <Power className="w-4 h-4 mr-1 md:mr-2" />
          <span className="hidden sm:inline">
            {isConnected ? "Connected" : "Disconnected"}
          </span>
          <span className="sm:hidden">
            {isConnected ? "✓" : "✗"}
          </span>
        </Badge>
        {lastCommand && (
          <Badge variant="secondary" className="h-8 px-3 md:px-4 max-w-[200px] truncate">
            <span className="hidden sm:inline">Last: {lastCommand}</span>
            <span className="sm:hidden">{lastCommand.split(":")[0]}</span>
          </Badge>
        )}
      </div>
    </div>
  );
}
