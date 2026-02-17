import Card from '../shared/Card';

export default function ClientWidgets() {
  return (
    <div className="client-widgets">
      <Card title="Tax Status">
        {/* Example: Show tax status, progress, etc. */}
        <div>Your tax return status: In Progress</div>
      </Card>
      <Card title="Notifications">
        {/* Example: Show notifications, alerts, etc. */}
        <div>No new notifications.</div>
      </Card>
    </div>
  );
}
