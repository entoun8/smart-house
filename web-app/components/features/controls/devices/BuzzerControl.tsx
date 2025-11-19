import { Volume2 } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface BuzzerControlProps {
  isConnected: boolean;
  sendCommand: (topic: string, message: string, label: string) => void;
}

export default function BuzzerControl({
  isConnected,
  sendCommand,
}: BuzzerControlProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Volume2 className="w-6 h-6 text-orange-400" />
          Buzzer
        </CardTitle>
        <CardDescription>Buzzer on GPIO 25</CardDescription>
      </CardHeader>
      <CardContent className="flex gap-3">
        <Button
          onClick={() => sendCommand("home/commands/buzzer", "beep", "Buzzer")}
          className="flex-1 bg-orange-600 hover:bg-orange-700"
          disabled={!isConnected}
        >
          Beep
        </Button>
        <Button
          onClick={() =>
            sendCommand("home/commands/buzzer", "alarm", "Buzzer")
          }
          variant="destructive"
          className="flex-1"
          disabled={!isConnected}
        >
          Alarm
        </Button>
      </CardContent>
    </Card>
  );
}
