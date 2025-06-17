"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useChainId, useChains } from "wagmi"
import { Activity, Globe } from "lucide-react"

export function NetworkInfo() {
  const chainId = useChainId()
  const chains = useChains()
  const currentChain = chains.find((chain) => chain.id === chainId)

  return (
    <Card className="bg-slate-800/50 border-slate-700">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <Globe className="h-5 w-5" />
          Network Information
        </CardTitle>
        <CardDescription className="text-gray-300">Current blockchain network details</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {currentChain && (
          <>
            <div>
              <label className="text-sm font-medium text-gray-400">Network</label>
              <div className="flex items-center gap-2 mt-1">
                <p className="text-white font-semibold">{currentChain.name}</p>
                <Badge variant="outline" className="border-green-500 text-green-400">
                  <Activity className="h-3 w-3 mr-1" />
                  Active
                </Badge>
              </div>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-400">Chain ID</label>
              <p className="text-white">{currentChain.id}</p>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-400">Native Currency</label>
              <p className="text-white">
                {currentChain.nativeCurrency.name} ({currentChain.nativeCurrency.symbol})
              </p>
            </div>

            {currentChain.blockExplorers?.default && (
              <div>
                <label className="text-sm font-medium text-gray-400">Block Explorer</label>
                <a
                  href={currentChain.blockExplorers.default.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 underline"
                >
                  {currentChain.blockExplorers.default.name}
                </a>
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  )
}
