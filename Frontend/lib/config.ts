// Configuration constants for the 9mine application
export const APP_CONFIG = {
  name: "9mine",
  description: "Decentralized mining and blockchain platform",
  url: "https://9mine.com",
  walletConnect: {
    projectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID || "",
    metadata: {
      name: "9mine",
      description: "Decentralized mining platform",
      url: "https://9mine.com",
      icons: ["https://9mine.com/icon.png"],
    },
  },
} as const

// Validate required environment variables
export function validateConfig() {
  const requiredEnvVars = {
    NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID,
  }

  const missing = Object.entries(requiredEnvVars)
    .filter(([_, value]) => !value)
    .map(([key]) => key)

  if (missing.length > 0) {
    console.warn(
      `Missing environment variables: ${missing.join(", ")}. ` +
        "Some features may not work correctly. " +
        "Please check your .env.local file.",
    )
  }

  return missing.length === 0
}
