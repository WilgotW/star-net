import React, { useEffect, useRef, useState } from "react";
import { useLanguage } from "../context/LanguageContext";

export default function BottomBar() {
  const { language, setLanguage } = useLanguage();

  function changeLanguage() {
    const lan = language === "En" ? "Sv" : "En";
    setLanguage(lan);
  }

  return (
    <div className="absolute bottom-5 right-5 z-50">
      <h1
        className=" cursor-pointer select-none"
        onClick={() => changeLanguage()}
      >
        Lan: {language}
      </h1>
    </div>
  );
}
