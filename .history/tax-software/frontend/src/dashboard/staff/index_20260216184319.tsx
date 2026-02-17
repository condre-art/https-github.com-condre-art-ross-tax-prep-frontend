import DashboardLayout from '../shared/DashboardLayout';
import StaffWidgets from './widgets';

export default function StaffDashboard() {
  return (
    <DashboardLayout title="Staff Dashboard">
      <StaffWidgets />
    </DashboardLayout>
  );
}
