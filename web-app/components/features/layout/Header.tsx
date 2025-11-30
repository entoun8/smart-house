"use client";

import { ThemeToggle } from "@/components/theme-toggle";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { LayoutDashboard, Settings, KeyRound, Activity } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

interface HeaderProps {
  isConnected: boolean;
}

export default function Header({ isConnected }: HeaderProps) {
  const pathname = usePathname();

  const getPageInfo = () => {
    if (pathname === "/" || pathname === "/dashboard") {
      return {
        title: "Smart Home Dashboard",
        description: "Monitor your home in real-time",
      };
    } else if (pathname === "/controls") {
      return {
        title: "Device Controls",
        description: "Control your smart home remotely",
      };
    } else if (pathname === "/rfid") {
      return {
        title: "RFID Access Control",
        description: "View all RFID card scans and access attempts",
      };
    }
    return {
      title: "Smart Home",
      description: "Your smart home system",
    };
  };

  const pageInfo = getPageInfo();

  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mb-8">
      <div>
        <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
          {pageInfo.title}
        </h1>
        <p className="text-sm md:text-base text-muted-foreground">
          {pageInfo.description}
        </p>
      </div>

      <div className="flex flex-wrap gap-2 md:gap-3">
        <ThemeToggle />

        <Link href="/">
          <Button
            variant={pathname === "/" ? "default" : "outline"}
            className="gap-2"
          >
            <LayoutDashboard className="w-4 h-4" />
            <span className="hidden sm:inline">Dashboard</span>
          </Button>
        </Link>

        <Link href="/controls">
          <Button
            variant={pathname === "/controls" ? "default" : "outline"}
            className="gap-2"
          >
            <Settings className="w-4 h-4" />
            <span className="hidden sm:inline">Controls</span>
          </Button>
        </Link>

        <Link href="/rfid">
          <Button
            variant={pathname === "/rfid" ? "default" : "outline"}
            className="gap-2"
          >
            <KeyRound className="w-4 h-4" />
            <span className="hidden sm:inline">RFID Logs</span>
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
          <span className="sm:hidden">{isConnected ? "✓" : "✗"}</span>
        </Badge>
      </div>
    </div>
  );
}
