import { useState,React } from 'react';
import style from "../pagescss/bot.module.css"
import axios from "axios";



const Bot=()=>{

    const [msg,setMsg]=useState()

    const [chat,setChat]=useState([])




    const addChat=async(user,data)=>{

      
      const msgBody={"role":user,"content":data}
     
      const newChat=([...chat,msgBody])
      
      setChat(newChat)
      
      const gptResponse= await sendChat(newChat)
      // newChat.push(gptResponse)
      //  add(newChat)
      // console.log(chat)
      

    }

    const add= async(newChat)=>{
      setChat(newChat)
    }

    const sendChat = async (newchat) => {
        try {

          console.log(newchat)
          const response = await axios.post('http://127.0.0.1:5000/getweather', {
            "chat":newchat 
          });
          
          console.log(response);

          console.log(response.data.choices[0].message.content)
          setChat([...newchat,{"role":"assistant","content":response.data.choices[0].message.content}])
        //   return {"role":"assistant","content":response.data.gpt_choice.message.content} ;

        //   setAns(response.data.gpt_choice.message.content)
        } catch (error) {
          console.error(error);
        }


      };

    return(
      <div className={style.back}>
        
        <div className={style.body}>

          <h1 className={style.hadding}>Real Time Chat Bot</h1>
          <div className={style.chatArea}>
          {
           
           chat.map((el, i) => (
              <div key={i} className={el.role=="assistant"? style.bot: style.person}>
                <p>
                  {/* <p>{i}</p> */}
                  {el.content}
                </p>
              </div>
            ))
           }
          </div>

          <hr/>

          <div>
             <textarea className={style.chat_inbox} onChange={(e)=>setMsg(e.target.value)} rows="4" cols="50"  placeholder="Send a message"></textarea>
             
             <button className={style.send_btn} onClick={()=>addChat("user",msg)} >Send</button>

          </div>
          <div>
            
          </div>

        </div>
      </div>
    )
}

export default Bot;
