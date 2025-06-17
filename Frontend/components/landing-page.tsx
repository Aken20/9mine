import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CustomConnectButton } from "@/components/custom-connect-button"
import { Shield, Wallet, Zap, Globe } from "lucide-react"

export function LandingPage() {
  return (
    <div className="text-center space-y-12">
      <div className="space-y-4">
        <h2 className="text-5xl font-bold text-white mb-4">Welcome to 9mine</h2>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto">
          Connect your wallet and explore the future of decentralized mining and blockchain technology. Interact with
          smart contracts, manage your assets, and be part of the Web3 revolution.
        </p>
      </div>

      <div className="flex justify-center">
        <CustomConnectButton />
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-12">
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <Wallet className="h-8 w-8 text-blue-400 mb-2" />
            <CardTitle className="text-white">Multi-Wallet Support</CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription className="text-gray-300">
              Connect with MetaMask, WalletConnect, and other popular wallets
            </CardDescription>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <Shield className="h-8 w-8 text-green-400 mb-2" />
            <CardTitle className="text-white">Secure & Safe</CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription className="text-gray-300">
              Built with security best practices and robust error handling
            </CardDescription>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <Zap className="h-8 w-8 text-yellow-400 mb-2" />
            <CardTitle className="text-white">Fast Transactions</CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription className="text-gray-300">
              Optimized for speed with real-time transaction monitoring
            </CardDescription>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <Globe className="h-8 w-8 text-purple-400 mb-2" />
            <CardTitle className="text-white">Multi-Chain</CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription className="text-gray-300">
              Support for Ethereum, Polygon, Arbitrum, and more networks
            </CardDescription>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
