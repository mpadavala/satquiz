import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { uploadPDF } from '../api/words'

const UploadPage = () => {
  const [file, setFile] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  const uploadMutation = useMutation({
    mutationFn: uploadPDF,
    onSuccess: (data) => {
      alert(`Successfully processed ${data.processed.length} words!`)
      setFile(null)
    },
    onError: (error) => {
      alert(`Upload failed: ${error.response?.data?.detail || error.message}`)
    },
  })

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.type === 'application/pdf') {
        setFile(droppedFile)
      } else {
        alert('Please upload a PDF file')
      }
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]
      if (selectedFile.type === 'application/pdf') {
        setFile(selectedFile)
      } else {
        alert('Please upload a PDF file')
      }
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (file) {
      uploadMutation.mutate(file)
    }
  }

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Upload SAT Word List PDF</h1>
        <p className="mt-2 text-gray-600">
          Upload a PDF file containing SAT vocabulary words. The system will automatically extract
          words and generate meanings and example sentences.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-8">
        <div
          className={`border-2 border-dashed rounded-lg p-12 text-center ${
            dragActive
              ? 'border-indigo-500 bg-indigo-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-upload"
            accept=".pdf"
            onChange={handleFileChange}
            className="hidden"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center"
          >
            <svg
              className="w-12 h-12 text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            <p className="text-gray-600 mb-2">
              <span className="font-semibold text-indigo-600">Click to upload</span> or drag and drop
            </p>
            <p className="text-sm text-gray-500">PDF files only</p>
          </label>
        </div>

        {file && (
          <div className="mt-4 p-4 bg-gray-50 rounded-md">
            <p className="text-sm text-gray-700">
              Selected file: <span className="font-medium">{file.name}</span>
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Size: {(file.size / 1024).toFixed(2)} KB
            </p>
          </div>
        )}

        <button
          type="submit"
          disabled={!file || uploadMutation.isPending}
          className="mt-6 w-full px-4 py-3 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          {uploadMutation.isPending ? 'Uploading and processing...' : 'Upload PDF'}
        </button>

        {uploadMutation.isSuccess && uploadMutation.data && (
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
            <h3 className="font-semibold text-green-800 mb-2">Upload Successful!</h3>
            <p className="text-sm text-green-700">
              Total words found: {uploadMutation.data.total_words_found}
            </p>
            <p className="text-sm text-green-700">
              Words processed: {uploadMutation.data.processed.length}
            </p>
            {uploadMutation.data.errors.length > 0 && (
              <p className="text-sm text-yellow-700 mt-2">
                Errors: {uploadMutation.data.errors.length}
              </p>
            )}
          </div>
        )}
      </form>
    </div>
  )
}

export default UploadPage
