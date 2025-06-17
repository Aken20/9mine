"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useReadContract, useWriteContract, useWaitForTransactionReceipt } from "wagmi"
import { useToast } from "@/hooks/use-toast"
import { Code, Loader2 } from "lucide-react"

// Example ERC-20 token ABI (simplified)
const ERC20_ABI = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "transfer",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const

export function SmartContractInteraction() {
  const [contractAddress, setContractAddress] = useState("")
  const [readAddress, setReadAddress] = useState("")
  const [writeToAddress, setWriteToAddress] = useState("")
  const [transferAmount, setTransferAmount] = useState("")
  const { toast } = useToast()

  // Read contract example
  const {
    data: balance,
    error: readError,
    refetch,
  } = useReadContract({
    address: contractAddress as `0x${string}`,
    abi: ERC20_ABI,
    functionName: "balanceOf",
    args: readAddress ? [readAddress as `0x${string}`] : undefined,
    query: {
      enabled: !!(contractAddress && readAddress),
    },
  })

  // Write contract example
  const { data: hash, error: writeError, isPending, writeContract } = useWriteContract()

  const { isLoading: isConfirming, isSuccess: isConfirmed } = useWaitForTransactionReceipt({
    hash,
  })

  const handleReadContract = () => {
    if (!contractAddress || !readAddress) {
      toast({
        title: "Missing Information",
        description: "Please provide both contract address and account address",
        variant: "destructive",
      })
      return
    }
    refetch()
  }

  const handleWriteContract = () => {
    if (!contractAddress || !writeToAddress || !transferAmount) {
      toast({
        title: "Missing Information",
        description: "Please fill in all fields",
        variant: "destructive",
      })
      return
    }

    try {
      writeContract({
        address: contractAddress as `0x${string}`,
        abi: ERC20_ABI,
        functionName: "transfer",
        args: [writeToAddress as `0x${string}`, BigInt(transferAmount)],
      })
    } catch (err) {
      toast({
        title: "Contract Interaction Failed",
        description: "Failed to interact with smart contract",
        variant: "destructive",
      })
    }
  }

  if (isConfirmed) {
    toast({
      title: "Transaction Confirmed",
      description: "Smart contract interaction successful",
    })
  }

  if (writeError) {
    toast({
      title: "Contract Error",
      description: writeError.message,
      variant: "destructive",
    })
  }

  return (
    <Card className="bg-slate-800/50 border-slate-700">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <Code className="h-5 w-5" />
          Smart Contract Interaction
        </CardTitle>
        <CardDescription className="text-gray-300">Interact with ERC-20 token contracts</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <Label htmlFor="contract" className="text-gray-300">
            Contract Address
          </Label>
          <Input
            id="contract"
            type="text"
            placeholder="0x..."
            value={contractAddress}
            onChange={(e) => setContractAddress(e.target.value)}
            className="bg-slate-700 border-slate-600 text-white"
          />
        </div>

        {/* Read Contract Section */}
        <div className="space-y-3">
          <h4 className="text-white font-medium">Read Contract (balanceOf)</h4>
          <div>
            <Label htmlFor="readAddress" className="text-gray-300">
              Account Address
            </Label>
            <Input
              id="readAddress"
              type="text"
              placeholder="0x..."
              value={readAddress}
              onChange={(e) => setReadAddress(e.target.value)}
              className="bg-slate-700 border-slate-600 text-white"
            />
          </div>
          <Button onClick={handleReadContract} variant="outline" className="w-full">
            Read Balance
          </Button>
          {balance !== undefined && (
            <div className="p-3 bg-slate-700 rounded-lg">
              <p className="text-sm text-gray-300">Balance:</p>
              <p className="text-white font-mono">{balance.toString()}</p>
            </div>
          )}
          {readError && (
            <div className="p-3 bg-red-900/20 border border-red-500 rounded-lg">
              <p className="text-red-400 text-sm">{readError.message}</p>
            </div>
          )}
        </div>

        {/* Write Contract Section */}
        <div className="space-y-3">
          <h4 className="text-white font-medium">Write Contract (transfer)</h4>
          <div>
            <Label htmlFor="writeToAddress" className="text-gray-300">
              To Address
            </Label>
            <Input
              id="writeToAddress"
              type="text"
              placeholder="0x..."
              value={writeToAddress}
              onChange={(e) => setWriteToAddress(e.target.value)}
              className="bg-slate-700 border-slate-600 text-white"
            />
          </div>
          <div>
            <Label htmlFor="amount" className="text-gray-300">
              Amount (in wei)
            </Label>
            <Input
              id="amount"
              type="number"
              placeholder="1000000000000000000"
              value={transferAmount}
              onChange={(e) => setTransferAmount(e.target.value)}
              className="bg-slate-700 border-slate-600 text-white"
            />
          </div>
          <Button onClick={handleWriteContract} disabled={isPending || isConfirming} className="w-full">
            {isPending || isConfirming ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                {isPending ? "Confirming..." : "Processing..."}
              </>
            ) : (
              "Transfer Tokens"
            )}
          </Button>
          {hash && (
            <div className="p-3 bg-slate-700 rounded-lg">
              <p className="text-sm text-gray-300">Transaction Hash:</p>
              <p className="text-xs text-blue-400 font-mono break-all">{hash}</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
