"use server"
import { myGetCookie } from "@/lib/auth"

export async function deleteCart(product_id: string, product_size: string, quantity: number) {
  const isCookies = await myGetCookie()
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/cart`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${isCookies}`
    },
    body: JSON.stringify({product_id, product_size, quantity})
  })
  return res.json()
}