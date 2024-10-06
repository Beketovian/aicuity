import Footer from "./components/Footer";
import Navbar from "./components/Navbar";

export default function About() {
    return (
        <>
            <Navbar />
            <div className="w-full h-full relative flex flex-col items-center justify-center gap-y-12 overflow-y-auto">
                <div className="max-w-screen-md w-full flex flex-col items-center gap-y-4">
                    <h1 className="max-w-screen-md w-full text-2xl font-bold">our mission.</h1>
                    <p className="max-w-screen-md w-full">
                        We've all been there where you need to study or learn a topic and you simply can't find a good high quality video that is both relevant and watchable. At Aicuity, our goal is to address this problem by  revolutionizing the way we obtain learning resources by delivering personalized video playlists tailored to your study topics. We combine cutting-edge AI with user-centered design to rank content for watchability, ensuring you get the most effective and engaging learning experience. We're dedicated to helping students and lifelong learners save time, focus on quality, and achieve their educational goals more efficiently.
                    </p>
                </div>

                <div className="max-w-screen-md w-full flex flex-col items-center gap-y-4">
                    <h1 className="max-w-screen-md w-full text-2xl font-bold">our team.</h1>
                    <p className="max-w-screen-md w-full">
                        Meet the team behind Aicuity.
                    </p>
                    <div className="flex flex-wrap w-full justify-between gap-x-4">
                       <div className="flex flex-col gap-y-1">
                            <img
                                className="rounded-md w-52 border-[3px] border-solid border-black"
                                src="/person2.jpg"
                            />
                            <p className="font-bold">Andrew Beketov</p>
                        </div>
                        <div className="flex flex-col gap-y-1">
                            <img
                                className="rounded-md w-52 border-[3px] border-solid border-black"
                                src="/person3.jpg"
                            />
                            <p className="font-bold">Christion Bradley</p>
                        </div>
                        <div className="flex flex-col gap-y-1">
                            <img
                                className="rounded-md w-52 border-[3px] border-solid border-black"
                                src="person1.jpg"
                            />
                            <p className="font-bold">Warren Wu</p>
                        </div>
                    </div>
                </div>
  
            </div>
            <Footer />
        </>
    )
}