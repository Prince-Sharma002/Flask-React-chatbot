import React, { useEffect, useState , useRef } from 'react';
import "../styles/Home.scss";
import { MdOutlineMicNone } from "react-icons/md";

const Home = () => {
  const [user_input, setUserInput] = useState('');
  const [bot_respond, setBotrespond] = useState('');
  const [user_ans, setUserans] = useState(null);
  const [dataArray, setDataArray] = useState({});


  // listening
  const [listening, setListening] = useState(true);
  const [transcript, setTranscript] = useState("");

// speak
const [ speakerIcon, setSpeakerIcon] = useState(true)

// using of useRef to even change value doesn't cause re-render here utteranceRef holds value which 
// which is null when initializing
const utteranceRef = useRef(null);
const synth = window.speechSynthesis;
const [voices, setVoices] = useState([]);
const [femaleVoice, setFemaleVoice] = useState(null);


  useEffect(()=>{

    const loadVoices = () => {
      const availableVoices = synth.getVoices();
      setVoices(availableVoices);

      console.log(availableVoices)
      // Find a female voice
      const female = availableVoices.find(voice => voice.gender === 'female' || voice.name.toLowerCase().includes('female'));
      setFemaleVoice(female);
    };

    // Load voices initially
    loadVoices();

  },[])

  useEffect(() => {
    if (listening) {
      startListening();
    } else {
      startListening();
    }

  }, [listening , bot_respond]);



      const startListening = () => {

        const recognition = new window.webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.lang = 'en-US';
        recognition.onresult = (event) => {
          const currentTranscript = event.results[event.results.length - 1][0].transcript.toLowerCase();
          setTranscript(currentTranscript);
          setUserInput(currentTranscript);

          if(  currentTranscript.includes("close tab")  ){
    
            setUserInput("close tab");
            handleSubmit( "close tab");
          }
          if( currentTranscript.includes("switch") ){
            setUserInput("switch");
            handleSubmit( "switch");
          }

        
        };
        recognition.start();
      };   

      const stopListening = () => {
        const recognition = new window.webkitSpeechRecognition();
        recognition.stop();
      };


      const toggleListening = () => {
        setListening((prevState) => !prevState);
      };


      // speak

      const speak = (text)=>{

        const utterThis = new SpeechSynthesisUtterance(text);
    
        utteranceRef.current = utterThis;

        if (femaleVoice) {
          utterThis.voice = femaleVoice;
        }
    
        // Optional: Set other properties on the utterThis
        utterThis.lang = 'hi-IN';
        utterThis.rate = 1.1; // Speed
        utterThis.pitch = 1; // Pitch
        utterThis.volume = 2; // Volume
    
        synth.speak(utterThis);
    
        utterThis.addEventListener("end", () => {
          synth.cancel();
        });
        }
    
    
      const togglespeaker = () => {
            if(speakerIcon)
              synth.pause();
            else 
              synth.resume();
           
      };
    
      const clear = ()=>{
        synth.cancel();
        setTranscript("");
    
      }
    
      const repeat = ()=>{
        synth.cancel();
        speak(user_ans);
      }

  
  
  const handleSubmit = async(user_input)=>{

    console.log("button click")

    console.log(user_input)
    
    var ans = '';

    if( user_input === 'skip') {
      ans = user_input;
      setUserans(null);
    }
    else if( user_ans !== null ){
      setUserInput( `ans is-${user_ans} - ${user_input}`)
      ans = `ans is-${user_ans} - ${user_input}`;
      setUserans(null);
    }
    else if( user_input.includes("on youtube") ){
      const query = user_input.replace(/on youtube/gi, '');
      const searchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`;
      window.open(searchUrl, '_blank');
      setUserInput("");
      return ;
    }
    else if( user_input.includes("search") ){
      const query = user_input.replace(/search/gi, '');
      const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
      window.open(searchUrl, '_blank');
      setUserInput("");
      return ;
    }
    else{
      ans = user_input;
      if( ans == "")
        return ;
    }

    await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: ans })  // userInput is the input from the user
      })
      .then(response => response.json())
      .then(data => {
        console.log('Response from server:', data.response);
        
        
        const newData = { [ans]: data.response }; // Dynamically create an object with the key

        setDataArray(prevDataArray =>  ({
          ...newData, // Add new data
          ...prevDataArray  // Preserve previous data
        }));
        
        speak( data.response );
   
        if( data.response == "ok give me answer"){
            setUserans( user_input );
            console.log("ok give me anserrrrr")
        }
        else if( data.response.includes("moving to sofia") ){
          window.open('https://palmapi-67c47.web.app/');
          setBotrespond("");
        }

        
        setBotrespond( data.response );
      })
      .catch(error => {
        console.error('Error:', error);
      });

      setUserInput("");
  }

  const handleChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleFormSubmit = (e , str) => {
    e.preventDefault();
    handleSubmit(user_input);
  };
  
  return (
    <div className='home'>
      <h1>ChatBot</h1>
      <div className='dataDiv'>
        {Object.entries(dataArray).slice(0, 20).map(([question, answer]) => (
          <div key={question}>
            <p className='que'><strong style={{color:"#FA7070"}}>Question:</strong> {question}</p>
            <p className='ans'><strong style={{color:"#8DECB4"}}>Answer:</strong> {bot_respond}</p>
          </div>
        ))}
      </div>
      <form onSubmit={handleFormSubmit}>
        <input type="text" value={user_input} onChange={handleChange}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault();
              handleFormSubmit(e);
            }
          }}
          placeholder='input' />
          <button className='mic' onClick={toggleListening}>  <MdOutlineMicNone/> </button>
      
      </form>
    </div>
  );
};

export default Home;
