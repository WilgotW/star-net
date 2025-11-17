import React, {
  createContext,
  useContext,
  useState,
  useRef,
  useEffect,
  ReactNode,
} from "react";

interface AmbientSoundContextType {
  playAmbientSound: (soundSrc: string) => void;
  stopAmbientSound: () => void;
  setShouldPlayAudio: React.Dispatch<React.SetStateAction<boolean>>;
}

const AmbientSoundContext = createContext<AmbientSoundContextType | undefined>(
  undefined
);

export const useAmbientSound = () => {
  const context = useContext(AmbientSoundContext);
  if (!context)
    throw new Error("useAmbientSound must be used within AmbientSoundProvider");
  return context;
};

export const AmbientSoundProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [ambientAudio, setAmbientAudio] = useState<HTMLAudioElement | null>(
    null
  );
  const [shouldPlayAudio, setShouldPlayAudio] = useState(false);

  useEffect(() => {
    // Cleanup function to pause audio when the component unmounts or shouldPlayAudio changes
    return () => ambientAudio?.pause();
  }, [ambientAudio, shouldPlayAudio]);

  const playAmbientSound = async (soundSrc) => {
    if (ambientAudio) {
      await ambientAudio.pause();
    }
    let aud = (await import("../sounds/ambient.wav")).default;
    const audio = new Audio(aud);
    audio.loop = true;
    audio.volume = 0.6;
    try {
      await audio.play();
      setAmbientAudio(audio); // Set the playing audio after successful play
    } catch (err) {
      console.error("Error playing sound:", err);
    }
  };

  const stopAmbientSound = () => ambientAudio?.pause();

  return (
    <AmbientSoundContext.Provider
      value={{ playAmbientSound, stopAmbientSound, setShouldPlayAudio }}
    >
      {children}
    </AmbientSoundContext.Provider>
  );
};
