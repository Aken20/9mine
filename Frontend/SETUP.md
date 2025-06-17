# 9mine Web3 DApp Setup Guide

## Prerequisites

1. Node.js 18+ installed
2. A WalletConnect Project ID

## Getting Started

### 1. Get WalletConnect Project ID

1. Visit [WalletConnect Cloud](https://cloud.walletconnect.com)
2. Sign up or log in
3. Create a new project
4. Copy your Project ID

### 2. Environment Configuration

1. Copy `.env.example` to `.env.local`:
   \`\`\`bash
   cp .env.example .env.local
   \`\`\`

2. Update `.env.local` with your Project ID:
   \`\`\`env
   NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=your_actual_project_id_here
   \`\`\`

### 3. Install Dependencies

\`\`\`bash
npm install
\`\`\`

### 4. Run Development Server

\`\`\`bash
npm run dev
\`\`\`

## Troubleshooting

### WalletConnect 403 Error
- Ensure your Project ID is correct
- Check that your domain is added to the allowed origins in WalletConnect Cloud
- For localhost development, add `http://localhost:3000` to allowed origins

### NODE_ENV Client Error
- This has been fixed by removing client-side NODE_ENV access
- All environment checks now happen server-side only

## Production Deployment

1. Set environment variables in your hosting platform
2. Ensure your production domain is added to WalletConnect allowed origins
3. Build and deploy:
   \`\`\`bash
   npm run build
   npm start
