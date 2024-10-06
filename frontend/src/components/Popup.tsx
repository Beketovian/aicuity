import { FaWindowClose } from "react-icons/fa";

interface PopupProps {
    video: string;
    highlights: string[];
    links: string[];
    setShowPopup: any;
}

export default function Popup({video, highlights, links, setShowPopup} : PopupProps) {
    return (
        <div className="absolute left-0 top-0 bg-black/60 backdrop-blur-md w-screen h-screen flex justify-center items-center">
            <div className="p-4 rounded-md bg-white border-4 border-black border-solid flex flex-col gap-y-4">
                <div className="w-full flex justify-end text-xl">
                    <FaWindowClose 
                        className="cursor-pointer"
                        onClick={() => {setShowPopup(null)}}
                    />
                </div>
                <div className="w-40 aspect-video rounded-md bg-gray-300">

                </div>
                <ul className="w-full list-disc pl-5 ">
                    {highlights.map((highlight, index) => (
                        <li key={index}>
                            <a href={links[index]}>
                                {highlight}
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}