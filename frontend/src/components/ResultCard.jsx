const severityColor = {
  low:    { bg: "bg-green-50",  border: "border-green-200",  text: "text-green-800",  badge: "bg-green-100 text-green-800" },
  medium: { bg: "bg-yellow-50", border: "border-yellow-200", text: "text-yellow-800", badge: "bg-yellow-100 text-yellow-800" },
  high:   { bg: "bg-red-50",   border: "border-red-200",    text: "text-red-800",    badge: "bg-red-100 text-red-800" },
};

function getSeverity(confidence, isHealthy) {
  if (isHealthy) return "low";
  if (confidence > 85) return "high";
  if (confidence > 60) return "medium";
  return "low";
}

export default function ResultCard({ result }) {
  const { disease_name, is_healthy, confidence, medicines, prevention_tips, top_predictions } = result;
  const sev = getSeverity(confidence, is_healthy);
  const colors = severityColor[sev];

  return (
    <div className="space-y-4 mt-6">

      {/* Main disease card */}
      <div className={`rounded-2xl border p-5 ${colors.bg} ${colors.border}`}>
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">{is_healthy ? "✅" : "🔬"}</span>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${colors.badge}`}>
                {is_healthy ? "Healthy" : sev === "high" ? "Severe" : sev === "medium" ? "Moderate" : "Mild"}
              </span>
            </div>
            <h2 className={`text-xl font-bold ${colors.text}`}>{disease_name}</h2>
          </div>
          <div className="text-right shrink-0">
            <div className="text-2xl font-bold text-gray-800">{confidence.toFixed(1)}%</div>
            <div className="text-xs text-gray-500">confidence</div>
          </div>
        </div>

        {/* Confidence bar */}
        <div className="mt-4">
          <div className="w-full bg-white rounded-full h-2 border border-gray-200">
            <div
              className="h-2 rounded-full bg-green-500 transition-all duration-1000"
              style={{ width: `${confidence}%` }}
            />
          </div>
        </div>
      </div>

      {/* Medicines */}
      {!is_healthy && medicines.length > 0 && (
        <div className="bg-white rounded-2xl border border-gray-200 p-5">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xl">💊</span>
            <h3 className="font-bold text-gray-800">Recommended Treatments</h3>
          </div>
          <ul className="space-y-2">
            {medicines.map((med, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-green-500 mt-0.5">•</span>
                <span className="text-gray-700 text-sm">{med}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Prevention tips */}
      {prevention_tips.length > 0 && (
        <div className="bg-white rounded-2xl border border-gray-200 p-5">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xl">🛡️</span>
            <h3 className="font-bold text-gray-800">Prevention Tips</h3>
          </div>
          <ul className="space-y-2">
            {prevention_tips.map((tip, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-blue-400 mt-0.5">→</span>
                <span className="text-gray-700 text-sm">{tip}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Top predictions */}
      {top_predictions && top_predictions.length > 1 && (
        <div className="bg-white rounded-2xl border border-gray-200 p-5">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xl">📊</span>
            <h3 className="font-bold text-gray-800">Other Possibilities</h3>
          </div>
          <div className="space-y-2">
            {top_predictions.slice(1).map((pred, i) => (
              <div key={i} className="flex items-center justify-between text-sm">
                <span className="text-gray-600 truncate mr-3">{pred.label}</span>
                <div className="flex items-center gap-2 shrink-0">
                  <div className="w-24 bg-gray-100 rounded-full h-1.5">
                    <div
                      className="h-1.5 rounded-full bg-gray-400"
                      style={{ width: `${pred.confidence}%` }}
                    />
                  </div>
                  <span className="text-gray-500 w-10 text-right">{pred.confidence}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}