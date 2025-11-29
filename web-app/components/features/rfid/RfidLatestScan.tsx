import { Badge } from "@/components/ui/badge";
import { CheckCircle, XCircle } from "lucide-react";

export type RfidScan = {
  id: number;
  card_id: string;
  success: boolean;
  user_id: number | null;
  timestamp: string;
  user?: {
    name: string;
  };
};

interface RfidLatestScanProps {
  scan: RfidScan;
  formatTime: (timestamp: string) => string;
}

export default function RfidLatestScan({
  scan,
  formatTime,
}: RfidLatestScanProps) {
  return (
    <div
      className={`mb-4 p-4 rounded-lg ${
        scan.success
          ? "bg-green-500/10 border border-green-500/20"
          : "bg-red-500/10 border border-red-500/20"
      }`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold mb-1">Latest Scan</p>
          <p className="text-sm">
            <span className="font-mono text-xs bg-black/10 dark:bg-white/10 px-2 py-1 rounded">
              {scan.card_id}
            </span>
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            {formatTime(scan.timestamp)}
          </p>
        </div>
        <div className="text-right">
          {scan.user && (
            <p className="text-sm font-medium mb-1">{scan.user.name}</p>
          )}
          <Badge
            variant={scan.success ? "default" : "destructive"}
            className={`flex items-center gap-1 ${
              scan.success ? "bg-green-500" : ""
            }`}
          >
            {scan.success ? (
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
  );
}
