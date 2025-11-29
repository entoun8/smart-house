import AsthmaAlert from "./AsthmaAlert";
import TemperatureStatus from "./TemperatureStatus";
import HumidityStatus from "./HumidityStatus";
import MotionStatus from "./MotionStatus";
import GasStatus from "./GasStatus";

export default function DashboardContent() {
  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        <TemperatureStatus />
        <HumidityStatus />
        <MotionStatus />
        <GasStatus />
      </div>
      <AsthmaAlert />
    </>
  );
}
