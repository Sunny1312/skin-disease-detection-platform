import { useRef } from 'react'

export default function SkinUpload({ onUpload, loading, disabled }) {
  const inputRef = useRef(null)

  const handleDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
      onUpload(file)
    }
  }

  const handleChange = (e) => {
    const file = e.target.files[0]
    if (file) onUpload(file)
  }

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      className={`
        relative overflow-hidden rounded-3xl border-2 border-dashed transition-all duration-300
        ${disabled ? 'opacity-70 cursor-not-allowed' : 'cursor-pointer hover:border-skin-primary hover:bg-skin-primary/5'}
        ${loading ? 'border-skin-accent bg-skin-muted/20' : 'border-slate-300 bg-white/60'}
        shadow-soft
      `}
      onClick={() => !disabled && inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        onChange={handleChange}
        className="hidden"
      />
      <div className="p-12 md:p-16 text-center">
        {loading ? (
          <div className="space-y-4">
            <div className="w-16 h-16 mx-auto rounded-full border-4 border-skin-primary/30 border-t-skin-primary animate-spin" />
            <p className="text-skin-dark font-medium">Analyzing your image...</p>
            <p className="text-slate-500 text-sm">AI is examining skin patterns</p>
          </div>
        ) : (
          <>
            <div className="w-20 h-20 mx-auto rounded-2xl bg-skin-muted/50 flex items-center justify-center text-4xl mb-4">
              📷
            </div>
            <p className="text-lg font-medium text-slate-700">
              Drop a skin image here or click to upload
            </p>
            <p className="text-slate-500 text-sm mt-1">
              JPG, PNG • Clear, well-lit photos work best
            </p>
          </>
        )}
      </div>
    </div>
  )
}
