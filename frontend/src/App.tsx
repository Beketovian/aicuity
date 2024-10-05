import { useState } from "react"
import Navbar from "./components/Navbar"
import Footer from "./components/Footer"

export default function App() {

    const [content, setContent] = useState("initial")

  return (
    <>
       <Navbar />
        <div className="content-wrapper">
            <div className={`${(content === "initial") ? "initial-content" : "hide"}`} onAnimationEnd={() => setContent("main")}>
                <img className="initial-content-img" src="/initial_img3.svg"/>
            </div>
            <div className={`${(content === "main") ? "main-content" : "hide"}`}>
                <h1 className="main-content-header">
                    a fast, simple, and easy way to 
                    <br/> personalize study playlists
                </h1>
                <div className="main-content-cta">
                    <input
                        className="main-content-input"
                        type="text"
                        placeholder="list all the topics you want to study"
                    />
                    <button className="main-content-btn">search</button>
                </div>
            </div>
        </div>
        <Footer />
    </>
  )
}
