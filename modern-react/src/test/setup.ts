import '@testing-library/jest-dom'
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'

// Automatically cleanup after each test
afterEach(() => {
  cleanup()
})

// Extend Vitest's expect with Testing Library's matchers
expect.extend({
  // Add custom matchers here if needed
})
