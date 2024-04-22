"use server"
import { myGetCookie } from "@/lib/auth";

export const userOrders = async () => {
    const isCookies = await myGetCookie()
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/orders`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${isCookies}`
            }
        })
        const data = await response.json()
        return data
    }
    catch (error) {
        console.log(error, "error");
        console.log("error is error");
    }
}