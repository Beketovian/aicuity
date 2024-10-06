import { useEffect, useState } from "react";

export default function Loading() {
    const [subtitle, setSubtitle] = useState("Searching and downloading videos...");
    const [fadeClass, setFadeClass] = useState("opacity-0");

    useEffect(() => {
        const updateSubtitle = (text: string, timeout: number) => {
            setFadeClass("opacity-0");
            setTimeout(() => {
                setSubtitle(text);
                setFadeClass("opacity-100");
            }, 1000);
        };

        // ideally we make this actually communicate with backend but too much work
        const timers = [
            setTimeout(() => updateSubtitle("Analyzing videos...", 1000), 6000),
            setTimeout(() => updateSubtitle("Catering videos for you...", 1000), 15000),
            setTimeout(() => updateSubtitle("Finishing up! (≧∇≦)ﾉ", 1000), 24000),
        ];

        return () => timers.forEach(clearTimeout);
    }, []);

    return (
        <div className="w-full h-full flex justify-center items-center">
            <div className="flex flex-col items-center gap-y-12 loading-animation">
                <div className="flex gap-x-4 items-center font-bold text-4xl">
                    <div className="idfk"></div>
                    <h1>Loading</h1>
                </div>
                <div className={`transition-opacity duration-1000 ${fadeClass}`}>
                    <h2 className="text-lg">{subtitle}</h2>
                </div>
            </div>
        </div>
    );
}

function Eye({ id }: { id: string }) {
    const [eyePosition, setEyePosition] = useState({ x: 50, y: 50 });

    const handleMouseMove = (event: any) => {
        const eyeRect = document.getElementById(`eye_${id}`)!.getBoundingClientRect();
        const pupilRect = document.getElementById(`pupil_${id}`)!.getBoundingClientRect();
        const eyeCenterX = eyeRect.left + eyeRect.width / 2;
        const eyeCenterY = eyeRect.top + eyeRect.height / 2;

        const angle = Math.atan2(event.clientY - eyeCenterY, event.clientX - eyeCenterX);
        
        const pupilRadius = pupilRect.width / 2;
        const pupilX = Math.cos(angle) * pupilRadius + 48;
        const pupilY = Math.sin(angle) * pupilRadius + 48;

        setEyePosition({ x: pupilX, y: pupilY });
    };

    useEffect(() => {
        window.addEventListener('mousemove', handleMouseMove);
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    return (
        <div id={`eye_${id}`} className="w-24 aspect-square rounded-full border-2 border-solid border-gray-200 relative overflow-hidden bg-white">
            <div id={`pupil_${id}`} className="w-12 aspect-square rounded-full bg-black absolute" style={{ left: eyePosition.x - 15, top: eyePosition.y - 15 }} />
        </div>
    );
};
