import { Wind as Window } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TOPICS } from "@/lib/mqtt";

interface WindowControlProps {
  isConnected: boolean;
  sendCommand: (topic: string, message: string, label: string) => void;
}

export default function WindowControl({
  isConnected,
  sendCommand,
}: WindowControlProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Window className="w-6 h-6 text-cyan-400" />
          Window Servo
        </CardTitle>
        <CardDescription>Window servo on GPIO 5</CardDescription>
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
