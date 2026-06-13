import React, { useState } from "react";
import "./SignIn.css";
import { baseUrl } from "../services/config.js";
import { toast } from "react-toastify";
import { Link, useNavigate } from "react-router-dom";
import { getToken, setToken } from "../services/token.js";
import { getProfilMe } from "../services/app.js";

function SignIn({ setTokens, setProfilMe }) {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSignIn = () => {
    if (!username.trim() || !password.trim()) {
      toast.error("Barcha maydonlarni to'ldiring");
      return;
    }

    setLoading(true);
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
      username: username,
      password: password,
    });

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    fetch(`${baseUrl}/token/`, requestOptions)
      .then((response) => response.json())
      .then((result) => {
        if (result?.detail) {
          toast.error(result?.detail);
        } else if (result?.access) {
          setToken(result?.access);
          setTokens(getToken());
          getProfilMe()?.then(setProfilMe);
          toast.success("Muvaffaqiyatli kirdingiz!");
          setTimeout(() => navigate("/"), 1000);
        }
      })
      .catch((error) => {
        toast.error("Xatolik yuz berdi");
        console.error(error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSignIn();
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <h1>Kirish</h1>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                id="username"
                type="text"
                required
                placeholder="Foydalanuvchi nomi"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Parol</label>
              <div className="password-wrapper">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  required
                  placeholder="Parolingizni kiriting"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                />
                <button
                  type="button"
                  className="toggle-password-btn"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={loading}
                >
                  {showPassword ? "Yashir" : "Ko'r"}
                </button>
              </div>
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-full"
              disabled={loading}
            >
              {loading ? "Kirish..." : "Kirish"}
            </button>

            <div className="login-footer">
              <span>Akkaunt yo'qmi?</span>
              <Link to="/create-account">Roʻyxatdan oʻtish</Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default SignIn;
