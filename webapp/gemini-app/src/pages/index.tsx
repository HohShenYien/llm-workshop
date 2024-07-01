import Image from "next/image";
import { Inter } from "next/font/google";
import { useState } from "react";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [reply, setReply] = useState("");
  const queryPrompt = () => {
    fetch("http://127.0.0.1:5000/prompt", {
      method: "POST",
      body: JSON.stringify({ prompt }),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    }).then((res) => {
      res.json().then((data) => {
        setReply(data.response);
      });
    });
  };
  return (
    <div className="h-screen w-screen flex justify-center items-center">
      <div className="w-[500px] h-[500px] flex flex-col">
        <div className="font-medium mb-2">Prompt</div>
        <textarea
          className="border-2 border-gray mb-8"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button
          className="bg-blue-400 text-white hover:bg-blue-500 active:bg-blue-600 rounded-sm px-3 py-1"
          onClick={queryPrompt}
        >
          Submit
        </button>
        {reply && (
          <div className="mt-8">
            <div className="font-medium">Response</div>
            <div>{reply}</div>
          </div>
        )}
      </div>
    </div>
  );
}
