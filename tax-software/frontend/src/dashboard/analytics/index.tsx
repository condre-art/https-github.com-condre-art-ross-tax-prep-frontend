import DashboardLayout from '../shared/DashboardLayout';
import AnalyticsWidgets from './widgets';

export default function AnalyticsDashboard() {
  return (
    <DashboardLayout title="Analytics Dashboard">
      <AnalyticsWidgets />
    </DashboardLayout>
  );
}
