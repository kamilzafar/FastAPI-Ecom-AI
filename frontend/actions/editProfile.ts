"use server"
import { myGetCookie } from "@/lib/auth"

export const updateUser = async (username: string) => {
    const cookie = await myGetCookie()
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/user`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${cookie}`,
            },
            body: JSON.stringify(
                { username: username }
            )
        })
        const data = await response.json()
        return data
    }
    catch (error) {
        console.log(error, "error");
        console.log("error is error");
    }
}