export default function Disclaimer() {
  return (
    <div className="mb-8 p-4 md:p-5 bg-amber-50/90 border border-amber-200/80 rounded-2xl flex gap-4">
      <span className="text-2xl flex-shrink-0">⚕️</span>
      <div>
        <p className="text-amber-900 font-medium text-sm">Medical Disclaimer</p>
        <p className="text-amber-800 text-sm mt-1 leading-relaxed">
          This tool is for educational and research purposes only. It is not a substitute for 
          professional medical advice, diagnosis, or treatment. Always consult a qualified 
          dermatologist or healthcare provider for medical concerns.
        </p>
      </div>
    </div>
  )
}
