import { describe, it, expect } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the main heading', () => {
    render(<App />)
    expect(screen.getByText(/Modern React \+ Vite/i)).toBeInTheDocument()
  })

  it('renders the counter button', () => {
    render(<App />)
    expect(screen.getByText(/Count is 0/i)).toBeInTheDocument()
  })

  it('increments counter when button is clicked', () => {
    render(<App />)
    const button = screen.getByText(/Count is 0/i)
    fireEvent.click(button)
    expect(screen.getByText(/Count is 1/i)).toBeInTheDocument()
  })

  it('renders feature list', () => {
    render(<App />)
    expect(screen.getByText(/React 19 with TypeScript/i)).toBeInTheDocument()
    expect(screen.getByText(/Vite for fast development/i)).toBeInTheDocument()
    expect(screen.getByText(/Tailwind CSS for styling/i)).toBeInTheDocument()
  })
})
