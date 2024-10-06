import "../styles/navbar.css";

export default function Navbar() {

    const currRoute = window.location.pathname;

    return (
        <nav className="w-full h-12 flex justify-between items-center gap-x-4 text-xl">
            <a 
                className="cursor-pointer" 
                href="/"
            >
                <img
                    src="/simple-logo.svg"
                    width={40}
                    height={40}
                />
            </a>
            <div className="flex gap-x-4">
                <a className={(currRoute === '/') ? "active" : "inactive"} href="/">home</a>
                <a className={(currRoute === '/about') ? "active" : "inactive"} href="/about">about</a>
            </div>
        </nav>
    )
}