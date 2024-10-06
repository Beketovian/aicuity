export interface PlaylistData {
    topic: string;
    videos: VideoData[];
}

export interface VideoData {
    link: string;
    title: string;
    rating: number;
}

export interface PopupData {
    video: string;
    highlights: string[];
    links: string[];
}