export interface PlaylistData {
    topic: string;
    videos: VideoData[];
}

export interface VideoData {
    link: string;
    title: string;
    rating: number;
}