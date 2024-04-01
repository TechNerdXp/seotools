import { useState, useEffect } from 'react';
import { SunIcon, MoonIcon, ComputerDesktopIcon } from '@heroicons/react/24/solid';
import { NavLink, useLocation } from 'react-router-dom';

export default function Navbar() {
  const [theme, setTheme] = useState('system');
  const location = useLocation();
  const currentPath = location.pathname;

// Retrieve theme from localStorage or default to 'system'
useEffect(() => {
    const storedTheme = typeof window !== 'undefined' ? localStorage.getItem('theme') : 'system';
    if (storedTheme) {
      setTheme(storedTheme);
    }
  }, []);

  // Update theme and localStorage
  useEffect(() => {
    let actualTheme;
    if (theme === 'system') {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        actualTheme = 'night';
      } else {
        actualTheme = 'nord';
      }
    } else {
      actualTheme = theme === 'light' ? 'nord' : 'night';
    }
    if (typeof window !== 'undefined' && theme !== 'system') {
      localStorage.setItem('theme', theme);
    }
    document.documentElement.setAttribute('data-theme', actualTheme);
  }, [theme]);

  // Handle theme change
  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
  };

  return (
    <div className="navbar bg-base-100 px-10 glass">
      <div className="navbar-start">
        <NavLink to="/" className="btn btn-ghost text-xl">🔍🛠️</NavLink>
      </div>
      <div className="navbar-center hidden lg:flex">
        <ul className="menu menu-horizontal px-1">
          <li><NavLink to="/files" className={currentPath === '/files' ? 'bg-secondary text-base' : ''}>Files</NavLink></li>
          <li><NavLink to="/mapping" className={currentPath === '/mapping' ? 'bg-secondary text-base' : ''}>Mapping Page</NavLink></li>
        </ul>
      </div>
      <div className="navbar-end">
        <button onClick={() => handleThemeChange('light')} className={`btn ${theme === 'light' ? 'btn-secondary' : 'btn-ghost'} text-xl p-1 w-8 h-8`}>
            <SunIcon />
        </button>
        <button onClick={() => handleThemeChange('system')} className={`btn ${theme === 'system' ? 'btn-secondary' : 'btn-ghost'} text-xl p-1 w-8 h-8`}>
            <ComputerDesktopIcon />
        </button>
        <button onClick={() => handleThemeChange('dark')} className={`btn ${theme === 'dark' ? 'btn-secondary' : 'btn-ghost'} text-xl p-1 w-8 h-8`}>
            <MoonIcon />
        </button>
      </div>
    </div>
  );
}
