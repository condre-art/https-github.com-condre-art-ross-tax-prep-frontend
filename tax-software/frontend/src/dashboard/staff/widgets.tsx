import Card from '../shared/Card';

export default function StaffWidgets() {
  return (
    <div className="staff-widgets">
      <Card title="Client Files">
        {/* Example: List client files, actions, etc. */}
        <div>View and manage client files.</div>
      </Card>
      <Card title="Workflow">
        {/* Example: Show workflow steps, progress, etc. */}
        <div>Track workflow progress.</div>
      </Card>
    </div>
  );
}
