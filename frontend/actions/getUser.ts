"use server"
import { myGetCookie } from "@/lib/auth";

export const getUser = async () =>{
    const isCookies = await myGetCookie()
    try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/users/me`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${isCookies}`
            },
            cache: 'no-cache',
        })
        const data = await res.json()      
        return data
    }
    catch (error) {
        console.log(error, "error");
        console.log("error is error");
    }
}