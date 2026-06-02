import React, { useState } from "react";
import "./SignIn.css";
import { baseUrl } from "../services/config.js";
import { Button } from "@mui/material";
import { toast } from "react-toastify";
import { Link, useNavigate } from "react-router-dom";
import { getToken, setToken } from "../services/token.js";
import { getProfilMe } from "../services/app.js";
import { AiOutlineEye, AiOutlineEyeInvisible, AiOutlineMail, AiOutlineLock } from "react-icons/ai";

function SignIn({ setTokens, setProfilMe }) {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loderSignIn, setLoaderSignIn] = useState(false);

  const signIn = () => {
    setLoaderSignIn(true);
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
          toast.success("Muvofaqqiyatli kirdingiz");
          navigate("/");
        }
      })
      .catch((error) => console.error(error))
      .finally(() => {
        setLoaderSignIn(false);
      });
  };

  return (
    <>
      <div className={`loadingEffect ${loderSignIn ? "active" : ""}`}>
        <p>
          <span>L</span>
          <span>o</span>
          <span>a</span>
          <span>d</span>
          <span>i</span>
          <span>n</span>
          <span>g</span>
        </p>
      </div>
      <div className="signin-container">
        <div className="signin-card">
          <div className="signin-header">
            <h1>Codial Algo</h1>
            <p>Algoritmik masalalarni yechmni boshlang</p>
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault();
              signIn();
            }}
            className="signin-form"
          >
            <div className="form-group">
              <label htmlFor="username">Foydalanuvchi Nomi</label>
              <div className="input-wrapper">
                <AiOutlineMail className="input-icon" />
                <input
                  id="username"
                  onChange={(e) => {
                    setUsername(e.target.value);
                  }}
                  type="text"
                  required
                  placeholder="Username kiriting"
                  value={username}
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="password">Parol</label>
              <div className="input-wrapper">
                <AiOutlineLock className="input-icon" />
                <input
                  id="password"
                  onChange={(e) => {
                    setPassword(e.target.value);
                  }}
                  type={showPassword ? "text" : "password"}
                  required
                  placeholder="Parol kiriting"
                  value={password}
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <AiOutlineEyeInvisible /> : <AiOutlineEye />}
                </button>
              </div>
            </div>

            <Button
              variant="contained"
              type="submit"
              fullWidth
              className="signin-button"
              disabled={loderSignIn}
            >
              {loderSignIn ? "Yuklanmoqda..." : "Kirish"}
            </Button>

            <div className="signin-footer">
              <p>
                Hali akkauntingiz yo'qmi?{" "}
                <Link to={"/create-account"}>Yangi akkaunt yaratish</Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

export default SignIn;
