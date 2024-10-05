import "../styles/navbar.css";

export default function Navbar() {

    const currRoute = window.location.pathname;

    return (
        <nav className="navbar">
            <div className="logo">
                <a href="/">aicuity.</a>
            </div>
            <div className="links">
                <a className={(currRoute === '/') ? "active" : "inactive"} href="/">home</a>
                <a className={(currRoute === '/about') ? "active" : "inactive"} href="/about">about</a>
            </div>
        </nav>
    )
}