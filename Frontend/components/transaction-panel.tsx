"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useAccount, useSendTransaction, useWaitForTransactionReceipt } from "wagmi"
import { parseEther, isAddress } from "viem"
import { useToast } from "@/hooks/use-toast"
import { Send, Loader2 } from "lucide-react"

export function TransactionPanel() {
  const [to, setTo] = useState("")
  const [amount, setAmount] = useState("")
  const { address } = useAccount()
  const { toast } = useToast()

  const { data: hash, error, isPending, sendTransaction } = useSendTransaction()

  const { isLoading: isConfirming, isSuccess: isConfirmed } = useWaitForTransactionReceipt({
    hash,
  })

  const handleSendTransaction = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!isAddress(to)) {
      toast({
        title: "Invalid Address",
        description: "Please enter a valid Ethereum address",
        variant: "destructive",
      })
      return
    }

    if (!amount || Number.parseFloat(amount) <= 0) {
      toast({
        title: "Invalid Amount",
        description: "Please enter a valid amount",
        variant: "destructive",
      })
      return
    }

    try {
      sendTransaction({
        to: to as `0x${string}`,
        value: parseEther(amount),
      })
    } catch (err) {
      toast({
        title: "Transaction Failed",
        description: "Failed to send transaction",
        variant: "destructive",
      })
    }
  }

  // Show success message when transaction is confirmed
  if (isConfirmed) {
    toast({
      title: "Transaction Confirmed",
      description: `Transaction ${hash} has been confirmed`,
    })
  }

  // Show error message
  if (error) {
    toast({
      title: "Transaction Error",
      description: error.message,
      variant: "destructive",
    })
  }

  return (
    <Card className="bg-slate-800/50 border-slate-700">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <Send className="h-5 w-5" />
          Send Transaction
        </CardTitle>
        <CardDescription className="text-gray-300">Send ETH to another address</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSendTransaction} className="space-y-4">
          <div>
            <Label htmlFor="to" className="text-gray-300">
              Recipient Address
            </Label>
            <Input
              id="to"
              type="text"
              placeholder="0x..."
              value={to}
              onChange={(e) => setTo(e.target.value)}
              className="bg-slate-700 border-slate-600 text-white"
              required
            />
          </div>

          <div>
            <Label htmlFor="amount" className="text-gray-300">
              Amount (ETH)
            </Label>
            <Input
              id="amount"
              type="number"
              step="0.001"
              placeholder="0.1"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="bg-slate-700 border-slate-600 text-white"
              required
            />
          </div>

          <Button type="submit" disabled={isPending || isConfirming || !address} className="w-full">
            {isPending || isConfirming ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                {isPending ? "Confirming..." : "Processing..."}
              </>
            ) : (
              "Send Transaction"
            )}
          </Button>

          {hash && (
            <div className="mt-4 p-3 bg-slate-700 rounded-lg">
              <p className="text-sm text-gray-300">Transaction Hash:</p>
              <p className="text-xs text-blue-400 font-mono break-all">{hash}</p>
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  )
}
