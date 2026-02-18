import React from 'react';
import Card from '../shared/Card';

export default function FilePreviewWidget({ fileUrl, fileName }) {
  // Supports PDF/image preview, fallback to download
  if (!fileUrl) return <Card title="File Preview">No file selected.</Card>;
  const isPdf = fileName?.toLowerCase().endsWith('.pdf');
  const isImage = /\.(jpg|jpeg|png|gif)$/i.test(fileName || '');
  return (
    <Card title="File Preview">
      {isPdf ? (
        <iframe src={fileUrl} title="PDF Preview" width="100%" height={400} />
      ) : isImage ? (
        <img src={fileUrl} alt={fileName} style={{ maxWidth: '100%', maxHeight: 400 }} />
      ) : (
        <a href={fileUrl} download={fileName}>Download {fileName}</a>
      )}
    </Card>
  );
}
