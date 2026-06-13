import React, { useState } from "react";
import "./CreateAccaunt.css";
import { baseUrl } from "../services/config.js";
import { toast } from "react-toastify";
import { Link, useNavigate } from "react-router-dom";

function CreateAccaunt() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const createAccaunt = () => {
    if (!username.trim() || !email.trim() || !password.trim()) {
      toast.error("Barcha maydonlarni to'ldiring");
      return;
    }

    setLoading(true);

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
      username: username,
      email: email,
      password: password,
    });

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    fetch(`${baseUrl}/users/register/`, requestOptions)
      .then((response) => response.json())
      .then((result) => {
        if (Array.isArray(result.username) && result.username[0]) {
          toast.error(result.username[0]);
        } else if (Array.isArray(result.email) && result.email[0]) {
          toast.error(result.email[0]);
        } else if (result.detail) {
          toast.error(result.detail);
        } else {
          toast.success("Akkaunt muvaffaqiyatli yaratildi!");
          setTimeout(() => navigate("/signIn"), 1500);
        }
      })
      .catch((error) => {
        toast.error("Xatolik yuz berdi");
        console.error(error);
      })
      .finally(() => setLoading(false));
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <div className="register-card">
          <div className="register-header">
            <h1>Roʻyxatdan Oʻtish</h1>
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault();
              createAccaunt();
            }}
            className="register-form"
          >
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
              <small className="form-hint">3-20 ta belgi, lotin harflari va raqamlar</small>
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                required
                placeholder="example@mail.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
              />
              <small className="form-hint">To'g'ri email manzilini kiritingy</small>
            </div>

            <div className="form-group">
              <label htmlFor="password">Parol</label>
              <input
                id="password"
                type="password"
                required
                placeholder="Xavfsiz parol"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
              />
              <small className="form-hint">Kamida 6 ta belgi</small>
            </div>

            <div className="form-actions">
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? "Roʻyxatdan oʻtilmoqda..." : "Roʻyxatdan oʻtish"}
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => navigate("/")}
                disabled={loading}
              >
                Bekor
              </button>
            </div>

            <div className="register-footer">
              <span>Akkaunt bormi?</span>
              <Link to="/signIn">Kirish</Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default CreateAccaunt;
