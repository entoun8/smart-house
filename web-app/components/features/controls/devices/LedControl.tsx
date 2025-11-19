import { Lightbulb } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface LedControlProps {
  isConnected: boolean;
  sendCommand: (topic: string, message: string, label: string) => void;
}

export default function LedControl({
  isConnected,
  sendCommand,
}: LedControlProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Lightbulb className="w-6 h-6 text-yellow-400" />
          LED Light
        </CardTitle>
        <CardDescription>Yellow LED on GPIO 12</CardDescription>
      </CardHeader>
      <CardContent className="flex gap-3">
        <Button
          onClick={() => sendCommand("home/commands/led", "on", "LED")}
          className="flex-1 bg-yellow-600 hover:bg-yellow-700"
          disabled={!isConnected}
        >
          On
        </Button>
        <Button
          onClick={() => sendCommand("home/commands/led", "off", "LED")}
          variant="destructive"
          className="flex-1"
          disabled={!isConnected}
        >
          Off
        </Button>
      </CardContent>
    </Card>
  );
}
