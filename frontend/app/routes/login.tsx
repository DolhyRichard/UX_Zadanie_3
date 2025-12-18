import React from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  const handleLogin = () => {
    // zatiaľ bez autentifikácie
    navigate("/upload");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-950 p-4">
      <div className="bg-white dark:bg-gray-900 shadow-xl rounded-2xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center text-indigo-700 dark:text-indigo-400 mb-6">
          Login / Register
        </h1>

        <div className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            className="w-full p-3 border border-gray-300 rounded bg-gray-50 dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full p-3 border border-gray-300 rounded bg-gray-50 dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />

          <button
            onClick={handleLogin}
            className="w-full py-3 rounded text-white font-semibold bg-indigo-500 hover:bg-indigo-600 transition"
          >
            Login / Register
          </button>
        </div>
      </div>
    </div>
  );
}
