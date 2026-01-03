# Modern React Project

A modern React project built with Vite, TypeScript, Tailwind CSS, and best practices.

## 🚀 Features

- ⚡ **Vite** - Fast build tool and dev server
- ⚛️ **React 19** - Latest React with TypeScript
- 🎨 **Tailwind CSS** - Utility-first CSS framework
- 📝 **TypeScript** - Type safety and better developer experience
- 🔧 **ESLint & Prettier** - Code quality and formatting
- 🐶 **Husky & lint-staged** - Git hooks for pre-commit checks
- 🧪 **Vitest** - Fast unit testing with React Testing Library
- 📁 **Modern folder structure** - Organized and scalable

## 📦 Tech Stack

- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Vitest** - Testing framework
- **React Testing Library** - Component testing

## 🏗️ Project Structure

```
modern-react/
├── src/
│   ├── components/     # Reusable UI components
│   │   ├── Button/
│   │   └── Card/
│   ├── hooks/         # Custom React hooks
│   ├── utils/         # Utility functions
│   ├── types/         # TypeScript type definitions
│   ├── test/          # Test setup and utilities
│   ├── App.tsx        # Main App component
│   ├── main.tsx       # Application entry point
│   └── index.css      # Global styles
├── public/            # Static assets
├── .husky/            # Git hooks
├── .vscode/           # VS Code settings
└── config files       # Various configuration files
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn or pnpm

### Installation

1. Clone the repository
2. Install dependencies:

```bash
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Testing

Run tests:

```bash
npm run test
```

Run tests with UI:

```bash
npm run test:ui
```

Run tests with coverage:

```bash
npm run test:coverage
```

### Code Quality

Lint code:

```bash
npm run lint
```

Format code:

```bash
npm run format
```

## 🛠️ Configuration

### Tailwind CSS

Configuration file: `tailwind.config.js`

### TypeScript

Configuration files:

- `tsconfig.json` - Main TypeScript config
- `tsconfig.app.json` - App-specific config
- `tsconfig.node.json` - Node-specific config

### ESLint & Prettier

- `.eslintrc.js` - ESLint configuration
- `.prettierrc` - Prettier configuration
- `.prettierignore` - Files to ignore for formatting

### Vite

Configuration file: `vite.config.ts`

### Vitest

Configuration file: `vitest.config.ts`

## 📝 Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint code with ESLint
- `npm run format` - Format code with Prettier
- `npm run test` - Run tests with Vitest
- `npm run test:ui` - Run tests with UI
- `npm run test:coverage` - Run tests with coverage

## 🎯 Best Practices

### Component Structure

- Use functional components with TypeScript
- Follow single responsibility principle
- Use composition over inheritance
- Implement proper prop typing

### State Management

- Use React hooks for local state
- Consider context for global state
- Keep state as close as possible to where it's used

### Styling

- Use Tailwind CSS utility classes
- Extract repeated styles into components
- Follow responsive design principles

### Testing

- Write unit tests for components
- Test user interactions
- Mock external dependencies
- Maintain good test coverage

## 🔧 Development Tools

### VS Code Extensions

- ESLint
- Prettier
- Tailwind CSS IntelliSense
- TypeScript and JavaScript Language Features

### Git Hooks

- Pre-commit: Runs lint-staged to check and format code
- Pre-push: (Optional) Run tests before pushing

## 📚 Learn More

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vite.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [TypeScript Documentation](https://www.typescriptlang.org)
- [Vitest Documentation](https://vitest.dev)

## 📄 License

This project is licensed under the MIT License.
