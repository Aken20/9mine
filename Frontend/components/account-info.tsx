"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useAccount, useBalance, useEnsName } from "wagmi"
import { formatEther } from "viem"
import { Copy, ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"

export function AccountInfo() {
  const { address, isConnected } = useAccount()
  const { data: balance } = useBalance({ address })
  const { data: ensName } = useEnsName({ address })
  const { toast } = useToast()

  const copyAddress = () => {
    if (address) {
      navigator.clipboard.writeText(address)
      toast({
        title: "Address copied",
        description: "Wallet address copied to clipboard",
      })
    }
  }

  const openEtherscan = () => {
    if (address) {
      window.open(`https://etherscan.io/address/${address}`, "_blank")
    }
  }

  if (!isConnected || !address) {
    return null
  }

  return (
    <Card className="bg-slate-800/50 border-slate-700">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          Account Information
          <Badge variant="secondary" className="bg-green-600">
            Connected
          </Badge>
        </CardTitle>
        <CardDescription className="text-gray-300">Your wallet details and balance</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {ensName && (
          <div>
            <label className="text-sm font-medium text-gray-400">ENS Name</label>
            <p className="text-white font-mono">{ensName}</p>
          </div>
        )}

        <div>
          <label className="text-sm font-medium text-gray-400">Address</label>
          <div className="flex items-center gap-2 mt-1">
            <p className="text-white font-mono text-sm">{`${address.slice(0, 6)}...${address.slice(-4)}`}</p>
            <Button variant="ghost" size="sm" onClick={copyAddress} className="h-6 w-6 p-0">
              <Copy className="h-3 w-3" />
            </Button>
            <Button variant="ghost" size="sm" onClick={openEtherscan} className="h-6 w-6 p-0">
              <ExternalLink className="h-3 w-3" />
            </Button>
          </div>
        </div>

        {balance && (
          <div>
            <label className="text-sm font-medium text-gray-400">Balance</label>
            <p className="text-white text-lg font-semibold">
              {Number.parseFloat(formatEther(balance.value)).toFixed(4)} {balance.symbol}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
