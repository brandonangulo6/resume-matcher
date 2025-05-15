'use client'

import { useState } from 'react'

export default function Home() {
  const [resumeText, setResumeText] = useState('')
  const [jobText, setJobText] = useState('')
  const [matchScore, setMatchScore] = useState<number | null>(null)
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)

  const handleTextMatch = async () => {
    if (!resumeText || !jobText) return
    setLoading(true)
    try {
      const res = await fetch('http://localhost:5000/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume: resumeText, job: jobText }),
      })
      const data = await res.json()
      setMatchScore(data.match_score)
    } catch (error) {
      console.error('Error matching text:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePdfUpload = async () => {
    if (!resumeFile || !jobText) return
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', resumeFile)
      formData.append('job', jobText)

      const res = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      setMatchScore(data.match_score)
    } catch (error) {
      console.error('Error matching PDF:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="p-6 max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Resume-Job Matcher</h1>

      <div className="space-y-2">
        <textarea
          className="w-full p-2 border rounded"
          placeholder="Paste your resume text here..."
          rows={5}
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          disabled={loading}
        />
        <textarea
          className="w-full p-2 border rounded"
          placeholder="Paste the job description here..."
          rows={5}
          value={jobText}
          onChange={(e) => setJobText(e.target.value)}
          disabled={loading}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed"
          onClick={handleTextMatch}
          disabled={loading || !resumeText || !jobText}
        >
          {loading ? 'Matching...' : 'Match Using Text'}
        </button>
      </div>

      <div className="space-y-2">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
          disabled={loading}
        />
        {resumeFile && (
          <div className="flex items-center space-x-2 mt-1">
            <span>{resumeFile.name}</span>
            <button
              onClick={() => setResumeFile(null)}
              className="text-red-600 hover:underline"
              disabled={loading}
            >
              Remove
            </button>
          </div>
        )}
        <button
          className="bg-green-600 text-white px-4 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed"
          onClick={handlePdfUpload}
          disabled={loading || !resumeFile || !jobText}
        >
          {loading ? 'Matching...' : 'Match Using PDF Upload'}
        </button>
      </div>

      {matchScore !== null && (
        <div className="text-xl font-semibold mt-4">
          Match Score: {(matchScore * 100).toFixed(2)}%
          <p
            className={
              matchScore > 0.8
                ? 'text-green-600'
                : matchScore > 0.6
                ? 'text-yellow-600'
                : 'text-red-600'
            }
          >
            {matchScore > 0.8
              ? '🌟 Excellent Match'
              : matchScore > 0.6
              ? '✅ Good Match'
              : '⚠️ Low Match'}
          </p>
        </div>
      )}
    </main>
  )
}
