"use server"
import { IProducts } from "@/components/Products"
import { myGetCookie } from "@/lib/auth";

export const addToCart = async (size: string, product_data: IProducts, quantity:number) => {
    const isCookies = await myGetCookie()
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/cart`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${isCookies}`
            },
            body: JSON.stringify({
                product_id: product_data.sku,
                quantity: quantity,
                product_size: size
            }),
        })
        const data = await response.json()        
        return data
    } catch (error) {
        console.log(error, "error");
        console.log("error is error");
    }
}