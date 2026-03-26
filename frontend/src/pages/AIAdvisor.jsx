import { useQuery } from '@tanstack/react-query'
import { fetchRecommendations } from '../api/ai'
import GrokChatPanel from '../components/ai/GrokChatPanel'
import RecommendationCard from '../components/ai/RecommendationCard'

function AIAdvisor() {
  const { data } = useQuery({ queryKey: ['ai-recommendations'], queryFn: fetchRecommendations })

  const cards = [
    {
      title: 'Context Snapshot',
      body: data?.context || 'No context available yet.',
    },
    ...(data?.starter_prompts || []).map((p, idx) => ({ title: `Starter Prompt ${idx + 1}`, body: p })),
  ]

  return (
    <div className="grid lg:grid-cols-[1.2fr_1fr] gap-4">
      <GrokChatPanel />
      <div className="space-y-3">
        {cards.map((card) => (
          <RecommendationCard key={card.title} title={card.title} body={card.body} />
        ))}
      </div>
    </div>
  )
}

export default AIAdvisor
