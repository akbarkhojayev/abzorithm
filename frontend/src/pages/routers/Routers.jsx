import React, { useEffect, useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Helmet } from "react-helmet";

import { ThemeProvider } from "../../context/ThemeContext.jsx";
import Navbar from "../../components/navbar/Navbar.jsx";
import Problems from "../problems/Problems.jsx";
import CodePanels from "../codePanels/CodePanels.jsx";
import Scrolltop from "../../components/scroltop/Scrolltop.jsx";
import CreateAccaunt from "../createAccount/CreateAccaunt.jsx";
import { ToastContainer } from "react-toastify";
import SignIn from "../signIn/SignIn.jsx";
import { getToken } from "../services/token.js";
import ProfilMe from "../profilMe/ProfilMe.jsx";
import LeaderBoard from "../leaderboard/LeaderBoard.jsx";
import Error from "../error/Error.jsx";
import SolutionsHistory from "../solutionsHistory/SolutionsHistory.jsx";
import Statistics from "../statistics/Statistics.jsx";

function Routers() {
  const [profil, setProfil] = useState(null);
  const [problemData, setProblemData] = useState([]);
  const [ratingUser, setRatingUser] = useState(null);
  const [profilMe, setProfilMe] = useState(null);
  const [tokens, setTokens] = useState(null);

  useEffect(() => {
    const token = getToken();
    setTokens(token);
  }, []);

  return (
    <ThemeProvider>
      <BrowserRouter>
        <Navbar
          tokens={tokens}
          setTokens={setTokens}
          profilMe={profilMe}
          setProfilMe={setProfilMe}
        />

        <ToastContainer autoClose={1000} />
        <Scrolltop />

        <Routes>
          <Route
            path="/"
            element={
              <>
                <Problems
                  setProblemData={setProblemData}
                  problemData={problemData}
                />
              </>
            }
          />
          <Route
            path="/codepanels/:slug"
            element={
              <>
                <CodePanels
                  profil={profil}
                  setProfil={setProfil}
                  setProblemData={setProblemData}
                />
              </>
            }
          />
          <Route
            path="/leaderboard"
            element={
              <>
                <LeaderBoard
                  ratingUser={ratingUser}
                  setRatingUser={setRatingUser}
                />
              </>
            }
          />
          <Route
            path="/signIn"
            element={
              <>
                <SignIn setTokens={setTokens} setProfilMe={setProfilMe} />
              </>
            }
          />
          <Route path="/create-account" element={<CreateAccaunt />} />
          <Route
            path="/profil"
            element={
              <>
                <ProfilMe
                  profil={profil}
                  setProfil={setProfil}
                  setProfilMe={setProfilMe}
                />
              </>
            }
          />
          <Route
            path="/solutions-history"
            element={
              tokens ? (
                <SolutionsHistory />
              ) : (
                <>
                  <Error />
                </>
              )
            }
          />
          <Route
            path="/statistics"
            element={
              tokens ? (
                <Statistics />
              ) : (
                <>
                  <Error />
                </>
              )
            }
          />
          {/* 404 error page */}
          <Route path="*" element={<Error />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default Routers;
