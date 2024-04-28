"use server"
import { getMessages, openaiapi } from "@/actions/openai";
import { cookies } from "next/headers";

export const replyToUser = async (userMessage: string) => {
    const messages = await openaiapi(userMessage);
    return messages;
}

export const getmessages = async () => {
    const messages = await getMessages();
    return messages;
}

export const checkThreadID = () => {
    const thread_id = cookies().has("thread_id")
    return thread_id
}