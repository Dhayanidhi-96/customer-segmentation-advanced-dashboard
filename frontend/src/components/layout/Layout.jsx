import Header from './Header'
import Sidebar from './Sidebar'

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-aura p-4 md:p-8">
      <div className="max-w-7xl mx-auto grid md:grid-cols-[260px_1fr] gap-4 md:gap-6">
        <Sidebar />
        <main className="space-y-4 md:space-y-6 fade-in-up">
          <Header />
          {children}
        </main>
      </div>
    </div>
  )
}

export default Layout
