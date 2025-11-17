export default function fadeOutAudio(audioRef, callback) {
  let volume = audioRef.current.volume;
  const fade = setInterval(() => {
    if (volume > 0.1) {
      // Decrease volume until it's almost 0
      volume -= 0.1;
      audioRef.current.volume = volume;
    } else {
      clearInterval(fade);
      audioRef.current.pause();
      audioRef.current.volume = 1; // Optional: Reset volume for next play
      callback(); // Execute callback function once fade-out is complete
    }
  }, 10); // Adjust interval for smoother fade-out
}
