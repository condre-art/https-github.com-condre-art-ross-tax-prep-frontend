import Card from '../shared/Card';
import IRSEfileWidget from './IRSEfileWidget';
import EfileKillSwitchPanel from './EfileKillSwitchPanel';
import SendTestFilesPanel from './SendTestFilesPanel';
import SendEtinFilesPanel from './SendEtinFilesPanel';

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
      <EfileKillSwitchPanel />
      <SendTestFilesPanel />
      <SendEtinFilesPanel />
    </div>
  );
}
