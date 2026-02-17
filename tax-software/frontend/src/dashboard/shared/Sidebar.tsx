import React from 'react';
import { Link } from 'react-router-dom';

const links = [
  { to: '/dashboard/admin', label: 'Admin' },
  { to: '/dashboard/client', label: 'Client' },
  { to: '/dashboard/staff', label: 'Staff' },
  { to: '/dashboard/analytics', label: 'Analytics' },
];

export default function Sidebar() {
  return (
    <aside className="sidebar ios-theme">
      <nav>
        <ul>
          {links.map(link => (
            <li key={link.to}>
              <Link to={link.to}>{link.label}</Link>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
