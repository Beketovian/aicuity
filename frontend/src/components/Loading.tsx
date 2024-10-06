import { useEffect, useState } from "react";

export default function Loading() {


    return (
        <div className="w-full h-full flex justify-center items-center">
            <div className="flex flex-col items-center gap-y-12 loading-animation">
                <div className="flex gap-x-4 items-center font-bold text-4xl">
                    <div className="idfk"></div>
                    <h1>loading</h1>
                </div>
            </div>
        </div>
    )
}

function Eye({id}: {id: string}) {
    const [eyePosition, setEyePosition] = useState({ x: 50, y: 50 });

    // Function to handle mouse movement
    const handleMouseMove = (event: any) => {
        // Get the bounding rectangle of the eye element
        const eyeRect = document.getElementById(`eye_${id}`)!.getBoundingClientRect();
        const pupilRect = document.getElementById(`pupil_${id}`)!.getBoundingClientRect();
        // Calculate the center of the eye
        const eyeCenterX = eyeRect.left + eyeRect.width / 2;
        const eyeCenterY = eyeRect.top + eyeRect.height / 2;

        // Calculate the angle to the cursor
        const angle = Math.atan2(event.clientY - eyeCenterY, event.clientX - eyeCenterX);
        
        // Calculate the new position of the pupil
        const pupilRadius = pupilRect.width / 2; // Adjust this for pupil size
        const pupilX = Math.cos(angle) * pupilRadius + 48;
        const pupilY = Math.sin(angle) * pupilRadius + 48;
        // console.log(pupilX, pupilY);
        // Update eye position
        setEyePosition({ x: pupilX, y: pupilY });
    };

    useEffect(() => {
        // Add event listener for mouse movement
        window.addEventListener('mousemove', handleMouseMove);

        // Cleanup event listener on component unmount
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    return (
        <div id={`eye_${id}`} className="w-24 aspect-square rounded-full border-2 border-solid border-gray-200 relative overflow-hidden bg-white">
            <div id={`pupil_${id}`} className="w-12 aspect-square rounded-full bg-black absolute" style={{left: eyePosition.x - 15, top: eyePosition.y - 15 }} />
        </div>
    );
};
