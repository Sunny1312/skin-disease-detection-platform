import { useState } from 'react'
import SkinUpload from './components/SkinUpload'
import Results from './components/Results'
import Disclaimer from './components/Disclaimer'

const API_BASE = 'http://localhost:8000'

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [uploadedImage, setUploadedImage] = useState(null)

  const handleUpload = async (file) => {
    setLoading(true)
    setError(null)
    setResult(null)
    setUploadedImage(URL.createObjectURL(file))

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || res.statusText || 'Prediction failed')
      }
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-skin-cream/30 to-teal-50/40">
      {/* Header */}
      <header className="border-b border-slate-200/80 bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-5">
          <h1 className="font-display text-2xl md:text-3xl font-semibold text-skin-dark tracking-tight">
            SkinSense
          </h1>
          <p className="text-slate-600 text-sm mt-0.5">
            AI-powered skin analysis with personalized care
          </p>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8 md:py-12">
        <Disclaimer />

        <SkinUpload onUpload={handleUpload} loading={loading} disabled={loading} />

        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-2xl text-red-700 flex items-center gap-3">
            <span className="text-xl">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {result && (
          <Results result={result} uploadedImage={uploadedImage} />
        )}
      </main>

      <footer className="text-center py-6 text-slate-500 text-sm">
        For educational purposes only • Always consult a dermatologist
      </footer>
    </div>
  )
}

export default App
