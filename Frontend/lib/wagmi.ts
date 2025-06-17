import { getDefaultConfig } from "@rainbow-me/rainbowkit"
import { arbitrum, base, mainnet, optimism, polygon, sepolia } from "wagmi/chains"
import { APP_CONFIG } from "./config"

export const config = getDefaultConfig({
  appName: APP_CONFIG.name,
  projectId: APP_CONFIG.walletConnect.projectId,
  chains: [mainnet, polygon, optimism, arbitrum, base, sepolia],
  ssr: true,
})
