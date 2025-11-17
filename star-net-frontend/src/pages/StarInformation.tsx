import React, { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import starTypesData from "../json/star_type.json";
import spectralClassesData from "../json/spectral_class.json";
import starColorsData from "../json/star_color.json";

import brownDwarf from "../images/brown-dwarf.png";
import redDwarf from "../images/red-dwarf.png";
import whiteDwarf from "../images/white-dwarf.png";
import mainSequence from "../images/main-sequence.png";
import superGiant from "../images/super-giant.jpeg";
import hyperGiant from "../images/hyper-giant.png";
import unknown from "../images/unknown.png";
import { FaLessThan } from "react-icons/fa6";
import { useLanguage } from "../context/LanguageContext";
import FetchError from "../components/FetchError";
import { useAmbientSound } from "../context/AmbientSoundContext";
import fadeOutAudio from "../functions/fadeOutAudio.ts";

interface StarData {
  starType: string;
  starColor: string;
  spectralClass: string;
}
interface StarSendData {
  temperature: number;
  luminosity: number;
  radius: number;
}

export default function StarInformation() {
  const { language } = useLanguage();

  const location = useLocation();
  const [sendData, setSendData] = useState<StarSendData>();
  const [starPredictionData, setStarPredictionData] = useState<StarData>();
  const navigate = useNavigate();

  const [spectralDesc, setSpectralDesc] = useState<string>();
  const [colorDesc, setColorDesc] = useState<string>();
  const [typeDesc, setTypeDesc] = useState<string>();

  const [hueShift, setHueShift] = useState<string>("0");
  const [brightness, setBrightness] = useState<string>("100%");
  const [activeImage, setActiveImage] = useState<string | undefined>(undefined);

  const [errorMsg, setErrorMsg] = useState<Error>();

  const { stopAmbientSound } = useAmbientSound();
  const spectralSoundRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    async function playSpectralSound(spectralClass: any) {
      try {
        stopAmbientSound();
        const soundModule = await import(`../sounds/${spectralClass}.wav`);
        spectralSoundRef.current = new Audio(soundModule.default);
        spectralSoundRef.current.play();
      } catch (error) {
        console.error("Failed to load or play the spectral sound:", error);
      }
    }

    if (starPredictionData?.spectralClass) {
      playSpectralSound(starPredictionData.spectralClass);
    }
  }, [starPredictionData?.spectralClass]);

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const dataString = queryParams.get("data");

    if (dataString) {
      try {
        const parsedData = JSON.parse(decodeURIComponent(dataString));
        setSendData({
          temperature: parsedData.temperature,
          luminosity: parsedData.luminosity,
          radius: parsedData.radius,
        });
      } catch (error) {
        console.error("Failed to parse data", error);
      }
    }
  }, [location.search]);

  useEffect(() => {
    if (sendData) {
      predictStarAttributes();
    }
  }, [sendData]);

  function predictStarAttributes() {
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        temperature: sendData?.temperature,
        luminosity: sendData?.luminosity,
        radius: sendData?.radius,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        setStarPredictionData({
          starType: data.starType,
          starColor: data.color,
          spectralClass: data.spectralClass,
        });
      })
      .catch((error) => {
        setErrorMsg(error);
      });
  }

  useEffect(() => {
    if (starPredictionData) {
      getStarDescription();
    }
  }, [starPredictionData, language]);

  function getStarDescription() {
    const typeMatches = starTypesData.StarTypes.filter(
      (ob) => ob.Name === starPredictionData?.starType
    );
    const spectralMatches = spectralClassesData.SpectralClasses.filter(
      (ob) => ob.Class === starPredictionData?.spectralClass
    );
    const colorMatches = starColorsData.StarColors.filter(
      (ob) => ob.Color === starPredictionData?.starColor
    );

    let typeDescription, spectralDescription, colorDescription;
    if (language === "En") {
      typeDescription =
        typeMatches.length > 0 ? typeMatches[0].Description : "";
      spectralDescription =
        spectralMatches.length > 0 ? spectralMatches[0].Description : "";
      colorDescription =
        colorMatches.length > 0 ? colorMatches[0].Description : "";
    } else {
      typeDescription =
        typeMatches.length > 0 ? typeMatches[0].DescriptionSv : "";
      spectralDescription =
        spectralMatches.length > 0 ? spectralMatches[0].DescriptionSv : "";
      colorDescription =
        colorMatches.length > 0 ? colorMatches[0].DescriptionSv : "";
    }

    setTypeDesc(typeDescription);
    setSpectralDesc(spectralDescription);
    setColorDesc(colorDescription);

    switch (starPredictionData?.starColor) {
      case "Red":
        setHueShift("0");
        setBrightness("100");
        break;
      case "Orange":
        setHueShift("30");
        break;
      case "Yellow":
        setHueShift("60");
        break;
      case "Blue":
        setHueShift("200");
        setBrightness("170");
        break;
      case "White":
        setHueShift("0");
        setBrightness("300");
        break;
      default:
        break;
    }
    switch (starPredictionData?.starType) {
      case "Red Dwarf":
        setActiveImage(redDwarf);
        break;
      case "Brown Dwarf":
        setActiveImage(brownDwarf);

        break;
      case "White Dwarf":
        setActiveImage(whiteDwarf);

        break;
      case "Main Sequence":
        setActiveImage(mainSequence);

        break;
      case "Supergiant":
        setActiveImage(superGiant);

        break;
      case "Hypergiant":
        setActiveImage(hyperGiant);
        break;

      default:
        setActiveImage(unknown);
        break;
    }
  }

  return (
    <div className="pt-10 pl-4 pr-4 bg-black h-[100vh]">
      {errorMsg ? (
        <>
          <FetchError error={errorMsg} />
        </>
      ) : (
        <>
          {starPredictionData && (
            <>
              <div className="flex w-[100%] justify-between text-[#00FF00]">
                <div className="image-main-container">
                  <div
                    className="w-52 h-52 bg-black tv-effect-container"
                    style={{ position: "relative" }}
                  >
                    <div
                      className={`image-wrapper`}
                      style={{
                        width: "100%",
                        height: "100%",
                        filter: `hue-rotate(${hueShift}deg) brightness(${brightness}%) invert(3%)`,
                        position: "relative",
                      }}
                    >
                      <img
                        className="tv-image"
                        src={activeImage}
                        alt=""
                        style={{
                          width: "100%",
                          height: "100%",

                          objectFit: "cover",
                        }}
                      />
                    </div>
                  </div>
                </div>
                <div className="flex flex-col gap-5 pt-3 pb-3">
                  <div className="w-60 flex flex-col gap-0 text">
                    <span>
                      {language === "En" ? <>Star type:</> : <>Stjärn typ:</>}{" "}
                      {starPredictionData.starType}
                    </span>
                    <span>
                      {language === "En" ? <>Star color:</> : <>Stjärn färg:</>}{" "}
                      {starPredictionData.starColor}
                    </span>
                    <span>
                      {language === "En" ? (
                        <>Spectral class:</>
                      ) : (
                        <>Spektralklass:</>
                      )}{" "}
                      {starPredictionData.spectralClass}
                    </span>
                  </div>
                  <div className="flex flex-col">
                    <span>
                      {language === "En" ? <>Temprature:</> : <>Temperatur:</>}{" "}
                      {sendData?.temperature}
                    </span>
                    <span>
                      {language === "En" ? <>Luminosity:</> : <>Ljusstyrka:</>}{" "}
                      {sendData?.luminosity}
                    </span>
                    <span>
                      {language === "En" ? <>Radius:</> : <>Radie:</>}{" "}
                      {sendData?.radius}
                    </span>
                  </div>
                </div>
              </div>
              <div className="w-[100%] flex flex-col gap-2 pt-5 text-[#00FF00]">
                <h2 className="text-xl ">
                  {language === "En" ? <>Description</> : <>Beskrivning</>}
                </h2>
                <span>{typeDesc}</span>
                <span>{spectralDesc}</span>
                <span>{colorDesc}</span>
              </div>
            </>
          )}
        </>
      )}
      <div
        className="mt-5 text-[#adadad] text-md w-[fit-content] flex h-10 items-center gap-5 cursor-pointer hover:text-[#00ff00] absolute bottom-5"
        onClick={() => navigate("/predict")}
      >
        <div>
          <FaLessThan />
        </div>
        {language === "En" ? <>Back</> : <>Tillbaka</>}
      </div>
    </div>
  );
}
