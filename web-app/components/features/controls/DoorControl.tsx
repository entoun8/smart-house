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
  sendCommand: (topic: string, message: string) => void;
}

export default function DoorControl({ sendCommand }: DoorControlProps) {
  const [status, setStatus] = useState<string>("close");

  useEffect(() => {
    const unsubscribe = subscribe(TOPICS.doorState, (message) => {
      setStatus(message);
    });

    return unsubscribe;
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
          onClick={() => sendCommand(TOPICS.doorCommand, "open")}
          className="flex-1 bg-green-600 hover:bg-green-700"
        >
          Open
        </Button>
        <Button
          onClick={() => sendCommand(TOPICS.doorCommand, "close")}
          variant="destructive"
          className="flex-1"
        >
          Close
        </Button>
      </CardContent>
    </Card>
  );
}
