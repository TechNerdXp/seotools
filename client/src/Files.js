import { useEffect, useState, Suspense } from 'react';
import { ArrowUpRightIcon, PlayIcon } from '@heroicons/react/24/solid';
import { NavLink } from 'react-router-dom'; // Assuming you're using react-router for navigation

function FilesTable() {
    const [isProcessing, setIsProcessing] = useState(false);
    const [fileName, setFileName] = useState(null);
    const [files, setFiles] = useState([]);
    const [processStatus, setProcessStatus] = useState('');
    const [compressStatus, setCompressStatus] = useState('');

    useEffect(() => {
        const interval = setInterval(async () => {
            const response = await fetch('/api/check-process');
            const data = await response.json();
            setIsProcessing(data.isProcessing);
            setFileName(data.fileName);

            const filesResponse = await fetch('/api/files');
            const filesData = await filesResponse.json();
            setFiles(filesData);
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    const handleFileUpload = async (event) => {
        const files = event.target.files;
        if (files && files.length > 0) {
            const file = files[0];
            const formData = new FormData();
            formData.append('file', file);

            await fetch('/api/upload', {
                method: 'POST',
                body: formData,
            });

            // Revalidate files
            const filesResponse = await fetch('/api/files');
            const filesData = await filesResponse.json();
            setFiles(filesData);
        }
    };

    const handleStartProcess = async (fileName) => {
        try {
            const processResponse = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ fileName }),
            });
            if (!processResponse.ok) {
                throw new Error('Process response was not ok');
            }
            const processResult = await processResponse.json();
            console.log(processResult);
            setProcessStatus('Processing started successfully!');

            // Revalidate files
            const filesResponse = await fetch('/api/files');
            const filesData = await filesResponse.json();
            setFiles(filesData);

            // Reset the status message after a delay
            setTimeout(() => setProcessStatus(''), 5000);
        } catch (error) {
            console.error('There was a problem starting the process:', error);
            setProcessStatus('Failed to start processing. Please try again.');
            setTimeout(() => setProcessStatus(''), 5000);
        }
    };

    const handleCompressing = (filename) => {
        fetch('/api/compress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                setCompressStatus('Compression completed successfully!');
                setTimeout(() => setCompressStatus(''), 5000);
            })
            .catch(error => {
                console.error('There was a problem with the compression:', error);
                setCompressStatus('Failed to compress file. Please try again.');
                setTimeout(() => setCompressStatus(''), 5000);
            });
    };


    return (
        <div className="overflow-x-auto">
            <label className="flex items-center space-x-2">
                <input type="file" onChange={handleFileUpload} className="file-input file-input-bordered file-input-secondary w-full max-w-xs" accept=".csv" title="Upload a CSV with keywords in first column." />
            </label>
            <table className="table table-zebra	table-pin-rows">
                <thead>
                    <tr>
                        <th>File Name</th>
                        <th>Status</th>
                        <th>Total Records</th>
                        <th>Total Processed</th>
                        <th>Total Remaining</th>
                        <th>Process</th>
                        <th>Mapping</th>
                        <th>Compress</th>
                        <th>Input File</th>
                        <th>Specs File</th>
                        <th>Compressed</th>
                    </tr>
                </thead>
                <tbody>
                    {files.map(file => (
                        <tr key={file.id}>
                            <td>{file.file_name}</td>
                            <td>{file.file_name === fileName ? 'Running' : file.status}</td>
                            <td>{file.total_records}</td>
                            <td>{file.total_specs}</td>
                            <td>{file.total_remaining}</td>
                            <td>
                                <button
                                    onClick={() => handleStartProcess(file.file_name)}
                                    disabled={isProcessing || file.status === 'Complete'}
                                    className={`btn btn-circle btn-xs ${isProcessing || file.status === 'Complete' ? 'btn-disabled' : 'btn-ghost'}`}
                                    title="Splits provided keywords into scecifications and outputs the data into specs CSV"
                                >
                                    <PlayIcon className="w-5 h-5" />
                                </button>
                            </td>
                            <td>
                                <NavLink to={`/mapping?filepath=data/specs/specs_${file.file_name}`} className={`btn btn-circle btn-xs btn-ghost`} title="Mapping of each spec column to fewer category columns in the compressed CSV.">
                                    <ArrowUpRightIcon className="w-5 h-5" />
                                </NavLink>
                            </td>
                            <td>
                                <button
                                    onClick={() => handleCompressing(file.file_name)}
                                    disabled={file.status !== 'Complete'}
                                    className={`btn btn-circle btn-xs ${file.status !== 'Complete' ? 'btn-disabled' : 'btn-ghost'}`}
                                    title="Create a compressed CSV based on specs CSV and and Mapping data with fewer columns"
                                >
                                    <PlayIcon className="w-5 h-5" />
                                </button>
                            </td>
                            <td>
                                <NavLink to={`/file?filepath=data/input/input_${file.file_name}`} className={`btn btn-circle btn-xs btn-ghost`}>
                                    <ArrowUpRightIcon className="w-5 h-5" />
                                </NavLink>
                            </td>
                            <td>
                                <NavLink to={`/file?filepath=data/specs/specs_${file.file_name}`} className={`btn btn-circle btn-xs btn-ghost`}>
                                    <ArrowUpRightIcon className="w-5 h-5" />
                                </NavLink>
                            </td>
                            <td>
                                <NavLink to={`/file?filepath=data/compressed/compressed_${file.file_name}`} className={`btn btn-circle btn-xs btn-ghost`}>
                                    <ArrowUpRightIcon className="w-5 h-5" />
                                </NavLink>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            {processStatus && <div className="mt-4 text-sm font-semibold">{processStatus}</div>}
            {compressStatus && <div className="mt-4 text-sm font-semibold">{compressStatus}</div>}
        </div>
    );
}

export default function Files() {
    return (
        <div className="p-6 space-y-4">
            <Suspense fallback={<div>Loading...</div>}>
                <FilesTable />
            </Suspense>
        </div>
    );
}
