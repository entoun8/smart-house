import { DoorOpen } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface DoorControlProps {
  isConnected: boolean;
  sendCommand: (topic: string, message: string, label: string) => void;
}

export default function DoorControl({
  isConnected,
  sendCommand,
}: DoorControlProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <DoorOpen className="w-6 h-6 text-blue-400" />
          Door Servo
        </CardTitle>
        <CardDescription>Door servo on GPIO 13</CardDescription>
      </CardHeader>
      <CardContent className="flex gap-3">
        <Button
          onClick={() => sendCommand("home/commands/door", "open", "Door")}
          className="flex-1 bg-green-600 hover:bg-green-700"
          disabled={!isConnected}
        >
          Open
        </Button>
        <Button
          onClick={() => sendCommand("home/commands/door", "close", "Door")}
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
