import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface RfidStatisticsProps {
  totalScans: number;
  successCount: number;
  failCount: number;
}

export default function RfidStatistics({
  totalScans,
  successCount,
  failCount,
}: RfidStatisticsProps) {
  return (
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
            {totalScans > 0 ? ((failCount / totalScans) * 100).toFixed(1) : 0}%
            failure rate
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
