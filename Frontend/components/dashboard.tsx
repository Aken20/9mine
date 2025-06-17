"use client"
import { AccountInfo } from "./account-info"
import { TransactionPanel } from "./transaction-panel"
import { SmartContractInteraction } from "./smart-contract-interaction"
import { NetworkInfo } from "./network-info"

export function Dashboard() {
  return (
    <div className="space-y-8">
      <div className="grid md:grid-cols-2 gap-6">
        <AccountInfo />
        <NetworkInfo />
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <TransactionPanel />
        <SmartContractInteraction />
      </div>
    </div>
  )
}
