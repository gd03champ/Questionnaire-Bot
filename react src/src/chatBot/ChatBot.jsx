import axios from "axios";

import { AiFillMessage } from "react-icons/ai";
import { IoClose } from "react-icons/io5";
import { IoMdSend } from "react-icons/io";
import { motion, AnimatePresence } from "framer-motion";
import { useEffect, useState } from "react";
import SyncLoader from "react-spinners/SyncLoader";
import "./ChatBot.style.css";

const ChatBot = () => {
  const [showBot, setShowBot] = useState(false);
  const [message, setMessage] = useState("");
  const [botTyping, setBotTyping] = useState(false);
  const [chats, setChats] = useState([]);
  const [file, setFile] = useState(null);

  const toggleBot = () => {
    setShowBot(!showBot);
  };

  const handleUpload = (e) => {
    const tempFile =  e.target.files[0]
    const data = new FormData()
    data.append('file',tempFile)
    axios.post('http://127.0.0.1:5000/post',data)
      .then(res=>console.log(res.data)).catch(err=>{console.log(err.message);})


  };

  

  const handleSend = () => {
    const inputField = document.querySelector("#inputField");
    inputField.focus();
    if (!message) return;
    setBotTyping(true);
    const tempObj = { sender: "user", text: message };
    setChats((chat) => [...chat, tempObj]);
    setMessage("");

    axios
      .post("http://localhost:5005/webhooks/rest/webhook", { message: message })
      .then((res) => {
        if (res.data.length === 0 ) {
          const tempObj = {emptyRes:"Bot didn't send any response! Make sure you spelled everything correctly"}
          setChats((chat) => [...chat, tempObj]);
          setBotTyping(false);
          return ;
        }
        res.data.map((obj) => setChats((chat) => [...chat, obj]));
        setBotTyping(false);
      })
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    const chatWindow = document.querySelector(".chat-window");
    chatWindow && (chatWindow.scrollTop = chatWindow.scrollHeight);
  }, [chats, showBot]);

  return (
    <div className="chatBot">
      <AnimatePresence>
        {showBot && (
          <motion.div
            initial={{
              y: "100px",
              opacity: 0,
            }}
            animate={{
              y: 0,
              opacity: 1,
            }}
            exit={{
              y: "100px",
              opacity: 0,
            }}
            transition={{
              duration: 0.3,
              ease: "circOut",
            }}
            className="chatBot-container"
          >
            <div className="chatBot-header">
              <div className="loader">
                <SyncLoader margin='5px' color="white" size="10px" loading={botTyping} />
              </div>
            </div>
            <div className="chat-window">
              {chats.map((chat, key) => {
                if (chat.sender === "user") {
                  return (
                    <div key={key} className="chat-row-user">
                      <div className="user-chat">{chat.text}</div>
                    </div>
                  );
                } else {
                  return (
                      <div key={key} className="vertical-align-bot-chat chat-row-bot">
                      {chat.text && <div className="bot-chat">{chat.text}</div>}
                      {chat.emptyRes && <div className="bot-chat empty">{chat.emptyRes}</div>}
                      {chat.image && <img className="image-chat" src={chat.image} />}
                      {chat.buttons && chat.buttons.map(field=>
                        <button className="bot-chat bot-payloads ">
                          {field.title}
                        </button>
                      ) }
                    </div>
                  );
                }
              })}
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="input-row"
            >
              {/* <input type="file" onChange={handleUpload} /> */}
              <input
                autoComplete="off"
                onChange={(e) => setMessage(e.target.value)}
                type="text"
                value={message}
                id="inputField"
                placeholder="Start Conversation...."
              />
              <button type="submit">
                <IoMdSend color="white" size="18px" />
              </button>
            </form>
          </motion.div>
        )}
      </AnimatePresence>
      <div className="toggle-chatBot-btn">
        <button onClick={toggleBot}>
          {showBot ? (
            <IoClose color="blue" size="100%" />
          ) : (
            <AiFillMessage color="blue" size="100%" />
          )}
        </button>
      </div>
    </div>
  );
};

export default ChatBot;
