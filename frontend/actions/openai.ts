"use server"
import { myGetCookie, setThreadID, getThreadID } from "@/lib/auth";

export const createThread = async () => {
    const isCookies = await myGetCookie()
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/openai/createthread`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${isCookies}`
            },
        })
        const data = await response.json()
        setThreadID(data.thread_id)
        return data.thread_id
    } catch (error) {
        console.log(error, "error");
        console.log("error is error");
    }
}

export const openaiapi = async (prompt: string) => {
    const token = await myGetCookie()
    let thread_id = await getThreadID()
    if (!thread_id) {
        await createThread()
    }
    
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/openai/userchat?prompt=${prompt}&thread_id=${thread_id}&token=${token}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
        })
        const data = await response.json()    
        return data.response
    } catch (error) {
        await createThread()
        console.log(error, "error");
        console.log("error is error");
    }
}

export const getMessages = async () => {
    const thread_id = await getThreadID()
    if (!thread_id) {
        console.error('thread_id is undefined');
        return;
    }
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/openai/getmessages?thread_id=${thread_id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        })
        const data = await response.json()
        return data
    } catch (error) {
        console.log(error, "error");
        console.log("error is error");
    }
}