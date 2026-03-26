import { NavLink } from 'react-router-dom'

const links = [
  ['Dashboard', '/dashboard'],
  ['Customers', '/customers'],
  ['Segments', '/segments'],
  ['Campaigns', '/campaigns'],
  ['Models', '/models'],
  ['AI Advisor', '/ai-advisor'],
]

function Sidebar() {
  return (
    <aside className="w-full md:w-64 bg-ink text-cream p-4 md:p-6 rounded-2xl shadow-xl">
      <h1 className="font-display text-xl mb-6">Segmentation OS</h1>
      <nav className="space-y-2">
        {links.map(([label, href]) => (
          <NavLink
            key={href}
            to={href}
            className={({ isActive }) =>
              `block rounded-lg px-3 py-2 transition ${isActive ? 'bg-coral text-white' : 'hover:bg-white/10'}`
            }
          >
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar
