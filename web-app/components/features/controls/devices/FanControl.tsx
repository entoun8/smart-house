"use client";

import { useEffect, useState } from "react";
import { Fan } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { subscribe, TOPICS } from "@/lib/mqtt";

interface FanControlProps {
  isConnected: boolean;
  sendCommand: (topic: string, message: string, label: string) => void;
}

export default function FanControl({
  isConnected,
  sendCommand,
}: FanControlProps) {
  const [status, setStatus] = useState<string>("off");

  useEffect(() => {
    subscribe(TOPICS.fanState, (message) => {
      setStatus(message);
    });
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Fan className="w-6 h-6 text-purple-400" />
          Fan Motor
        </CardTitle>
        <CardDescription>
          Status: <span className={`font-bold ${status === "on" ? "text-green-500" : status === "off" ? "text-red-500" : "text-gray-500"}`}>
            {status.toUpperCase()}
          </span>
        </CardDescription>
      </CardHeader>
      <CardContent className="flex gap-3">
        <Button
          onClick={() => sendCommand(TOPICS.fanCommand, "on", "Fan")}
          className="flex-1 bg-green-600 hover:bg-green-700"
          disabled={!isConnected}
        >
          Turn ON
        </Button>
        <Button
          onClick={() => sendCommand(TOPICS.fanCommand, "off", "Fan")}
          variant="destructive"
          className="flex-1"
          disabled={!isConnected}
        >
          Turn OFF
        </Button>
      </CardContent>
    </Card>
  );
}
