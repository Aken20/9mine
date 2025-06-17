// Security utilities for Web3 applications

/**
 * Validates if a string is a valid Ethereum address
 */
export function isValidAddress(address: string): boolean {
  return /^0x[a-fA-F0-9]{40}$/.test(address)
}

/**
 * Sanitizes user input to prevent XSS attacks
 */
export function sanitizeInput(input: string): string {
  return input.replace(/[<>"']/g, "")
}

/**
 * Validates transaction amount
 */
export function isValidAmount(amount: string): boolean {
  const num = Number.parseFloat(amount)
  return !isNaN(num) && num > 0 && num < Number.MAX_SAFE_INTEGER
}

/**
 * Rate limiting helper
 */
export class RateLimiter {
  private requests: Map<string, number[]> = new Map()

  constructor(
    private maxRequests = 10,
    private windowMs = 60000, // 1 minute
  ) {}

  isAllowed(identifier: string): boolean {
    const now = Date.now()
    const requests = this.requests.get(identifier) || []

    // Remove old requests outside the window
    const validRequests = requests.filter((time) => now - time < this.windowMs)

    if (validRequests.length >= this.maxRequests) {
      return false
    }

    validRequests.push(now)
    this.requests.set(identifier, validRequests)
    return true
  }
}

/**
 * Contract interaction safety checks
 */
export function validateContractInteraction(
  contractAddress: string,
  functionName: string,
  args: any[],
): { isValid: boolean; error?: string } {
  if (!isValidAddress(contractAddress)) {
    return { isValid: false, error: "Invalid contract address" }
  }

  if (!functionName || typeof functionName !== "string") {
    return { isValid: false, error: "Invalid function name" }
  }

  // Add more validation as needed
  return { isValid: true }
}
