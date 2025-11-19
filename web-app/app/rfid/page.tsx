"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { connectMQTT } from "@/lib/mqtt";
import { KeyRound, CheckCircle, XCircle, Filter, ArrowLeft } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Link from "next/link";

type RfidScan = {
  id: number;
  card_id: string;
  success: boolean;
  user_id: number | null;
  timestamp: string;
  user?: {
    name: string;
  };
};

type FilterType = "all" | "success" | "fail";

export default function RfidPage() {
  const [scans, setScans] = useState<RfidScan[]>([]);
  const [filter, setFilter] = useState<FilterType>("all");
  const [latestScan, setLatestScan] = useState<RfidScan | null>(null);

  useEffect(() => {
    console.log("[RfidPage] Component mounted");

    // Connect to MQTT for real-time updates
    const client = connectMQTT();

    client.on("connect", () => {
      console.log("[RfidPage] MQTT connected, subscribing to RFID topic");

      client.subscribe("ks5009/house/events/rfid_scan", (err) => {
        if (!err) {
          console.log("[RfidPage] ✅ Subscribed to RFID scan topic");
        } else {
          console.error("[RfidPage] ❌ Subscribe failed:", err);
        }
      });
    });

    const handleMessage = (topic: string, message: Buffer) => {
      if (topic === "ks5009/house/events/rfid_scan") {
        console.log(
          "🔑 [RfidPage] RFID scan from MQTT:",
          message.toString()
        );

        // Refresh data when new scan detected
        fetchScans();
      }
    };

    client.on("message", handleMessage);

    // Initial data fetch
    fetchScans();

    // Refresh every 5 seconds
    const interval = setInterval(fetchScans, 5000);

    return () => {
      client.off("message", handleMessage);
      clearInterval(interval);
    };
  }, []);

  const fetchScans = async () => {
    const { data, error } = await supabase
      .from("rfid_scans")
      .select(
        `
        id,
        card_id,
        success,
        user_id,
        timestamp,
        users (
          name
        )
      `
      )
      .order("timestamp", { ascending: false })
      .limit(100);

    if (error) {
      console.error("Error fetching RFID scans:", error);
      return;
    }

    if (data) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const formattedData = data.map((scan: any) => ({
        ...scan,
        user: scan.users,
      }));

      setScans(formattedData);

      // Set latest scan
      if (formattedData.length > 0) {
        setLatestScan(formattedData[0]);
      }
    }
  };

  const filteredScans = scans.filter((scan) => {
    if (filter === "success") return scan.success;
    if (filter === "fail") return !scan.success;
    return true;
  });

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const successCount = scans.filter((s) => s.success).length;
  const failCount = scans.filter((s) => !s.success).length;
  const totalScans = scans.length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <Link href="/">
            <Button variant="outline" size="icon">
              <ArrowLeft className="w-4 h-4" />
            </Button>
          </Link>
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              RFID Access Control
            </h1>
            <p className="text-muted-foreground mt-1">
              View all RFID card scans and access attempts
            </p>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Total Scans</CardDescription>
              <CardTitle className="text-3xl">{totalScans}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">All time</p>
            </CardContent>
          </Card>

          <Card className="border-green-500/20 bg-green-500/5">
            <CardHeader className="pb-2">
              <CardDescription className="text-green-700 dark:text-green-400">
                Successful Access
              </CardDescription>
              <CardTitle className="text-3xl text-green-600 dark:text-green-400">
                {successCount}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                {totalScans > 0
                  ? ((successCount / totalScans) * 100).toFixed(1)
                  : 0}
                % success rate
              </p>
            </CardContent>
          </Card>

          <Card className="border-red-500/20 bg-red-500/5">
            <CardHeader className="pb-2">
              <CardDescription className="text-red-700 dark:text-red-400">
                Failed Attempts
              </CardDescription>
              <CardTitle className="text-3xl text-red-600 dark:text-red-400">
                {failCount}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                {totalScans > 0
                  ? ((failCount / totalScans) * 100).toFixed(1)
                  : 0}
                % failure rate
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Table */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-3">
                  <KeyRound className="w-6 h-6 text-blue-500" />
                  Access Logs
                </CardTitle>
                <CardDescription>
                  Recent RFID card scans with filter options
                </CardDescription>
              </div>

              <div className="flex gap-2">
                <Button
                  variant={filter === "all" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setFilter("all")}
                >
                  <Filter className="w-4 h-4 mr-2" />
                  All ({totalScans})
                </Button>
                <Button
                  variant={filter === "success" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setFilter("success")}
                  className={
                    filter === "success"
                      ? "bg-green-500 hover:bg-green-600"
                      : ""
                  }
                >
                  <CheckCircle className="w-4 h-4 mr-2" />
                  Success ({successCount})
                </Button>
                <Button
                  variant={filter === "fail" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setFilter("fail")}
                  className={
                    filter === "fail" ? "bg-red-500 hover:bg-red-600" : ""
                  }
                >
                  <XCircle className="w-4 h-4 mr-2" />
                  Failed ({failCount})
                </Button>
              </div>
            </div>
          </CardHeader>

          <CardContent>
            {/* Latest Scan Alert */}
            {latestScan && (
              <div
                className={`mb-4 p-4 rounded-lg ${
                  latestScan.success
                    ? "bg-green-500/10 border border-green-500/20"
                    : "bg-red-500/10 border border-red-500/20"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-semibold mb-1">Latest Scan</p>
                    <p className="text-sm">
                      <span className="font-mono text-xs bg-black/10 dark:bg-white/10 px-2 py-1 rounded">
                        {latestScan.card_id}
                      </span>
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {formatTime(latestScan.timestamp)}
                    </p>
                  </div>
                  <div className="text-right">
                    {latestScan.user && (
                      <p className="text-sm font-medium mb-1">
                        {latestScan.user.name}
                      </p>
                    )}
                    <Badge
                      variant={latestScan.success ? "default" : "destructive"}
                      className={`flex items-center gap-1 ${
                        latestScan.success ? "bg-green-500" : ""
                      }`}
                    >
                      {latestScan.success ? (
                        <>
                          <CheckCircle className="w-3 h-3" />
                          Authorized
                        </>
                      ) : (
                        <>
                          <XCircle className="w-3 h-3" />
                          Denied
                        </>
                      )}
                    </Badge>
                  </div>
                </div>
              </div>
            )}

            {/* Table */}
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[200px]">Timestamp</TableHead>
                    <TableHead>Card ID</TableHead>
                    <TableHead>User</TableHead>
                    <TableHead className="text-right">Result</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredScans.length === 0 ? (
                    <TableRow>
                      <TableCell
                        colSpan={4}
                        className="text-center text-muted-foreground py-8"
                      >
                        No scans found
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredScans.map((scan) => (
                      <TableRow key={scan.id}>
                        <TableCell className="text-sm">
                          {formatTime(scan.timestamp)}
                        </TableCell>
                        <TableCell>
                          <code className="text-xs bg-muted px-2 py-1 rounded">
                            {scan.card_id}
                          </code>
                        </TableCell>
                        <TableCell>
                          {scan.user?.name || (
                            <span className="text-muted-foreground italic text-sm">
                              Unknown User
                            </span>
                          )}
                        </TableCell>
                        <TableCell className="text-right">
                          {scan.success ? (
                            <Badge
                              variant="default"
                              className="bg-green-500 flex items-center gap-1 w-fit ml-auto"
                            >
                              <CheckCircle className="w-3 h-3" />
                              Success
                            </Badge>
                          ) : (
                            <Badge
                              variant="destructive"
                              className="flex items-center gap-1 w-fit ml-auto"
                            >
                              <XCircle className="w-3 h-3" />
                              Failed
                            </Badge>
                          )}
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>

            {/* Footer Info */}
            <div className="mt-4 text-center text-sm text-muted-foreground">
              Showing {filteredScans.length} of {totalScans} total scans
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
