import { useState } from "react";
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
import TablePagination from "@/components/ui/table-pagination";

export type FilterType = "all" | "success" | "fail";

interface RfidLogsTableProps {
  scans: RfidScan[];
  filter: FilterType;
  setFilter: (filter: FilterType) => void;
  latestScan: RfidScan | null;
  formatTime: (timestamp: string) => string;
}

const ITEMS_PER_PAGE = 10;

export default function RfidLogsTable({
  scans,
  filter,
  setFilter,
  latestScan,
  formatTime,
}: RfidLogsTableProps) {
  const [currentPage, setCurrentPage] = useState(1);

  const filteredScans = scans.filter((scan) => {
    if (filter === "success") return scan.success;
    if (filter === "fail") return !scan.success;
    return true;
  });

  const totalPages = Math.ceil(filteredScans.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const paginatedScans = filteredScans.slice(startIndex, endIndex);

  const successCount = scans.filter((s) => s.success).length;
  const failCount = scans.filter((s) => !s.success).length;
  const totalScans = scans.length;

  const handleFilterChange = (newFilter: FilterType) => {
    setFilter(newFilter);
    setCurrentPage(1);
  };

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
              onClick={() => handleFilterChange("all")}
            >
              <Filter className="w-4 h-4 mr-2" />
              All ({totalScans})
            </Button>
            <Button
              variant={filter === "success" ? "default" : "outline"}
              size="sm"
              onClick={() => handleFilterChange("success")}
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
              onClick={() => handleFilterChange("fail")}
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
        {latestScan && (
          <RfidLatestScan scan={latestScan} formatTime={formatTime} />
        )}

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
              {paginatedScans.length === 0 ? (
                <TableRow>
                  <TableCell
                    colSpan={4}
                    className="text-center text-muted-foreground py-8"
                  >
                    No scans found
                  </TableCell>
                </TableRow>
              ) : (
                paginatedScans.map((scan) => (
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

        <div className="mt-6">
          <TablePagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
            startIndex={startIndex}
            endIndex={endIndex}
            filteredCount={filteredScans.length}
            totalCount={totalScans}
          />
        </div>
      </CardContent>
    </Card>
  );
}
