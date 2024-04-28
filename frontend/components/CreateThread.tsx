"use client"
import { createThread } from '@/actions/openai';
import { getThreadID } from '@/lib/auth';
import React from 'react'
import { LuMessageCircle } from 'react-icons/lu'

const CreateThread = () => {
    const startConversation = async () => {
        await createThread();
    }

    const handleButtonClick = async (e: React.FormEvent) => {
        e.preventDefault()
        const threadid = await getThreadID()
        if (!threadid) {
            await startConversation()
        }
    }
  return (
    <div>
        <button
            className="fixed bottom-4 right-4 inline-flex items-center justify-center text-sm font-medium disabled:pointer-events-none disabled:opacity-50 border rounded-full w-16 h-16 bg-black hover:bg-gray-700 m-0 cursor-pointer border-gray-200 bg-none p-0 normal-case leading-5 hover:text-gray-900"
            type="button" aria-haspopup="dialog" aria-expanded="false" data-state="closed"
            onClick={handleButtonClick}
        >
            <LuMessageCircle className="w-8 h-8 text-white" />
        </button>
    </div>
  )
}

export default CreateThread