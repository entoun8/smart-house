"use client";

import { publish } from "@/lib/mqtt";
import DoorControl from "./DoorControl";
import WindowControl from "./WindowControl";
import FanControl from "./FanControl";

export default function ControlsContent() {
  const sendCommand = (topic: string, message: string) => {
    publish(topic, message);
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
      <DoorControl sendCommand={sendCommand} />
      <WindowControl sendCommand={sendCommand} />
      <FanControl sendCommand={sendCommand} />
    </div>
  );
}
