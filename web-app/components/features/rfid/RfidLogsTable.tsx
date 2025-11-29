import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
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
import { CheckCircle, Filter, KeyRound, XCircle } from "lucide-react";
import RfidLatestScan, { RfidScan } from "./RfidLatestScan";

export type FilterType = "all" | "success" | "fail";

interface RfidLogsTableProps {
  scans: RfidScan[];
  filter: FilterType;
  setFilter: (filter: FilterType) => void;
  latestScan: RfidScan | null;
  formatTime: (timestamp: string) => string;
}

export default function RfidLogsTable({
  scans,
  filter,
  setFilter,
  latestScan,
  formatTime,
}: RfidLogsTableProps) {
  const filteredScans = scans.filter((scan) => {
    if (filter === "success") return scan.success;
    if (filter === "fail") return !scan.success;
    return true;
  });

  const successCount = scans.filter((s) => s.success).length;
  const failCount = scans.filter((s) => !s.success).length;
  const totalScans = scans.length;

  return (
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
                filter === "success" ? "bg-green-500 hover:bg-green-600" : ""
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
          <RfidLatestScan scan={latestScan} formatTime={formatTime} />
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
  );
}
