"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { connectMQTT, TOPICS } from "@/lib/mqtt";
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

  useEffect(() => {
    console.log("[MotionStatus] Component mounted");
    console.log("[MotionStatus] TOPICS.motion:", TOPICS.motion);

    const client = connectMQTT();
    console.log("[MotionStatus] MQTT client created");

    client.on("connect", () => {
      console.log(
        "[MotionStatus] MQTT connected, subscribing to:",
        TOPICS.motion
      );

      client.subscribe(TOPICS.motion, (err) => {
        if (!err) {
          console.log("[MotionStatus] ✅ Subscribed to", TOPICS.motion);
        } else {
          console.error("[MotionStatus] ❌ Subscribe failed:", err);
        }
      });
    });

    const handleMessage = async (topic: string, message: Buffer) => {
      if (topic === TOPICS.motion) {
        console.log(
          "🚨 [MotionStatus] Motion detected from MQTT:",
          message.toString()
        );
        setLastDetection(new Date().toLocaleTimeString());
        setMotionCount((prev) => prev + 1);

        // Log to database so it persists after refresh
        const { error } = await supabase.from("motion_logs").insert({});
        if (error) {
          console.error("[MotionStatus] DB log failed:", error);
        } else {
          console.log("[MotionStatus] ✅ Logged to database");
        }
      }
    };

    client.on("message", handleMessage);

    fetchMotionCount();

    return () => {
      client.off("message", handleMessage);
    };
  }, []);

  const fetchMotionCount = async () => {
    const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000).toISOString();

    const { data, count } = await supabase
      .from("motion_logs")
      .select("*", { count: "exact", head: true })
      .gte("timestamp", oneHourAgo);

    if (count !== null) {
      setMotionCount(count);
    }
  };

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
