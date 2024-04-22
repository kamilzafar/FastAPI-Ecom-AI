"use server"
import { myGetCookie } from "@/lib/auth";

export const openaiapi = async (prompt: string) => {
    const isCookies = await myGetCookie()
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/openai?prompt=${prompt}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
        const data = await response.json()    
        return data.message
    } catch (error) {
        console.log(error, "error");
        console.log("error is error");
    }
}