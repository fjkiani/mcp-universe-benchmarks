// Navigation Bar - Modern SaaS-style navigation
import { Link, useLocation } from 'react-router-dom'
import { Button } from '../common/Button'

export function Navbar() {
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-lg border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">HR</span>
            </div>
            <span className="font-bold text-lg text-gray-900 tracking-tight">
              Zeta OS
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              to="/"
              className={`text-sm font-bold tracking-tight transition-colors ${isActive('/')
                ? 'text-blue-600'
                : 'text-gray-900 hover:text-blue-600'
                }`}
            >
              PORTAL
            </Link>
            <Link
              to="/dashboard"
              className={`text-sm font-medium transition-colors ${isActive('/dashboard')
                ? 'text-blue-600'
                : 'text-gray-600 hover:text-gray-900'
                }`}
            >
              Management
            </Link>
            <Link
              to="/demo/agent"
              className={`text-sm font-medium transition-colors ${isActive('/demo/agent')
                ? 'text-blue-600'
                : 'text-gray-600 hover:text-gray-900'
                }`}
            >
              Receptionist
            </Link>
            <Link
              to="/demo/identity"
              className={`text-sm font-medium transition-colors ${isActive('/demo/identity')
                ? 'text-blue-600'
                : 'text-gray-600 hover:text-gray-900'
                }`}
            >
              Identity
            </Link>
          </div>

          {/* CTA Button */}
          <div className="flex items-center space-x-4">
            <Button
              variant="primary"
              size="sm"
              className="bg-gray-950 text-white hover:bg-black border-none"
              onClick={() => window.open('/portal', '_self')}
            >
              Launch Hub
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}

