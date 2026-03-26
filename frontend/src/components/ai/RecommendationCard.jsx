function RecommendationCard({ title, body }) {
  return (
    <div className="bg-white rounded-xl p-4 border border-zinc-100">
      <h3 className="font-display text-lg">{title}</h3>
      <p className="text-sm text-zinc-600 mt-2 whitespace-pre-wrap">{body}</p>
    </div>
  )
}

export default RecommendationCard
