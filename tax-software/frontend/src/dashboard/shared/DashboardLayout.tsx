import Sidebar from './Sidebar';
import Header from './Header';
import '../ios-theme.css';

interface DashboardLayoutProps {
  title: string;
  children: React.ReactNode;
}

export default function DashboardLayout({ title, children }: DashboardLayoutProps) {
  return (
    <div className="dashboard-layout ios-theme">
      <Sidebar />
      <div className="dashboard-main">
        <Header title={title} />
        <div className="dashboard-content">
          {children}
        </div>
      </div>
    </div>
  );
}
