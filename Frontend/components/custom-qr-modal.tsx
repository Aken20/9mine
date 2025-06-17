"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Copy, ExternalLink, X } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface CustomQRModalProps {
  isOpen: boolean
  onClose: () => void
  uri?: string
  walletName?: string
}

export function CustomQRModal({ isOpen, onClose, uri, walletName }: CustomQRModalProps) {
  const [qrDataUrl, setQrDataUrl] = useState<string>("")
  const { toast } = useToast()

  useEffect(() => {
    if (uri && isOpen) {
      // Create a simple QR code placeholder
      // In a real implementation, you'd use a QR code library
      const canvas = document.createElement("canvas")
      const ctx = canvas.getContext("2d")
      canvas.width = 200
      canvas.height = 200

      if (ctx) {
        // Simple placeholder pattern
        ctx.fillStyle = "#000000"
        ctx.fillRect(0, 0, 200, 200)
        ctx.fillStyle = "#ffffff"
        ctx.fillRect(10, 10, 180, 180)
        ctx.fillStyle = "#000000"
        ctx.font = "12px monospace"
        ctx.fillText("QR Code", 70, 100)
        ctx.fillText("Placeholder", 60, 120)

        setQrDataUrl(canvas.toDataURL())
      }
    }
  }, [uri, isOpen])

  const copyUri = () => {
    if (uri) {
      navigator.clipboard.writeText(uri)
      toast({
        title: "Copied",
        description: "Connection URI copied to clipboard",
      })
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md bg-slate-800 border-slate-700">
        <DialogHeader>
          <DialogTitle className="text-white flex items-center justify-between">
            Connect with {walletName || "Wallet"}
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </DialogTitle>
        </DialogHeader>

        <div className="flex flex-col items-center space-y-4 p-4">
          {qrDataUrl && (
            <div className="bg-white p-4 rounded-lg">
              <img src={qrDataUrl || "/placeholder.svg"} alt="QR Code" className="w-48 h-48" />
            </div>
          )}

          <p className="text-sm text-gray-300 text-center">Scan this QR code with your wallet app to connect</p>

          <div className="flex gap-2 w-full">
            <Button onClick={copyUri} variant="outline" className="flex-1">
              <Copy className="h-4 w-4 mr-2" />
              Copy URI
            </Button>
            <Button onClick={() => window.open(uri, "_blank")} variant="outline" disabled={!uri}>
              <ExternalLink className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
