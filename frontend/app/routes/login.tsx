import React from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  const handleLogin = () => {
    // For now, no real logic
    navigate("/upload");
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Login / Register</h1>
      <input type="text" placeholder="Username" className="block mb-2 p-2 border" />
      <input type="password" placeholder="Password" className="block mb-2 p-2 border" />
      <button
        className="px-4 py-2 bg-blue-500 text-white rounded"
        onClick={handleLogin}
      >
        Login / Register
      </button>
    </div>
  );
}
