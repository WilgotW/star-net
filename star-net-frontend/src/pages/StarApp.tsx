import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import galaxy from "../images/galaxy.jpg";
import { FaLessThan } from "react-icons/fa6";
import { useLanguage } from "../context/LanguageContext";
import descriptions from "../json/descriptions.json";
import { useAmbientSound } from "../context/AmbientSoundContext";

export default function StarApp() {
  const navigate = useNavigate();
  const { language } = useLanguage();
  const { setShouldPlayAudio } = useAmbientSound();

  const [description, setDescription] = useState<string>("");

  useEffect(() => {
    if (language === "En") {
      const desc = descriptions.Descriptions.find(
        (desc) => desc.page === "home"
      )?.text;
      if (desc) {
        setDescription(desc);
      }
    } else {
      const desc = descriptions.Descriptions.find(
        (desc) => desc.page === "home"
      )?.textSv;
      if (desc) {
        setDescription(desc);
      }
    }
  }, [language]);

  function handleNavigate() {
    setShouldPlayAudio(true);
    navigate("/predict");
  }

  return (
    <div className="bg-black h-[100vh] flex flex-col">
      <div className="w-[100%] flex justify-center">
        <div className="relative w-full h-96 tv-effect-container max-w-[750px] ">
          <img
            src={galaxy}
            alt=""
            className="w-full h-full object-cover brightness-75"
          />
          <div className="absolute inset-0 flex justify-center items-center">
            <h1 className="text-5xl text-white outlined-text z-50 select-none">
              StarNet
            </h1>
          </div>
        </div>
      </div>
      <div className="w-[100%] flex justify-center">
        <div className="text-white p-10 flex flex-col items-center image-main-container max-w-[900px]">
          <span className="text-sm h-[400px]">{description}</span>
          <div
            className="mt-5 text-[#adadad] text-md flex w-[100%] h-10 items-center gap-5 cursor-pointer hover:text-[#00ff00]"
            onClick={() => handleNavigate()}
          >
            <div className="rotate-180">
              <FaLessThan />
            </div>
            USE STARNET
          </div>
        </div>
      </div>
    </div>
  );
}
