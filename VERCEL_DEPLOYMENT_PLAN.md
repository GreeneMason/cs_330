# Vercel Deployment Plan - Predictr

## Overview
This document outlines the steps needed to deploy the Predictr UFC fight prediction application to Vercel.

## Prerequisites Checklist

### 1. Environment Variables
Ensure the following environment variables are configured in Vercel:
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - Clerk authentication public key
- `CLERK_SECRET_KEY` - Clerk authentication secret key
- `NEXT_PUBLIC_CONVEX_URL` - Convex backend URL
- `CONVEX_DEPLOYMENT` - Convex deployment identifier
- Any additional API keys for UFC data sources

### 2. Backend Services Status
- [x] **Convex Database** - Already configured and running
  - Database schema defined in `/convex` directory
  - API endpoints for predictions, fighters, users
  - Real-time subscriptions configured

- [ ] **Flask Backend** - Currently runs on port 8000
  - **Action Required**: Decide on deployment strategy:
    - Option A: Deploy Flask to separate service (Railway, Render, Heroku)
    - Option B: Convert Flask endpoints to Next.js API routes
    - Option C: Use Vercel serverless functions for Python

### 3. Authentication
- [x] **Clerk** - Already integrated
  - Sign-in/Sign-up flows working
  - User profile management
  - Dev mode authorization for masonmgreene@gmail.com

## Deployment Steps

### Phase 1: Pre-Deployment Preparation

#### 1.1 Code Cleanup
- [x] Remove unused imports from components
- [x] Ensure all components have proper error boundaries
- [ ] Remove any console.logs and debug statements
- [ ] Verify all TypeScript types are properly defined

#### 1.2 Configuration Files
- [ ] Create/verify `vercel.json` configuration:
```json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/.next",
  "devCommand": "cd frontend && npm run dev",
  "installCommand": "cd frontend && npm install",
  "framework": "nextjs",
  "regions": ["iad1"]
}
```

- [ ] Update `frontend/package.json` build scripts:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

#### 1.3 Environment Setup
- [ ] Create `.env.local` template file
- [ ] Document all required environment variables
- [ ] Set up Vercel environment variables in dashboard

### Phase 2: Flask Backend Decision

#### Option A: Separate Flask Deployment (Recommended)
1. Deploy Flask app to Railway/Render
2. Update frontend to call Flask API via environment variable
3. Configure CORS settings on Flask backend
4. Set `NEXT_PUBLIC_FLASK_API_URL` in Vercel

#### Option B: Convert to Next.js API Routes
1. Convert `/backend/app.py` endpoints to `/frontend/app/api/*`
2. Rewrite Python logic in TypeScript/JavaScript
3. May require retraining models in JavaScript-compatible format

#### Option C: Vercel Python Functions
1. Use Vercel's Python runtime for serverless functions
2. Adapt Flask routes to Vercel function format
3. Note: Cold start times may be slower

### Phase 3: Database & ML Models

#### 3.1 Convex Setup
- [x] Convex is already configured
- [ ] Verify production Convex deployment
- [ ] Ensure all schema migrations are applied
- [ ] Test real-time subscriptions in production

#### 3.2 ML Models
- [ ] Verify model files location and accessibility
- [ ] Current models in `/models` directory:
  - Ensemble models
  - Neural network models
  - Feature files
- [ ] Decision: Host models where Flask backend runs OR convert to ONNX for browser

### Phase 4: Frontend Deployment

#### 4.1 Connect to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Link project
cd frontend
vercel link
```

#### 4.2 Configure Project
1. Set project name: `predictr` or `ufc-predictr`
2. Set framework preset: Next.js
3. Set root directory: `frontend`
4. Configure build settings

#### 4.3 Environment Variables in Vercel
```bash
# Via CLI
vercel env add NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
vercel env add CLERK_SECRET_KEY
vercel env add NEXT_PUBLIC_CONVEX_URL

# Or via Vercel Dashboard:
# Settings → Environment Variables → Add
```

### Phase 5: Testing & Optimization

#### 5.1 Pre-Deployment Tests
- [ ] Test authentication flow
- [ ] Test prediction creation
- [ ] Test fighter search
- [ ] Test profile management
- [ ] Verify Dev Mode access restriction

#### 5.2 Performance Optimization
- [ ] Enable Next.js Image Optimization
- [ ] Implement lazy loading for heavy components
- [ ] Add loading states for all async operations
- [ ] Optimize bundle size:
  ```bash
  npm run build
  # Review bundle analyzer output
  ```

#### 5.3 Production Build Test
```bash
cd frontend
npm run build
npm run start
# Test locally on http://localhost:3000
```

### Phase 6: Deployment

#### 6.1 Initial Deployment
```bash
cd frontend
vercel --prod
```

#### 6.2 Post-Deployment Verification
- [ ] Visit production URL
- [ ] Test all navigation routes
- [ ] Verify authentication works
- [ ] Create test prediction
- [ ] Check Convex real-time updates
- [ ] Test on mobile devices
- [ ] Verify Dev Mode access control

### Phase 7: Domain & DNS (Optional)

#### 7.1 Custom Domain Setup
1. Purchase domain (e.g., predictr.app)
2. Add domain in Vercel dashboard
3. Configure DNS records
4. Wait for SSL certificate provisioning

## Current Project Structure

```
cs_330/
├── frontend/                 # Next.js app (DEPLOY THIS)
│   ├── app/                 # App router pages
│   ├── components/          # React components
│   ├── convex/             # Convex client config
│   └── package.json
├── backend/                 # Flask API (NEEDS SEPARATE HOSTING)
│   ├── app.py
│   └── requirements.txt
├── convex/                  # Convex backend (ALREADY HOSTED)
│   └── schema & functions
├── models/                  # ML models (HOST WITH FLASK)
│   ├── ensemble/
│   └── neural_network/
└── data/                    # Training data (NOT NEEDED IN PRODUCTION)
```

## Deployment Checklist

### Critical Path
- [ ] Deploy Flask backend to external service
- [ ] Configure Flask backend URL in Vercel env vars
- [ ] Set up all Clerk environment variables
- [ ] Set up all Convex environment variables
- [ ] Deploy frontend to Vercel
- [ ] Test production deployment end-to-end

### Optional Enhancements
- [ ] Set up custom domain
- [ ] Configure analytics (Vercel Analytics)
- [ ] Set up error monitoring (Sentry)
- [ ] Enable preview deployments for branches
- [ ] Configure GitHub integration for auto-deploys

## Post-Deployment Monitoring

### Key Metrics to Track
- Page load times
- API response times
- Error rates
- Prediction accuracy trends
- User engagement metrics

### Monitoring Tools
- Vercel Analytics (built-in)
- Convex Dashboard (real-time data)
- Clerk Dashboard (authentication metrics)

## Rollback Plan
If deployment issues occur:
1. Revert to previous Vercel deployment via dashboard
2. Check Vercel logs for errors
3. Verify environment variables are correct
4. Test Convex connection
5. Verify Flask backend is accessible

## Cost Estimates

### Vercel
- Hobby Plan: Free (good for MVP)
- Pro Plan: $20/month (recommended for production)

### Convex
- Free tier: 1GB storage, 1M function calls/month
- Pro: Pay-as-you-go

### Flask Hosting (Railway/Render)
- Free tier: Available with limitations
- Paid: ~$5-20/month depending on usage

## Next Steps

1. **Immediate**: Deploy Flask backend to Railway or Render
2. **Today**: Configure all environment variables
3. **Today**: Run production build test locally
4. **Today**: Deploy to Vercel
5. **Tomorrow**: Monitor and fix any issues
6. **Week 1**: Optimize performance and user experience

## Support & Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Convex Production Deployment](https://docs.convex.dev/production)
- [Clerk Production Checklist](https://clerk.com/docs/deployments/production)

---

**Last Updated**: December 10, 2025
**Status**: Ready for deployment preparation
