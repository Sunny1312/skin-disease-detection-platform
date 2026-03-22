export default function Results({ result, uploadedImage }) {
  const rec = result.recommendations || {}
  const severityStyles = {
    low: 'bg-emerald-100 text-emerald-800 border-emerald-200',
    moderate: 'bg-amber-100 text-amber-800 border-amber-200',
    high: 'bg-rose-100 text-rose-800 border-rose-200',
    unknown: 'bg-slate-100 text-slate-700 border-slate-200',
  }
  const severityStyle = severityStyles[rec.severity] || severityStyles.unknown

  return (
    <div className="mt-10 space-y-8">
      {/* Main Prediction Card */}
      <section className="bg-white rounded-3xl shadow-card border border-slate-100 overflow-hidden">
        <div className="p-6 md:p-8">
          <h2 className="font-display text-xl font-semibold text-skin-dark mb-6 flex items-center gap-2">
            <span>📋</span> Your Result
          </h2>
          <div className="flex flex-col lg:flex-row gap-8">
            <div className="flex-shrink-0">
              {uploadedImage && (
                <img
                  src={uploadedImage}
                  alt="Your skin image"
                  className="w-full max-w-sm rounded-2xl object-cover border border-slate-100 shadow-sm"
                />
              )}
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-display text-2xl md:text-3xl font-semibold text-skin-primary">
                {result.disease}
              </p>
              <div className="flex flex-wrap gap-3 mt-4">
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-slate-100 rounded-xl">
                  <span className="text-slate-600 text-sm">Confidence</span>
                  <span className="font-semibold text-skin-dark">
                    {(result.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <span className={`inline-flex items-center px-4 py-2 rounded-xl border text-sm font-medium ${severityStyle}`}>
                  Severity: {rec.severity}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Disease Information - Detailed */}
      {(rec.description || rec.symptoms?.length || rec.causes?.length) && (
        <section className="bg-white rounded-3xl shadow-card border border-slate-100 overflow-hidden">
          <div className="p-6 md:p-8">
            <h2 className="font-display text-xl font-semibold text-skin-dark mb-6 flex items-center gap-2">
              <span>📖</span> About {result.disease}
            </h2>
            <div className="flex flex-col lg:flex-row gap-8">
              {rec.image && (
                <img
                  src={rec.image}
                  alt={result.disease}
                  className="w-full lg:w-80 h-56 lg:h-64 rounded-2xl object-cover flex-shrink-0"
                />
              )}
              <div className="flex-1 space-y-5">
                {rec.description && (
                  <p className="text-slate-600 leading-relaxed">{rec.description}</p>
                )}
                {rec.symptoms?.length > 0 && (
                  <div>
                    <h3 className="font-medium text-skin-dark mb-2">Common Symptoms</h3>
                    <ul className="space-y-1.5">
                      {rec.symptoms.map((s, i) => (
                        <li key={i} className="flex items-start gap-2 text-slate-600">
                          <span className="text-skin-accent mt-1">•</span>
                          <span>{s}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {rec.causes?.length > 0 && (
                  <div>
                    <h3 className="font-medium text-skin-dark mb-2">Possible Causes</h3>
                    <div className="flex flex-wrap gap-2">
                      {rec.causes.map((c, i) => (
                        <span
                          key={i}
                          className="px-3 py-1.5 bg-slate-100 rounded-lg text-slate-700 text-sm"
                        >
                          {c}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Product Cards with Images */}
      {rec.products?.length > 0 && (
        <section className="bg-white rounded-3xl shadow-card border border-slate-100 overflow-hidden">
          <div className="p-6 md:p-8">
            <h2 className="font-display text-xl font-semibold text-skin-dark mb-6 flex items-center gap-2">
              <span>🛒</span> Recommended Products
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {rec.products.map((product, i) => (
                <a
                  key={i}
                  href={product.url || '#'}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group bg-slate-50 rounded-2xl overflow-hidden border border-slate-100 hover:border-skin-accent/30 hover:shadow-soft transition-all block"
                >
                  <div className="aspect-square overflow-hidden bg-white">
                    <img
                      src={product.image}
                      alt={product.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      onError={(e) => {
                        e.target.src = 'https://picsum.photos/seed/product/300/300'
                      }}
                    />
                  </div>
                  <div className="p-4">
                    <h3 className="font-medium text-skin-dark line-clamp-2 group-hover:text-skin-primary transition-colors">
                      {product.name}
                    </h3>
                    <p className="text-slate-600 text-sm mt-1 line-clamp-2">{product.description}</p>
                    <div className="mt-3 text-xs font-semibold text-skin-primary uppercase tracking-wider">
                      View Product →
                    </div>
                  </div>
                </a>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Care Guide */}
      <section className="bg-white rounded-3xl shadow-card border border-slate-100 overflow-hidden">
        <div className="p-6 md:p-8">
          <h2 className="font-display text-xl font-semibold text-skin-dark mb-6 flex items-center gap-2">
            <span>💡</span> Care Recommendations
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            {rec.ingredients?.length > 0 && (
              <div className="p-4 bg-skin-muted/20 rounded-2xl">
                <h3 className="font-medium text-skin-dark mb-2">Ingredients to Look For</h3>
                <ul className="space-y-1.5 text-slate-600">
                  {rec.ingredients.map((ing, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-skin-accent" />
                      {ing}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {rec.remedies?.length > 0 && (
              <div className="p-4 bg-skin-muted/20 rounded-2xl">
                <h3 className="font-medium text-skin-dark mb-2">Basic Remedies</h3>
                <ul className="space-y-1.5 text-slate-600">
                  {rec.remedies.map((r, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-skin-accent" />
                      {r}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {rec.lifestyle?.length > 0 && (
              <div className="p-4 bg-skin-muted/20 rounded-2xl md:col-span-2">
                <h3 className="font-medium text-skin-dark mb-2">Lifestyle Tips</h3>
                <ul className="space-y-1.5 text-slate-600">
                  {rec.lifestyle.map((l, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-skin-accent" />
                      {l}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
          {rec.consult_when && (
            <div className="mt-6 p-5 bg-amber-50 border border-amber-200 rounded-2xl">
              <h3 className="font-medium text-amber-900 mb-2">When to See a Dermatologist</h3>
              <p className="text-amber-800 text-sm leading-relaxed">{rec.consult_when}</p>
            </div>
          )}
        </div>
      </section>

      {/* Grad-CAM */}
      {result.gradcam_image && (
        <section className="bg-white rounded-3xl shadow-card border border-slate-100 overflow-hidden">
          <div className="p-6 md:p-8">
            <h2 className="font-display text-xl font-semibold text-skin-dark mb-2 flex items-center gap-2">
              <span>🔬</span> AI Attention Map (Grad-CAM)
            </h2>
            <p className="text-slate-600 text-sm mb-6">
              Red regions show where the model focused when making its prediction.
            </p>
            <img
              src={`data:image/jpeg;base64,${result.gradcam_image}`}
              alt="Grad-CAM heatmap"
              className="w-full max-w-lg rounded-2xl border border-slate-100"
            />
          </div>
        </section>
      )}

      {/* All Probabilities */}
      {result.all_probabilities && (
        <details className="bg-white rounded-3xl shadow-card border border-slate-100 overflow-hidden group">
          <summary className="p-6 cursor-pointer font-medium text-skin-dark hover:bg-slate-50/50 transition-colors list-none flex items-center justify-between">
            <span>View All Predictions</span>
            <span className="text-slate-400 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div className="px-6 pb-6 pt-0 space-y-3">
            {Object.entries(result.all_probabilities)
              .sort((a, b) => b[1] - a[1])
              .map(([name, prob]) => (
                <div key={name} className="flex items-center gap-4">
                  <span className="w-48 text-sm text-slate-600 truncate">{name}</span>
                  <div className="flex-1 h-3 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-skin-primary to-skin-accent rounded-full transition-all"
                      style={{ width: `${prob * 100}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium text-skin-dark w-14">{(prob * 100).toFixed(1)}%</span>
                </div>
              ))}
          </div>
        </details>
      )}
    </div>
  )
}
