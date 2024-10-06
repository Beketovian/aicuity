import { PlaylistData, Ranking, VideoData, Subtitle } from "../types";
import "../styles/cardCarousel.css";
import { FaGlasses, FaPlay } from "react-icons/fa";
import { useEffect, useState } from "react";

interface CardCarouselProps {
    playlists: Ranking;
    prompt: string;
    setShowPopup: any;
}

export default function CardCarousel({playlists, prompt, setShowPopup}: CardCarouselProps) {

    const [playlistCards, setPlaylistCards] = useState<any[]>([]);

    useEffect(() => {

        async function fetchData() {
    const values = Object.values(playlists)[0];
    Object.keys(values).forEach(async (key:any) => {
        const videoId = key;
        const videoData = values[key];
        const body = {
            video_id: videoId
        }
        // make a request to the backend
        const response = await fetch("http://localhost:5000/get_title", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        })
        const data = await response.json()
        setPlaylistCards((prev) => [...prev, (
            <VideoCard
                key={videoId}
                videoId={videoId}
                video={{link: `https://www.youtube.com/watch?v=${videoId}`, title: data.title, rating: videoData[0]+1}}
                setShowPopup={setShowPopup}
                videoData={videoData}
            />
        )]);
    })
    }
    fetchData();

    }, [])

    return (
        <div className="w-full max-h-[70%] mt-[65px] loading-animation flex flex-col gap-y-8 overflow-y-auto pr-4">
            <div className="w-full">
            <h1 className="text-2xl font-bold border-b-[3px] border-solid border-gray-300 mb-2">{prompt}</h1>
            <div className="w-full flex flex-col gap-y-4">
                <div className="w-full grid grid-cols-playlist px-4 bg-gray-200 text-gray-600 font-bold rounded-lg py-2 text-sm">
                    <p>Video Title</p>
                    <p className="justify-self-center">Video Ranking</p>
                    <p className="justify-self-center">Play Video</p>
                </div>
                {playlistCards}
            </div>
            </div>
        </div>
    )
}

interface PlaylistCardProps {
    topic: string;
    videos: VideoData[];
    setShowPopup: any;
}

function PlaylistCard({topic, videos, setShowPopup}: PlaylistCardProps) {
    return (
        <div className="w-full">
            <h1 className="text-2xl font-bold border-b-[3px] border-solid border-gray-300 mb-2">{topic}</h1>
            <div className="w-full flex flex-col gap-y-4">
                <div className="w-full grid grid-cols-playlist px-4 bg-gray-200 text-gray-600 font-bold rounded-lg py-2 text-sm">
                    <p>Video Title</p>
                    <p className="justify-self-center">Watchability Score</p>
                    <p className="justify-self-center">Play Video</p>
                </div>
                {videos.map((video, index) => {
                    return (
                        <VideoCard
                            key={index}
                            video={video}
                            setShowPopup={setShowPopup}
                        />
                    )
                })}
            </div>
        </div>
    )
}

interface VideoCardProps {
    video: VideoData;
    setShowPopup: any;
    videoData: any;
    videoId: string;
}

function VideoCard({video, setShowPopup, videoData, videoId}: VideoCardProps) {
    
    function showStuff() {
        const stuff = videoData[1];
        const currHighlights = []
        const currLinks = [];

        stuff.map(({duration, start, text}: Subtitle) => {
            currHighlights.push(text);
            currLinks.push(`${video.link}&t=${start}`);
        })
        setShowPopup({
            video: video.link,
            highlights: currHighlights,
            links: currLinks,
            videoId: videoId
        })
    }
    
    return (
        <button type="button" onClick={showStuff} className="w-full grid grid-cols-playlist px-4">
            <h2 className="w-full flex text-start justify-start text-base font-normal">{video.title}</h2>
            <div className="flex justify-center items-center text-center gap-x-2 text-base font-bold">
                <p>{video.rating}</p>
            </div>
            <a href={video.link} className="text-base justify-self-center">
                <FaPlay/>
            </a>
        </button>
    )
}