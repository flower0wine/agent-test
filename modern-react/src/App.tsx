import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 text-gray-900 dark:text-gray-100">
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <header className="text-center mb-12">
          <div className="flex justify-center items-center gap-8 mb-8">
            <a href="https://vite.dev" target="_blank" rel="noopener noreferrer">
              <img
                src={viteLogo}
                className="logo h-24 w-24 transition-all duration-300 hover:scale-110 hover:drop-shadow-lg"
                alt="Vite logo"
              />
            </a>
            <a href="https://react.dev" target="_blank" rel="noopener noreferrer">
              <img
                src={reactLogo}
                className="logo react h-24 w-24 transition-all duration-300 hover:scale-110 hover:drop-shadow-lg animate-spin-slow"
                alt="React logo"
              />
            </a>
          </div>

          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
            Modern React + Vite
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            A modern React project with TypeScript, Tailwind CSS, and best practices
          </p>
        </header>

        <main className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          <div className="card bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl border border-gray-200 dark:border-gray-700">
            <h2 className="text-2xl font-semibold mb-4 text-primary-700 dark:text-primary-400">
              Counter Example
            </h2>
            <div className="flex flex-col items-center gap-6">
              <button
                onClick={() => setCount((count) => count + 1)}
                className="px-8 py-4 bg-gradient-to-r from-primary-500 to-primary-600 text-white font-semibold rounded-xl hover:from-primary-600 hover:to-primary-700 transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl"
              >
                Count is {count}
              </button>
              <p className="text-gray-600 dark:text-gray-400 text-center">
                Click the button to see React state management in action
              </p>
            </div>
          </div>

          <div className="card bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl border border-gray-200 dark:border-gray-700">
            <h2 className="text-2xl font-semibold mb-4 text-primary-700 dark:text-primary-400">
              Features
            </h2>
            <ul className="space-y-3">
              <li className="flex items-center gap-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                <span>React 19 with TypeScript</span>
              </li>
              <li className="flex items-center gap-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                <span>Vite for fast development</span>
              </li>
              <li className="flex items-center gap-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                <span>Tailwind CSS for styling</span>
              </li>
              <li className="flex items-center gap-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                <span>ESLint & Prettier for code quality</span>
              </li>
              <li className="flex items-center gap-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                <span>Modern folder structure</span>
              </li>
            </ul>
          </div>
        </main>

        <div className="text-center">
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Edit{' '}
            <code className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded font-mono">
              src/App.tsx
            </code>{' '}
            and save to test HMR
          </p>

          <div className="flex flex-wrap justify-center gap-4">
            <a
              href="https://react.dev"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gray-800 dark:bg-gray-700 text-white rounded-xl hover:bg-gray-900 dark:hover:bg-gray-600 transition-colors"
            >
              <span>React Docs</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                />
              </svg>
            </a>
            <a
              href="https://vite.dev"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition-colors"
            >
              <span>Vite Docs</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                />
              </svg>
            </a>
            <a
              href="https://tailwindcss.com"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 bg-cyan-600 text-white rounded-xl hover:bg-cyan-700 transition-colors"
            >
              <span>Tailwind Docs</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
