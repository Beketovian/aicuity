import { useState } from "react"
import Navbar from "./components/Navbar"
import Footer from "./components/Footer"
import { PlaylistData, PopupData } from "./types"
import CardCarousel from "./components/CardCarousel";
import Loading from "./components/Loading";
import Popup from "./components/Popup";


export default function App() {

    const [playlists, setPlaylists] = useState<PlaylistData[]>([])

    const [stage1, setStage1] = useState<string>("show");
    const [stage2, setStage2] = useState<string>("hide");
    const [stage2b, setStage2b] = useState<string>("hide");
    const [stage3, setStage3] = useState<string>("hide");

    const [showPopup, setShowPopup] = useState<PopupData | null>(null);

    function transitionStage1() {
        // end stage 1
        setStage1("hide");
        // start stage 2
        setStage2("show");
        setStage2b("show");
    }

    function transitionStage2() {
        // end stage 2
        setStage2("hide");
        // start stage 3
        setStage3("show");
    }

    async function handleSubmit(e: any) {
        e.preventDefault()
        transitionStage2();
        // get all topics
        const topics = e.target[0].value.split(",");
        const body = {
            query: topics
        }
        // make a request to the backend
        // const response = await fetch("http://localhost:5000/search_and_analyze", {
        //     method: "POST",
        //     headers: {
        //         "Content-Type": "application/json"
        //     },
        //     body: JSON.stringify(body)
        // })
        // const data = await response.json()
        // console.log(data);
        setPlaylists([
            {
                topic: "your mom",
                videos: [
                    {
                        link: "/omg",
                        title: "why moms are the best parents",
                        rating: 5
                    }
                ]
            }
        ])
    }

    return (
        <>
        <Navbar />
        <div className="w-full h-full relative">

            <div className={`initial-content ${stage1} border-4 border-solid border-black`} onAnimationEnd={transitionStage1}>
                <img className="initial-content-img" src="/initial_img3.svg"/>
            </div>

            <div className={`${stage2b} ${(stage3 === "show") ? "justify-start" : "justify-center"} w-full h-full relative`}>

                <div className={`playlist-content ${stage3}`}>
                    {/* {(playlists.length <= 0) ? <Loading/> : <Loading/>} */}
                    {(playlists.length <= 0) ? <Loading/> : <CardCarousel playlists={playlists} setShowPopup={setShowPopup}/>}
                </div>

                <div className={`w-full flex flex-col gap-y-8 items-center justify-center absolute left-1/2 ${(stage3 === "show") ? "cta-ani" : "cta-non"}`}>
                    <h1 className={`main-content-header font-bold text-4xl ${stage2}`}>
                        a fast, simple, and easy way to 
                        <br/> personalize study playlists
                    </h1>
                    <form onSubmit={handleSubmit} className={`w-full main-content-cta ${stage2b} z-4 items-center`}>
                        <input
                            className={`${(stage3 === "show") ? "w-full" : "w-80"} main-content-input text-base transition-all duration-1000 delay-250 border-[3px] border-black border-solid`}
                            type="text"
                            placeholder="list all the topics you want to study"
                        />
                        <button className="px-4 py-3 border-none bg-[#E4B1F0] rounded-md text-base font-bold main-content-btn z-3 brutalist">search</button>
                    </form>
                </div>

                <img
                    className={`w-2/6 max-w-80 wiggle absolute top-0 left-0 ${stage2}`}
                    src="/element1.png"
                />
                <img
                    className={`w-2/6 max-w-80 wiggle absolute top-0 right-0 animation-delay-500 ${stage2}`}
                    src="/element2.png"
                />
                <img
                    className={`w-2/6 max-w-80 wiggle absolute bottom-0 left-0 animation-delay-1000 ${stage2}`}
                    src="/element3.png"
                />
                <img
                    className={`w-2/6 max-w-80 wiggle absolute bottom-0 right-0 ${stage2}`}
                    src="/element4.png"
                />
            </div>
        </div>
        {(showPopup == null) ? <></> : <Popup video={showPopup.video} highlights={showPopup.highlights} links={showPopup.links} setShowPopup={setShowPopup}/>}
        <Footer />
        </>
    )
}
