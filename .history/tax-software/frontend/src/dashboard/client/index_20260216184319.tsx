import DashboardLayout from '../shared/DashboardLayout';
import ClientWidgets from './widgets';

export default function ClientDashboard() {
  return (
    <DashboardLayout title="Client Dashboard">
      <ClientWidgets />
    </DashboardLayout>
  );
}
