import React from 'react'
import { createThread, getMessages } from '@/actions/openai'
import { getThreadID } from '@/lib/auth'
import ChatBox from './ChatBox'
import CreateThread from './CreateThread'

const Chat = async () => {
  const threadid = await getThreadID()
  if (threadid) {
    const messages = await getMessages()
  return (
    <div>
      <ChatBox messages={messages} />
    </div>
  )
}
  else {
    return (
      <CreateThread />
    )
  }
}

export default Chat