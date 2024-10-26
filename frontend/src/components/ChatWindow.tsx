import { useRef, useState } from 'react'
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageModel, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react'
import api from '../api';

function ChatWindow() {
    const BOT_NAME = "Jarvis";
    const inputRef = useRef<HTMLInputElement>(null);
    const [chatMessages, setChatMessages] = useState<MessageModel[]>([
        {
            message: `Hello, I am ${BOT_NAME}!`,
            sender: BOT_NAME,
            direction: "incoming",
            position: 0
        },
    ]);

    const [isChatbotTyping, setIsChatbotTyping] = useState<boolean>(false);

    const handleUserMessage = async (userMessage: string) => {
        // Create a new user message object
        const newUserMessage: MessageModel = {
            message: userMessage,
            sender: "user",
            direction: "outgoing",
            position: 0
        };

        // Update chat messages state with the new user message
        const updatedChatMessages = [...chatMessages, newUserMessage];
        setChatMessages(updatedChatMessages);
        setIsChatbotTyping(true);
        await processUserMessageToChatGPT(updatedChatMessages);
    };

    async function processUserMessageToChatGPT(messages: MessageModel[]) {
        let responseData;
        try {
            const response = await api.post("/api/query/", { q: messages[messages.length - 1].message });
            responseData = response.data;
        } catch (error) {
            console.error('Error:', error);
            responseData = { 'answer': error }
        }

        setChatMessages([
            ...messages,
            {
                message: responseData.answer,
                sender: BOT_NAME,
                direction: "incoming",
                position: 0
            },
        ]);
        // Set the typing indicator to false after getting the response
        setIsChatbotTyping(false);
    }

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setIsChatbotTyping(true);
            const newMessage: MessageModel = {
                message: `You have uploaded a file: ${file.name}`,
                sender: BOT_NAME,
                direction: "incoming",
                position: 0
            };

            const formData = new FormData();
            formData.append('file', file);
            api
                .post("/api/files/", formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                })
                .then((res) => {
                    if (res.status === 201) {
                        const updatedChatMessages = [...chatMessages, newMessage];
                        setChatMessages(updatedChatMessages);
                        setIsChatbotTyping(false);
                    }
                    else alert(`Failed to save the file. ${res.status}`);
                })
                .catch((err) => {
                    alert(`Failed to save the file. ${err}`);
                    setIsChatbotTyping(false);
                });
        }
    };

    const handleButtonClick = () => {
        if (inputRef.current) {
            inputRef.current.click();
        }
    };

    return (
        <>
            <input
                type="file"
                ref={inputRef}
                onChange={handleFileChange}
                style={{ display: 'none' }}
            />
            <MainContainer>
                <ChatContainer>
                    <MessageList typingIndicator={
                        isChatbotTyping ? <TypingIndicator content="thinking" /> : null
                    }>
                        {chatMessages.map((message, i) => {
                            return <Message key={i} model={message} style={message.sender === BOT_NAME ? { textAlign: "left" } : {}} />;
                        })}
                    </MessageList>
                    <MessageInput placeholder='Type your question here' onSend={handleUserMessage} onAttachClick={handleButtonClick} />
                </ChatContainer>
            </MainContainer>
        </>
    )
}

export default ChatWindow;
