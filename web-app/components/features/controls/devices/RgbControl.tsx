import { Palette } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface RgbControlProps {
  isConnected: boolean;
  sendCommand: (topic: string, message: string, label: string) => void;
}

export default function RgbControl({
  isConnected,
  sendCommand,
}: RgbControlProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Palette className="w-6 h-6 text-pink-400" />
          RGB Strip
        </CardTitle>
        <CardDescription>4 NeoPixel LEDs on GPIO 26</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-2">
          <Button
            onClick={() => sendCommand("home/commands/rgb", "red", "RGB")}
            className="bg-red-600 hover:bg-red-700"
            disabled={!isConnected}
            size="sm"
          >
            Red
          </Button>
          <Button
            onClick={() => sendCommand("home/commands/rgb", "green", "RGB")}
            className="bg-green-600 hover:bg-green-700"
            disabled={!isConnected}
            size="sm"
          >
            Green
          </Button>
          <Button
            onClick={() => sendCommand("home/commands/rgb", "blue", "RGB")}
            className="bg-blue-600 hover:bg-blue-700"
            disabled={!isConnected}
            size="sm"
          >
            Blue
          </Button>
          <Button
            onClick={() => sendCommand("home/commands/rgb", "orange", "RGB")}
            className="bg-orange-600 hover:bg-orange-700"
            disabled={!isConnected}
            size="sm"
          >
            Orange
          </Button>
          <Button
            onClick={() => sendCommand("home/commands/rgb", "purple", "RGB")}
            className="bg-purple-600 hover:bg-purple-700"
            disabled={!isConnected}
            size="sm"
          >
            Purple
          </Button>
          <Button
            onClick={() => sendCommand("home/commands/rgb", "off", "RGB")}
            variant="outline"
            disabled={!isConnected}
            size="sm"
          >
            OFF
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
