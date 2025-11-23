import { Fan } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TOPICS } from "@/lib/mqtt";

interface FanControlProps {
  isConnected: boolean;
  sendCommand: (topic: string, message: string, label: string) => void;
}

export default function FanControl({
  isConnected,
  sendCommand,
}: FanControlProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Fan className="w-6 h-6 text-purple-400" />
          Fan Motor
        </CardTitle>
        <CardDescription>DC motor on GPIO 18, 19</CardDescription>
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
