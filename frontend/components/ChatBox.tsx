"use client"

import { useState } from 'react';
import { LuMessageCircle } from "react-icons/lu";
import { RxCross2 } from "react-icons/rx"
import Markdown from 'react-markdown';
import { replyToUser } from './ChatData';
import { IoAdd } from "react-icons/io5";
import { createThread } from '@/actions/openai';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { SendIcon } from 'lucide-react';

const ChatBox = ({messages}: {messages?: string[]}) => {
    const [popupOpen, setPopupOpen] = useState(false);
    const [userInput, setUserInput] = useState("");
    const [chatMessages, setChatMessages] = useState<string[]>(messages? messages : []);
    // const [loading, setLoading] = useState(false);  

    const openPopup = () => {
        setPopupOpen(!popupOpen);
    };

    const handleUserInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUserInput(event.target.value);
    };

const handleSendMessage = () => {
    if (userInput.trim() !== "") {
        addUserMessage(userInput);
        respondToUser(userInput);
        setUserInput("");
    }
    };

const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
        handleSendMessage();
    }
};

const addUserMessage = (message: string) => {    
    setChatMessages((prevMessages) => [...prevMessages, message]);
};

const addBotMessage = (message: string) => {
    setChatMessages((prevMessages) => [...prevMessages, message]);
};

const create = async () => {
    await createThread();
    setChatMessages([]);
};

const respondToUser = async (userMessage: string) => {
    const messages = await replyToUser(userMessage);
    // Replace this with your chatbot logic
    setTimeout(() => {
        addBotMessage(messages);
    }, 500);
};

  return (
    <div>
        <button
            className="fixed bottom-4 right-4 inline-flex items-center justify-center text-sm font-medium disabled:pointer-events-none disabled:opacity-50 border rounded-full w-16 h-16 bg-black hover:bg-gray-700 m-0 cursor-pointer border-gray-200 bg-none p-0 normal-case leading-5 hover:text-gray-900"
            type="button" aria-haspopup="dialog" aria-expanded="false" data-state="closed"
            onClick={openPopup}
        >
            <LuMessageCircle className='text-white h-8 w-8'/>
        </button>

        {popupOpen && (
            <div style={{ boxShadow: '0 0 #0000, 0 0 #0000, 0 1px 2px 0 rgb(0 0 0 / 0.05)' }}
                className="fixed z-10 bottom-[calc(4rem+1.5rem)] p-1 right-0 mr-4 bg-white rounded-lg border border-[#e5e7eb] md:h-[400px] w-[400px] lg:h-[500px]">
                {/* Popup content */}
                <div className='flex items-center'>
                    <div className="flex w-full flex-col space-y-1.5 pb-3">
                        <h2 className="font-semibold text-lg tracking-tight text-black">Chatbot</h2>
                        <p className="text-sm text-[#6b7280] leading-3">Powered by Mendable and Vercel</p>
                    </div>
                    <div className="flex items-center justify-center w-12 h-12">
                        <IoAdd onClick={create} className='text-black border-none rounded-full hover:bg-slate-500 bg-inherit h-12 w-12'/>
                    </div>
                    <button
                        className="inline-flex items-center justify-center text-sm font-medium disabled:pointer-events-none disabled:opacity-50 border rounded-full w-12 h-12  hover:bg-gray-700 cursor-pointer border-gray-200 bg-none normal-case leading-5 hover:text-gray-900"
                        type="button" aria-haspopup="dialog" aria-expanded="false" data-state="closed"
                        onClick={openPopup}
                    >
                        <RxCross2 className='text-black border-none rounded-full hover:bg-slate-500 bg-inherit h-12 w-12'/>
                    </button>
                </div>
                <div>
                    <div className="pr-4 h-[474px]" style={{ minWidth: '100%', display: 'table' }}>
                        <div id="chatbox" className="p-4 h-80 overflow-y-auto">
                            {chatMessages.map((message, index) => (
                                <div
                                    key={index}
                                    className={`mb-2 ${index % 2 === 0 ? "text-right" : ""}`}
                                >
                                    <Markdown
                                        className={`${
                                            index % 2 === 0 ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-700"
                                        } rounded-lg py-2 px-4 inline-block`}
                                    >
                                        {message}
                                    </Markdown>
                                </div>
                            ))}
                        </div>
                    </div>
                    {/* Input box */}
                    <div className="flex fixed bottom-[calc(4rem+1.5rem)] w-[390px] items-center bg-gray-100 dark:bg-gray-900 px-4 py-3 rounded-b-lg">
                        <Input
                            id='user-input'
                            className="flex-1 bg-transparent border-none focus:ring-0 dark:text-white"
                            placeholder="Type your message..."
                            type="text"
                            value={userInput}
                            onChange={handleUserInput}
                            onKeyPress={handleKeyPress}
                        />
                        <Button 
                            id='send-button'
                            className="ml-2"
                            onClick={handleSendMessage}
                        >
                            <SendIcon className="h-5 w-5" />
                            <span className="sr-only">Send</span>
                        </Button>
                    </div>
                </div>
            </div>
        )}
    </div>
  );
};

export default ChatBox;