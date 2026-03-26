import { Navigate, Route, Routes } from 'react-router-dom'
import Layout from './components/layout/Layout'
import AIAdvisor from './pages/AIAdvisor'
import Campaigns from './pages/Campaigns'
import Customers from './pages/Customers'
import Dashboard from './pages/Dashboard'
import Models from './pages/Models'
import Segments from './pages/Segments'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/customers" element={<Customers />} />
        <Route path="/segments" element={<Segments />} />
        <Route path="/campaigns" element={<Campaigns />} />
        <Route path="/models" element={<Models />} />
        <Route path="/ai-advisor" element={<AIAdvisor />} />
      </Routes>
    </Layout>
  )
}

export default App
