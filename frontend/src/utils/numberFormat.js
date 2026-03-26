export function formatCompactIndian(value, digits = 1) {
  const num = Number(value || 0)
  if (!Number.isFinite(num)) return '0'

  const abs = Math.abs(num)
  if (abs >= 10000000) {
    return `${(num / 10000000).toFixed(digits).replace(/\.0+$/, '')}Cr`
  }
  if (abs >= 100000) {
    return `${(num / 100000).toFixed(digits).replace(/\.0+$/, '')}L`
  }
  if (abs >= 1000) {
    return `${(num / 1000).toFixed(digits).replace(/\.0+$/, '')}K`
  }
  return `${num.toFixed(0)}`
}

export function formatCurrencyCompactIndian(value, digits = 1) {
  return `₹${formatCompactIndian(value, digits)}`
}

export function formatIndianNumber(value) {
  const num = Number(value || 0)
  if (!Number.isFinite(num)) return '0'
  return new Intl.NumberFormat('en-IN', { maximumFractionDigits: 2 }).format(num)
}

export function formatDecimal(value, digits = 2) {
  const num = Number(value || 0)
  if (!Number.isFinite(num)) return '0'
  return num.toFixed(digits)
}
