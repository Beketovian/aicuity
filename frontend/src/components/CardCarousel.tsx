import { PlaylistData, VideoData } from "../types";
import "../styles/cardCarousel.css";
import { FaGlasses, FaPlay } from "react-icons/fa";

interface CardCarouselProps {
    playlists: PlaylistData[];
}

export default function CardCarousel({playlists}: CardCarouselProps) {
    return (
        <div className="w-full max-h-[90%] mt-[65px] loading-animation flex flex-col gap-y-8 overflow-y-auto pr-4">
            {playlists.map((playlist: PlaylistData, index) => {
                return (
                    <PlaylistCard
                        key={index}
                        topic={playlist.topic}
                        videos={playlist.videos}
                    />
                )
            })}
        </div>
    )
}

function PlaylistCard({topic, videos}: PlaylistData) {
    return (
        <div className="w-full">
            <h1 className="text-2xl font-bold border-b-[3px] border-solid border-gray-300 mb-2">{topic}</h1>
            <div className="w-full flex flex-col gap-y-4">
                <div className="w-full grid grid-cols-playlist px-4 bg-gray-200 text-gray-600 font-bold rounded-lg py-2 text-sm">
                    <p>Video Title</p>
                    <p>Watchability Score</p>
                    <p className="justify-self-center">Play Video</p>
                </div>
                {videos.map((video, index) => {
                    return (
                        <VideoCard
                            key={index}
                            video={video}
                        />
                    )
                })}
            </div>
        </div>
    )
}

function VideoCard({video}: {video: VideoData}) {
    return (
        <div className="w-full grid grid-cols-playlist px-4">
            <h2 className="text-base font-normal">{video.title}</h2>
            <div className="flex items-center gap-x-2 text-base font-bold">
                <p>{video.rating} / 10</p>
                <FaGlasses />
            </div>
            <a href={video.link} className="text-base justify-self-center">
                <FaPlay/>
            </a>
        </div>
    )
}