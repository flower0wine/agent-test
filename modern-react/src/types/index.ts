export interface User {
  id: string
  name: string
  email: string
  avatar?: string
}

export interface ApiResponse<T> {
  data: T
  message: string
  success: boolean
  timestamp: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  totalPages: number
}

export type Theme = 'light' | 'dark' | 'system'

export interface AppConfig {
  theme: Theme
  language: string
  notifications: boolean
}
