"use client"

import { ConnectButton } from "@rainbow-me/rainbowkit"
import { Button } from "@/components/ui/button"
import { Wallet, ChevronDown, AlertCircle } from "lucide-react"

export function CustomConnectButton() {
  return (
    <ConnectButton.Custom>
      {({ account, chain, openAccountModal, openChainModal, openConnectModal, authenticationStatus, mounted }) => {
        const ready = mounted && authenticationStatus !== "loading"
        const connected =
          ready && account && chain && (!authenticationStatus || authenticationStatus === "authenticated")

        return (
          <div
            {...(!ready && {
              "aria-hidden": true,
              style: {
                opacity: 0,
                pointerEvents: "none",
                userSelect: "none",
              },
            })}
          >
            {(() => {
              if (!connected) {
                return (
                  <Button
                    onClick={openConnectModal}
                    className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white font-semibold px-6 py-2 rounded-lg transition-all duration-200 flex items-center gap-2 shadow-lg hover:shadow-xl"
                  >
                    <Wallet className="h-4 w-4" />
                    Connect Wallet
                  </Button>
                )
              }

              if (chain.unsupported) {
                return (
                  <Button
                    onClick={openChainModal}
                    variant="destructive"
                    className="font-semibold px-4 py-2 rounded-lg flex items-center gap-2"
                  >
                    <AlertCircle className="h-4 w-4" />
                    Wrong Network
                  </Button>
                )
              }

              return (
                <div className="flex gap-2">
                  <Button
                    onClick={openChainModal}
                    variant="outline"
                    className="bg-slate-800 border-slate-600 text-white hover:bg-slate-700 px-3 py-2 rounded-lg flex items-center gap-2 transition-all duration-200"
                  >
                    {chain.hasIcon && (
                      <div
                        className="rounded-full overflow-hidden"
                        style={{
                          background: chain.iconBackground,
                          width: 16,
                          height: 16,
                        }}
                      >
                        {chain.iconUrl && (
                          <img
                            alt={chain.name ?? "Chain icon"}
                            src={chain.iconUrl || "/placeholder.svg"}
                            style={{ width: 16, height: 16 }}
                            onError={(e) => {
                              // Fallback for broken images
                              e.currentTarget.style.display = "none"
                            }}
                          />
                        )}
                      </div>
                    )}
                    {chain.name}
                    <ChevronDown className="h-3 w-3" />
                  </Button>

                  <Button
                    onClick={openAccountModal}
                    className="bg-slate-800 border border-slate-600 text-white hover:bg-slate-700 px-4 py-2 rounded-lg flex items-center gap-2 transition-all duration-200"
                  >
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                    {account.displayName}
                    {account.displayBalance ? ` (${account.displayBalance})` : ""}
                    <ChevronDown className="h-3 w-3" />
                  </Button>
                </div>
              )
            })()}
          </div>
        )
      }}
    </ConnectButton.Custom>
  )
}
