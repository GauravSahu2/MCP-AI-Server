import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'AI Model Control Plane',
  description: 'High-Assurance AI Architecture Dashboard',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="theme-dark">
        {children}
      </body>
    </html>
  )
}
