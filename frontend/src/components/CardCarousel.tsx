import { PlaylistData, VideoData } from "../types";
import "../styles/cardCarousel.css";
import { FaGlasses } from "react-icons/fa";

interface CardCarouselProps {
    playlists: PlaylistData[];
}

export default function CardCarousel({playlists}: CardCarouselProps) {
    return (
        <div className="carousel-container">
            {playlists.map((playlist: PlaylistData) => {
                return (
                    <PlaylistCard
                        videos={playlist.videos}
                    />
                )
            })}
        </div>
    )
}

function PlaylistCard({videos}: {videos:VideoData[]}) {
    return (
        <div className="playlist-card-container">
            <h1 className="playlist-topic-title">topic title</h1>
            <div className="videos-container">
                {videos.map((video) => {
                    return (
                        <VideoCard
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
        <div className="video-card-container">
            <img className="video-card-img" src="/placeholder.jpg" alt="video thumbnail"/>
            <h2 className="video-card-title">video title</h2>
            <div className="video-card-rating">
                <FaGlasses />
                <p className="video-card-score">80%</p>
            </div>
        </div>
    )
}