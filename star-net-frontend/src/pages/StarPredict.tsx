import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaLessThan } from "react-icons/fa6";
import { useLanguage } from "../context/LanguageContext";
import descriptions from "../json/descriptions.json";
import { useAmbientSound } from "../context/AmbientSoundContext";

interface StarSendData {
  temperature: string;
  luminosity: string;
  radius: string;
}

export default function StarPredict() {
  const { playAmbientSound, setShouldPlayAudio } = useAmbientSound();

  useEffect(() => {
    playAmbientSound("");
  }, [playAmbientSound, setShouldPlayAudio]);

  const navigate = useNavigate();
  const [starSendData, setStarSendData] = useState<StarSendData>({
    temperature: "",
    luminosity: "",
    radius: "",
  });
  const { language } = useLanguage();
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

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement>,
    field: keyof StarSendData
  ) {
    const value = e.target.value;
    setStarSendData((prevState) => ({
      ...prevState,
      [field]: value,
    }));
  }

  function send(ev: React.MouseEvent<HTMLDivElement, MouseEvent>) {
    ev.preventDefault();
    const dataToSend = {
      temperature: parseFloat(starSendData.temperature) || 0,
      luminosity: parseFloat(starSendData.luminosity) || 0,
      radius: parseFloat(starSendData.radius) || 0,
    };
    const data = JSON.stringify(dataToSend);
    navigate(`/info?data=${encodeURIComponent(data)}`);
  }
  return (
    <div className="p-3 flex flex-col gap-5 bg-black h-[100vh]  image-main-container ">
      <h1 className="text-2xl">
        {language === "En" ? (
          <>Predict star types</>
        ) : (
          <>Förutse stjärn tpyer</>
        )}
      </h1>
      <span className="h-[500px] ">{description}</span>
      <div className="flex flex-col gap-2">
        {/* <button className="text-white" onClick={test}>
          plwefwefwefwefay
        </button> */}
        <input
          className="bg-black border-b text-white outline-none"
          type="text"
          placeholder={language === "En" ? "Temperature" : "Temperatur"}
          value={starSendData.temperature}
          onChange={(e) => handleChange(e, "temperature")}
        />
        <input
          className="bg-black border-b text-white outline-none"
          type="text"
          placeholder={language === "En" ? "Luminosity" : "Ljusstyrka"}
          value={starSendData.luminosity}
          onChange={(e) => handleChange(e, "luminosity")}
        />
        <input
          className="bg-black border-b text-white outline-none"
          type="text"
          placeholder={language === "En" ? "Radius" : "Radie"}
          value={starSendData.radius}
          onChange={(e) => handleChange(e, "radius")}
        />
        <div
          className="mt-5 text-[#adadad] text-xl w-[fit-content] flex h-10 items-center gap-5 cursor-pointer hover:text-[#00ff00]"
          onClick={(ev) => send(ev)}
        >
          <div className="rotate-180">
            <FaLessThan />
          </div>
          {language === "En" ? <>Predict</> : <>Förutse</>}
        </div>
      </div>
    </div>
  );
}
