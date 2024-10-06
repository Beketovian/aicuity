import { FaExternalLinkAlt, FaWindowClose } from "react-icons/fa";

interface PopupProps {
    video: string;
    videoId: string;
    highlights: string[];
    links: string[];
    setShowPopup: any;
}

export default function Popup({video, highlights, links, setShowPopup, videoId} : PopupProps) {
    return (
        <div className="absolute left-0 top-0 bg-black/60 backdrop-blur-md w-screen h-screen flex justify-center items-center">
            <div className="p-4 rounded-md bg-white border-4 border-black border-solid flex flex-col gap-y-4 items-center">
                <div className="w-full flex justify-end text-xl">
                    <FaWindowClose 
                        className="cursor-pointer"
                        onClick={() => {setShowPopup(null)}}
                    />
                </div>
                {/* <div className="w-160 aspect-video rounded-md bg-gray-300">
                <iframe
                    width="100%" // Width of the iframe
                    src={"https://www.youtube.com/embed/"+videoId} // The YouTube video URL (replace with your URL)
                    title="YouTube video player" // Title for accessibility
                    frameBorder="0" // No border
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" // Permissions
                    allowFullScreen // Allow fullscreen mode
                ></iframe>
                </div> */}
                <ul className="w-full list-disc pl-5 ">
                    {highlights.map((highlight, index) => (
                        <li key={index}>
                            <a className="flex gap-x-2 items-center text-sm underline" href={links[index]}>
                                "...{highlight}..."
                                <FaExternalLinkAlt className="text-xs" />
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}