"use client";

import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface ConnectionWarningProps {
  isConnected: boolean;
}

export default function ConnectionWarning({
  isConnected,
}: ConnectionWarningProps) {
  if (isConnected) {
    return null;
  }

  return (
    <Card className="mt-6 border-yellow-500 bg-yellow-500/10">
      <CardHeader>
        <CardTitle className="text-yellow-600 dark:text-yellow-400 flex items-center gap-2">
          ⚠️ Not Connected
        </CardTitle>
        <CardDescription className="text-yellow-700 dark:text-yellow-300">
          Please wait for MQTT connection. Controls are disabled until connected.
        </CardDescription>
      </CardHeader>
    </Card>
  );
}
