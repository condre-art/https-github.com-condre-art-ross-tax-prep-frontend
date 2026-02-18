import Card from '../shared/Card';
import IRSEfileWidget from './IRSEfileWidget';

export default function AdminWidgets() {
  return (
    <div className="admin-widgets">
      <Card title="User Management">
        {/* Example: List users, add/remove, etc. */}
        <div>Manage users and roles.</div>
      </Card>
      <Card title="Platform Analytics">
        {/* Example: Show stats, charts, etc. */}
        <div>View platform stats and activity.</div>
      </Card>
      <IRSEfileWidget />
    </div>
  );
}
