import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom'; // If you're using react-router

// Custom hook to parse query parameters
function useQuery() {
  return new URLSearchParams(useLocation().search);
}

// FileContent component handles the main content and logic
function FileContent() {
  const [data, setData] = useState([]);
  const query = useQuery();
  const filepath = query.get('filepath');

  useEffect(() => {
    if (filepath) {
      fetch('/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filepath }),
      })
        .then(response => response.json())
        .then(data => setData(data));
    }
  }, [filepath]);

  const headers = data.length > 0 ? Object.keys(data[0]) : [];

  return (
    <div>
      <button onClick={() => window.open(`/api/download?file=${filepath}`, '_blank')} className="btn btn-sm btn-secondary m-4">
        Export CSV
      </button>
      {data.length === 0 ? (
        <div>Loading...</div>
      ) : (
        <table className="table table-zebra	table-pin-rows">
          <thead>
            <tr>
              {headers.map((header, index) => (
                <th key={index}>{header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {headers.map((header, index) => (
                  <td key={index}>{row[header]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

// File component wraps FileContent in Suspense
export default function File() {
  return (
    <React.Suspense fallback={<div>Loading...</div>}>
      <FileContent />
    </React.Suspense>
  );
}
