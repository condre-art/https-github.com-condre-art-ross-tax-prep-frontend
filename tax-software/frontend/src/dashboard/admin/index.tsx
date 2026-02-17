import DashboardLayout from '../shared/DashboardLayout';
import AdminWidgets from './widgets';

export default function AdminDashboard() {
  return (
    <DashboardLayout title="Admin Dashboard">
      <AdminWidgets />
    </DashboardLayout>
  );
}
