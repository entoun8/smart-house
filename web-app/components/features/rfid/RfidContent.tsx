"use client";

import { useEffect, useState } from "react";
import { getUserByRfidCard, insertRfidScan, getRfidScans } from "@/lib/supabaseService";
import { subscribe, TOPICS } from "@/lib/mqtt";
import RfidStatistics from "./RfidStatistics";
import RfidLogsTable, { FilterType } from "./RfidLogsTable";
import { RfidScan } from "./RfidLatestScan";

export default function RfidContent() {
  const [scans, setScans] = useState<RfidScan[]>([]);
  const [filter, setFilter] = useState<FilterType>("all");
  const [latestScan, setLatestScan] = useState<RfidScan | null>(null);

  useEffect(() => {
    const unsubscribe = subscribe(TOPICS.rfid, async (message) => {
      try {
        const data = JSON.parse(message);
        const cardId = data.card;
        const isAuthorized = data.status === "authorized";

        // If authorized, get the user_id for this card
        let userId = null;
        if (isAuthorized) {
          const user = await getUserByRfidCard(cardId);
          userId = user?.id || null;
        }

        const { error } = await insertRfidScan(cardId, isAuthorized, userId);

        if (error) {
          console.error("Failed to insert RFID scan:", error);
        } else {
          console.log("✅ RFID scan saved to database");
        }

        fetchScans();
      } catch (e) {
        console.error("Failed to parse RFID message:", e);
      }
    });

    fetchScans();

    const interval = setInterval(fetchScans, 5000);

    return () => {
      clearInterval(interval);
      unsubscribe();
    };
  }, []);

  const fetchScans = async () => {
    const data = await getRfidScans(100);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const formattedData = data.map((scan: any) => ({
      ...scan,
      user: scan.users,
    }));

    setScans(formattedData);

    if (formattedData.length > 0) {
      setLatestScan(formattedData[0]);
    }
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const successCount = scans.filter((s) => s.success).length;
  const failCount = scans.filter((s) => !s.success).length;
  const totalScans = scans.length;

  return (
    <div className="space-y-6">
      <RfidStatistics
        totalScans={totalScans}
        successCount={successCount}
        failCount={failCount}
      />

      <RfidLogsTable
        scans={scans}
        filter={filter}
        setFilter={setFilter}
        latestScan={latestScan}
        formatTime={formatTime}
      />
    </div>
  );
}
