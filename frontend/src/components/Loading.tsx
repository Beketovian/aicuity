import { CgSpinner } from "react-icons/cg";

export default function Loading() {
    return (
        <div className="w-full h-full flex justify-center items-center">
            <div className="flex items-center gap-x-4 font-bold text-4xl loading-animation">
                <CgSpinner className="animate-spin"/>
                <h1>loading</h1>
            </div>
        </div>
    )
}