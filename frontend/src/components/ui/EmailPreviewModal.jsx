function EmailPreviewModal({ open, onClose, subject, html }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl w-full max-w-2xl p-5">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-display text-xl">{subject}</h3>
          <button className="text-sm" onClick={onClose}>Close</button>
        </div>
        <div className="border rounded p-4" dangerouslySetInnerHTML={{ __html: html || '<p>No preview available.</p>' }} />
      </div>
    </div>
  )
}

export default EmailPreviewModal
