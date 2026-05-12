interface CardProps {
  title?: string
  children: React.ReactNode
  footer?: React.ReactNode
  className?: string
}

export function Card({ title, children, footer, className = '' }: CardProps) {
  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      )}
      <div>{children}</div>
      {footer && (
        <div className="mt-4 pt-4 border-t border-gray-200">{footer}</div>
      )}
    </div>
  )
}







