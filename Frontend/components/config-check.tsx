"use client"

import { useEffect } from "react"
import { validateConfig } from "@/lib/config"
import { useToast } from "@/hooks/use-toast"

export function ConfigCheck() {
  const { toast } = useToast()

  useEffect(() => {
    const isValid = validateConfig()

    if (!isValid) {
      toast({
        title: "Configuration Warning",
        description: "Some environment variables are missing. Check the console for details.",
        variant: "destructive",
      })
    }
  }, [toast])

  return null
}
