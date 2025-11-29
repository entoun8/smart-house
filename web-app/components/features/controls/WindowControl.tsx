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
  sendCommand: (topic: string, message: string) => void;
}

export default function WindowControl({ sendCommand }: WindowControlProps) {
  const [status, setStatus] = useState<string>("close");

  useEffect(() => {
    const unsubscribe = subscribe(TOPICS.windowState, (message) => {
      setStatus(message);
    });

    return unsubscribe;
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
          onClick={() => sendCommand(TOPICS.windowCommand, "open")}
          className="flex-1 bg-green-600 hover:bg-green-700"
        >
          Open
        </Button>
        <Button
          onClick={() => sendCommand(TOPICS.windowCommand, "close")}
          variant="destructive"
          className="flex-1"
        >
          Close
        </Button>
      </CardContent>
    </Card>
  );
}
