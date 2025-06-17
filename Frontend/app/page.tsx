"use client"

import { useAccount } from "wagmi"
import { Dashboard } from "@/components/dashboard"
import { LandingPage } from "@/components/landing-page"
import { CustomConnectButton } from "@/components/custom-connect-button"

export default function Home() {
  const { isConnected } = useAccount()

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        <header className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-white">9mine</h1>
          <CustomConnectButton />
        </header>

        {isConnected ? <Dashboard /> : <LandingPage />}
      </div>
    </main>
  )
}
