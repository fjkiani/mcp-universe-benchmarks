// Visual Constants - SaaS/YC Style Design System
// These drive the visual creativity, not just content

export const VISUAL_THEME = {
  // Color Palette
  colors: {
    primary: {
      light: '#3b82f6', // blue-500
      DEFAULT: '#2563eb', // blue-600
      dark: '#1d4ed8', // blue-700
      gradient: 'from-blue-600 to-purple-600'
    },
    success: {
      light: '#10b981', // emerald-500
      DEFAULT: '#059669', // emerald-600
      dark: '#047857', // emerald-700
      gradient: 'from-green-500 to-emerald-500'
    },
    warning: {
      light: '#f59e0b', // amber-500
      DEFAULT: '#d97706', // amber-600
      dark: '#b45309', // amber-700
      gradient: 'from-orange-500 to-red-500'
    },
    danger: {
      light: '#ef4444', // red-500
      DEFAULT: '#dc2626', // red-600
      dark: '#b91c1c', // red-700
      gradient: 'from-red-500 to-pink-500'
    }
  },

  // Gradients
  gradients: {
    hero: 'bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50',
    card: 'bg-gradient-to-br from-white to-gray-50',
    accent: 'bg-gradient-to-r from-blue-600 to-purple-600',
    success: 'bg-gradient-to-r from-green-500 to-emerald-500',
    warning: 'bg-gradient-to-r from-orange-500 to-red-500'
  },

  // Animations
  animations: {
    fadeIn: 'animate-fade-in',
    slideUp: 'animate-slide-up',
    scale: 'animate-scale',
    pulse: 'animate-pulse',
    blob: 'animate-blob',
    float: 'animate-float'
  },

  // Shadows
  shadows: {
    sm: 'shadow-sm',
    DEFAULT: 'shadow-md',
    lg: 'shadow-lg',
    xl: 'shadow-xl',
    '2xl': 'shadow-2xl',
    glow: 'shadow-lg shadow-blue-500/20',
    glowPurple: 'shadow-lg shadow-purple-500/20'
  },

  // Spacing Scale
  spacing: {
    section: 'py-20 px-4',
    container: 'max-w-7xl mx-auto',
    card: 'p-6',
    cardLarge: 'p-8'
  },

  // Typography
  typography: {
    hero: {
      headline: 'text-5xl md:text-7xl font-bold text-gray-900 leading-tight',
      subheadline: 'text-xl md:text-2xl text-gray-600 leading-relaxed'
    },
    section: {
      headline: 'text-4xl md:text-5xl font-bold text-gray-900',
      subheadline: 'text-xl text-gray-600'
    },
    card: {
      title: 'text-2xl font-bold text-gray-900',
      description: 'text-gray-600 leading-relaxed'
    }
  }
}

// Animation Presets
export const ANIMATION_PRESETS = {
  fadeInUp: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.5 }
  },
  scaleIn: {
    initial: { opacity: 0, scale: 0.9 },
    animate: { opacity: 1, scale: 1 },
    transition: { duration: 0.3 }
  },
  slideInRight: {
    initial: { opacity: 0, x: 20 },
    animate: { opacity: 1, x: 0 },
    transition: { duration: 0.5 }
  }
}

// Layout Presets
export const LAYOUT_PRESETS = {
  hero: {
    container: 'max-w-7xl mx-auto text-center',
    spacing: 'pt-24 pb-20 px-4',
    background: 'relative overflow-hidden bg-gradient-to-b from-white via-blue-50/50 to-white'
  },
  section: {
    container: 'max-w-7xl mx-auto',
    spacing: 'py-20 px-4',
    background: 'bg-white'
  },
  card: {
    base: 'bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300',
    padding: 'p-6',
    hover: 'transform hover:-translate-y-2 hover:scale-105'
  }
}

// Interactive States
export const INTERACTIVE_STATES = {
  button: {
    base: 'transition-all duration-300 transform',
    hover: 'hover:scale-105 hover:shadow-lg',
    active: 'active:scale-95'
  },
  card: {
    base: 'transition-all duration-500',
    hover: 'hover:shadow-2xl hover:-translate-y-3',
    focus: 'focus:ring-2 focus:ring-blue-500'
  },
  link: {
    base: 'transition-colors duration-200',
    hover: 'hover:text-blue-600'
  }
}

