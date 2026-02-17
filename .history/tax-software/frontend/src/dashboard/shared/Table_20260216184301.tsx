import React from 'react';

interface TableProps {
  columns: string[];
  data: Array<Record<string, any>>;
}

export default function Table({ columns, data }: TableProps) {
  return (
    <table className="dashboard-table ios-theme">
      <thead>
        <tr>
          {columns.map(col => <th key={col}>{col}</th>)}
        </tr>
      </thead>
      <tbody>
        {data.map((row, idx) => (
          <tr key={idx}>
            {columns.map(col => <td key={col}>{row[col]}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
