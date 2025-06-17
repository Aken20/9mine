"use client"

import { RainbowKitProvider, darkTheme } from "@rainbow-me/rainbowkit"
import { APP_CONFIG } from "@/lib/config"
import type React from "react"

// Custom theme to handle prop issues
const customDarkTheme = darkTheme({
  accentColor: "#7c3aed",
  accentColorForeground: "white",
  borderRadius: "medium",
  fontStack: "system",
  overlayBlur: "small",
})

interface RainbowKitWrapperProps {
  children: React.ReactNode
}

export function RainbowKitWrapper({ children }: RainbowKitWrapperProps) {
  return (
    <RainbowKitProvider
      theme={customDarkTheme}
      appInfo={{
        appName: APP_CONFIG.name,
        learnMoreUrl: APP_CONFIG.url,
        disclaimer: ({ Text, Link }) => (
          <Text>
            By connecting your wallet, you agree to the <Link href="/terms">Terms of Service</Link> and acknowledge you
            have read and understand the protocol <Link href="/disclaimer">Disclaimer</Link>
          </Text>
        ),
      }}
      modalSize="compact"
      initialChain={1} // Ethereum mainnet
    >
      {children}
    </RainbowKitProvider>
  )
}
