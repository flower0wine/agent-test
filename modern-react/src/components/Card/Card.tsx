import type { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  title?: string
  className?: string
}

export const Card = ({ children, title, className = '' }: CardProps) => {
  return (
    <div
      className={`bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl border border-gray-200 dark:border-gray-700 ${className}`}
    >
      {title && (
        <h3 className="text-2xl font-semibold mb-6 text-primary-700 dark:text-primary-400">
          {title}
        </h3>
      )}
      <div className="space-y-4">{children}</div>
    </div>
  )
}
