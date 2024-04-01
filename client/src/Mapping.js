import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom'; // If you're using react-router

// Custom hook to parse query parameters
function useQuery() {
    return new URLSearchParams(useLocation().search);
}

// MappingPageContent component handles the main content and logic
function MappingPageContent() {
    const [headers, setHeaders] = useState([]);
    const [mapping, setMapping] = useState({});
    const [saveStatus, setSaveStatus] = useState('');

    const query = useQuery();

    useEffect(() => {
        const filepath = query.get('filepath') || '';
        // Fetch mapping data only once on component mount
        fetch('/api/get_mapping', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ filepath }),
        })
            .then(response => response.json())
            .then(data => {
                setMapping(data);
                setHeaders(Object.keys(data));
            });
    });

    const handleChange = (event) => {
        const { name, value } = event.target;
        setMapping(prevMapping => ({
            ...prevMapping,
            [name]: value,
        }));
    };

    const handleSaveMapping = () => {
        fetch('/api/save_mapping', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(mapping)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                setSaveStatus('Mapping saved successfully!');
                // Reset the status message after a delay
                setTimeout(() => setSaveStatus(''), 5000);
            })
            .catch(error => {
                console.error('There was a problem with the save operation:', error);
                setSaveStatus('Failed to save mapping. Please try again.');
                // Reset the status message after a delay
                setTimeout(() => setSaveStatus(''), 5000);
            });
    };

    return (
        <div className="p-10 rounded-lg">
            {headers.map(header => (
                <div key={header} className="flex items-center mb-4">
                    <label className="mr-2 text-sm font-bold w-48">{header}</label>
                    <select name={header} value={mapping[header]} onChange={handleChange} className="shadow appearance-none border rounded w-48 py-2 px-3 leading-tight focus:outline-none focus:shadow-outline">
                        {['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5'].map(category => (
                            <option key={category} value={category}>{category}</option>
                        ))}
                    </select>
                </div>
            ))}
            <button onClick={handleSaveMapping} className="bg-secondary hover:bg-secondary-focus text-secondary-content font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Save Mapping</button>
            {saveStatus && <div className="mt-4 text-sm font-semibold">{saveStatus}</div>}
        </div>
    );
}

// Mapping component wraps MappingPageContent in Suspense
export default function Mapping() {
    return (
        <React.Suspense fallback={<div>Loading...</div>}>
            <MappingPageContent />
        </React.Suspense>
    );
}
