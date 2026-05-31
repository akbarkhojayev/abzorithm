import React, { createContext, useContext, useState, useEffect } from "react";

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within ThemeProvider");
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    // Load theme from localStorage or use system preference
    try {
      const saved = localStorage.getItem("theme");
      if (saved) return saved;

      // Check system preference
      if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
        return "dark";
      }
      return "light";
    } catch {
      return "light";
    }
  });

  useEffect(() => {
    // Save theme to localStorage
    try {
      localStorage.setItem("theme", theme);
    } catch (e) {
      console.error("Failed to save theme:", e);
    }

    // Update document attribute
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  const isDark = theme === "dark";

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, isDark }}>
      {children}
    </ThemeContext.Provider>
  );
};
