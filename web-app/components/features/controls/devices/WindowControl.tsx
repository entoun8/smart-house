"use client";

import { useEffect, useState } from "react";
import { Wind as Window } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { subscribe, TOPICS } from "@/lib/mqtt";

interface WindowControlProps {
  isConnected: boolean;
  sendCommand: (topic: string, message: string, label: string) => void;
}

export default function WindowControl({
  isConnected,
  sendCommand,
}: WindowControlProps) {
  const [status, setStatus] = useState<string>("close");

  useEffect(() => {
    subscribe(TOPICS.windowState, (message) => {
      setStatus(message);
    });
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Window className="w-6 h-6 text-cyan-400" />
          Window Servo
        </CardTitle>
        <CardDescription>
          Status: <span className={`font-bold ${status === "open" ? "text-green-500" : status === "close" ? "text-red-500" : "text-gray-500"}`}>
            {status.toUpperCase()}
          </span>
        </CardDescription>
      </CardHeader>
      <CardContent className="flex gap-3">
        <Button
          onClick={() => sendCommand(TOPICS.windowCommand, "open", "Window")}
          className="flex-1 bg-green-600 hover:bg-green-700"
          disabled={!isConnected}
        >
          Open
        </Button>
        <Button
          onClick={() => sendCommand(TOPICS.windowCommand, "close", "Window")}
          variant="destructive"
          className="flex-1"
          disabled={!isConnected}
        >
          Close
        </Button>
      </CardContent>
    </Card>
  );
}
