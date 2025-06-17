"use client"

import { useToast } from "@/hooks/use-toast"
import { useCallback } from "react"

export function useWeb3Error() {
  const { toast } = useToast()

  const handleError = useCallback(
    (error: Error | unknown, context?: string) => {
      let title = "Web3 Error"
      let description = "An unexpected error occurred"

      if (error instanceof Error) {
        // Handle specific Web3 errors
        if (error.message.includes("User rejected")) {
          title = "Transaction Rejected"
          description = "You rejected the transaction in your wallet"
        } else if (error.message.includes("insufficient funds")) {
          title = "Insufficient Funds"
          description = "You don't have enough funds for this transaction"
        } else if (error.message.includes("network")) {
          title = "Network Error"
          description = "Please check your network connection and try again"
        } else if (error.message.includes("gas")) {
          title = "Gas Error"
          description = "Transaction failed due to gas estimation error"
        } else {
          description = error.message
        }
      }

      if (context) {
        title = `${context}: ${title}`
      }

      toast({
        title,
        description,
        variant: "destructive",
      })

      // Log error for debugging
      console.error("Web3 Error:", error)
    },
    [toast],
  )

  return { handleError }
}
