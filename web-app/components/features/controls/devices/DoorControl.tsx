"use client";

import { useEffect, useState } from "react";
import { DoorOpen } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { subscribe, TOPICS } from "@/lib/mqtt";

interface DoorControlProps {
  isConnected: boolean;
  sendCommand: (topic: string, message: string, label: string) => void;
}

export default function DoorControl({
  isConnected,
  sendCommand,
}: DoorControlProps) {
  const [status, setStatus] = useState<string>("close");

  useEffect(() => {
    subscribe(TOPICS.doorState, (message) => {
      setStatus(message);
    });
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <DoorOpen className="w-6 h-6 text-blue-400" />
          Door Servo
        </CardTitle>
        <CardDescription>
          Status: <span className={`font-bold ${status === "open" ? "text-green-500" : status === "close" ? "text-red-500" : "text-gray-500"}`}>
            {status.toUpperCase()}
          </span>
        </CardDescription>
      </CardHeader>
      <CardContent className="flex gap-3">
        <Button
          onClick={() => sendCommand(TOPICS.doorCommand, "open", "Door")}
          className="flex-1 bg-green-600 hover:bg-green-700"
          disabled={!isConnected}
        >
          Open
        </Button>
        <Button
          onClick={() => sendCommand(TOPICS.doorCommand, "close", "Door")}
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
