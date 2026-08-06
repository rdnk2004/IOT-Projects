# 🌿 PlantIQ — Smart Plant Care & Environmental Analytics Dashboard

[![Next.js 16](https://img.shields.io/badge/Next.js-16.0-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![React 19](https://img.shields.io/badge/React-19.0-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS v4](https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)

**PlantIQ** is a modern, responsive web application for monitoring plant health, tracking environmental telemetry (soil moisture, temperature, ambient light, humidity), and viewing smart care recommendations.

---

## ✨ Features

- **📊 Real-Time Metric Cards:** Track soil moisture levels, ambient temperature, humidity, and sunlight exposure.
- **📈 Interactive Trend Analytics:** Dynamic charts powered by `Recharts` visualizing historical environmental data.
- **🌱 Smart Care Insights:** Automated recommendations for watering, fertilizing, and sunlight adjustment based on live sensor metrics.
- **🎨 Modern Dark Design:** Built with React 19, Tailwind CSS v4, and Lucide React icons for a sleek user experience.

---

## 🛠️ Tech Stack

- **Framework:** [Next.js 16 App Router](https://nextjs.org/)
- **Library:** [React 19](https://react.dev/)
- **Language:** [TypeScript](https://www.typescriptlang.org/)
- **Styling:** [Tailwind CSS v4](https://tailwindcss.com/)
- **Charts:** [Recharts](https://recharts.org/)
- **Icons:** [Lucide React](https://lucide.dev/)

---

## 🚀 Getting Started

### Prerequisites

Make sure you have Node.js (v18+) and npm/yarn/pnpm installed.

### Installation

1. Navigate to the project directory:
   ```bash
   cd plantiq
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to view the application.

---

## 📁 Project Structure

```
plantiq/
├── public/              # Static assets and icons
├── src/                 # Application source code
│   └── app/             # Next.js App Router pages and components
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
└── next.config.ts       # Next.js configuration
```

---

## 📜 Available Scripts

- `npm run dev` — Launch Next.js development server
- `npm run build` — Build production distribution
- `npm run start` — Run production server
- `npm run lint` — Execute ESLint validation

---

## 📄 License

Part of the [IOT-Projects Monorepo](../README.md). MIT License.
