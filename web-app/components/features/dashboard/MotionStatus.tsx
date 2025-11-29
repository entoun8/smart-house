"use client";

import { useEffect, useState } from "react";
import { insertMotionLog, getMotionCount } from "@/lib/supabaseService";
import { subscribe, TOPICS } from "@/lib/mqtt";
import { Activity } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function MotionStatus() {
  const [motionCount, setMotionCount] = useState<number>(0);
  const [lastDetection, setLastDetection] = useState<string>("");

  const fetchMotionCount = async () => {
    const count = await getMotionCount(1);
    setMotionCount(count);
  };

  useEffect(() => {
    const unsubscribe = subscribe(TOPICS.motion, async () => {
      setLastDetection(new Date().toLocaleTimeString());
      setMotionCount((prev) => prev + 1);
      await insertMotionLog();
    });

    fetchMotionCount();

    return unsubscribe;
  }, []);

  return (
    <Card className="hover:shadow-lg transition-all">
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Activity
            className={`w-6 h-6 ${
              motionCount > 0 ? "text-orange-500" : "text-gray-400"
            }`}
          />
          Motion Detection
        </CardTitle>
        <CardDescription>PIR detections in the last hour</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <p className="text-4xl font-bold">{motionCount}</p>
          <p className="text-sm text-muted-foreground">
            {motionCount === 1 ? "detection" : "detections"}
          </p>
          {lastDetection && (
            <p className="text-sm text-muted-foreground">
              Last detection: {lastDetection}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
