# Fight Prediction Frontend

A modern Next.js application for fight prediction using machine learning ensemble models.

## 🚀 Tech Stack

- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4 + ShadCN/UI components
- **Backend**: Convex (real-time database + functions)
- **Authentication**: Clerk (auth + billing)
- **Charts**: Recharts + ShadCN Chart components
- **Deployment**: Vercel

## 📦 Dependencies Installed

### Core Dependencies
- **next** (16.0.3) - React framework
- **react** (19.2.0) - UI library
- **typescript** (^5) - Type safety

### UI & Styling
- **tailwindcss** (^4) - Utility-first CSS
- **@radix-ui/react-*** - Accessible UI primitives
- **lucide-react** (^0.553.0) - Icon library
- **class-variance-authority** - Component variants
- **clsx** + **tailwind-merge** - Conditional styling

### Backend & Data
- **convex** (^1.29.0) - Real-time database
- **@clerk/nextjs** (^6.35.1) - Authentication & billing

### Charts & Visualization
- **recharts** (^2.15.4) - Chart library
- **date-fns** (^4.1.0) - Date utilities

### Forms & Validation
- **react-hook-form** (^7.66.0) - Form handling
- **zod** (^4.1.2) - Schema validation
- **@hookform/resolvers** - Form validation

### ShadCN Components Installed
- ✅ **button** - Clickable elements
- ✅ **card** - Content containers
- ✅ **input** - Form inputs
- ✅ **form** - Form components
- ✅ **table** - Data tables
- ✅ **badge** - Status indicators
- ✅ **chart** - Data visualization
- ✅ **label** - Form labels

## 📁 Project Structure

```
fight-prediction-frontend/
├── app/                          # Next.js App Router
│   ├── page.tsx                 # Dashboard home
│   ├── layout.tsx               # Root layout
│   ├── globals.css              # Global styles
│   ├── predict/                 # Prediction pages
│   │   └── page.tsx
│   ├── analytics/               # Analytics pages
│   │   └── page.tsx
│   └── settings/                # Settings pages
│       └── page.tsx
├── components/                   # React components
│   ├── ui/                      # ShadCN base components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── chart.tsx
│   │   └── ...
│   ├── features/                # Feature-specific components
│   │   ├── prediction/          # Prediction components
│   │   ├── analytics/           # Analytics components
│   │   └── billing/             # Billing components
│   └── layout/                  # Layout components
│       ├── header.tsx
│       ├── sidebar.tsx
│       └── footer.tsx
├── convex/                      # Backend functions
│   ├── _generated/              # Auto-generated types
│   ├── schema.ts                # Database schema
│   └── functions.ts             # API functions
├── lib/                         # Utilities
│   └── utils.ts                 # Helper functions
├── public/                      # Static assets
└── styles/                      # Additional styles
```

## 🛠 Development Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Format code with Prettier
npx prettier --write .
```

## 🔧 Configuration Files

- **package.json** - Dependencies and scripts
- **tsconfig.json** - TypeScript configuration
- **tailwind.config.ts** - Tailwind CSS configuration
- **components.json** - ShadCN configuration
- **eslint.config.mjs** - ESLint configuration
- **.prettierrc** - Prettier configuration
- **.env.local** - Environment variables (auto-generated)
- **.env.example** - Environment template

## 🌟 Key Features Ready to Implement

### Already Configured
- ✅ TypeScript end-to-end type safety
- ✅ Tailwind CSS with ShadCN components
- ✅ Convex real-time database setup
- ✅ Clerk authentication integration ready
- ✅ Chart visualization components
- ✅ Form handling and validation
- ✅ Responsive design utilities

### Next Steps
1. **Setup Clerk** - Add authentication keys
2. **Define Convex Schema** - Database structure
3. **Create Core Components** - Dashboard, prediction forms
4. **Integrate ML Backend** - Connect to Python ensemble
5. **Deploy to Vercel** - Production deployment

## 🔗 Integration Points

### ML Backend Integration
The frontend will connect to the existing Python ML ensemble via:
- API routes in `app/api/`
- Convex functions for data persistence
- Real-time prediction updates

### Current ML System
- **Flask Dashboard**: `../dashboard/` (legacy)
- **Python Ensemble**: `../prediction/predict_ensemble.py`
- **Models**: `../models/ensemble/` (trained models)
- **Data**: `../data/event_normalized_large_dataset.csv`

## 🚀 Ready for Development!

All dependencies are installed and the project structure is ready. You can now:

1. Start the development server: `npm run dev`
2. Begin implementing components
3. Set up Clerk authentication
4. Define Convex schema
5. Connect to the ML backend

The foundation is solid and follows modern React/Next.js best practices!
