"use client"

import type React from "react"

import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { WagmiProvider } from "wagmi"
import { config } from "@/lib/wagmi"
import { useState } from "react"
import { ConfigCheck } from "@/components/config-check"
import { RainbowKitWrapper } from "@/components/rainbowkit-wrapper"

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())

  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitWrapper>
          <ConfigCheck />
          {children}
        </RainbowKitWrapper>
      </QueryClientProvider>
    </WagmiProvider>
  )
}
