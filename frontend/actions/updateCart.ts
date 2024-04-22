"use server"
import { myGetCookie } from "@/lib/auth";

export const updateCart = async (product_id: string,product_size: string,quantity: number) => {
    const isCookies = await myGetCookie()
    try{
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/cart`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${isCookies}`
            },
            body: JSON.stringify({
                product_id: product_id,
                product_size: product_size,
                quantity: quantity,
        }),
        cache: 'no-cache',
    })
        const data = await response.json()
        return data
    } catch (error) {
        console.log(error, "error");
        console.log("error is error");
    }
}