import React from 'react';
import { createBrowserRouter, redirect } from 'react-router-dom';
import Confirmationform from './components/confirmationPage';
import Exercises from './components/exercises';
import Loginform from './components/loginform';
import Mainpage from './components/mainpage';
import Registerform from './components/registerform';
import ShowPastResults from './components/showPastResults';
import Addition from './components/exercises/addition';
import Multiplication from './components/exercises/multiplication';
import Derivatives from './components/exercises/derivatives';

const guardLoader = async () => {
  const token = localStorage.getItem('LoginToken');
  if (!token) {
    return redirect('/login');
  }
  try {
    const jwt = JSON.parse(atob(token.split('.')[1]));

    const exp = jwt.exp;
    if (exp * 1000 <= Date.now() - 1000 * 60 * 5) {
      return redirect('/login');
    }
    return null;
  } catch (e) {
    return redirect('/login');
  }
};

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Mainpage />,
    loader: guardLoader
  },
  {
    path: '/register',
    element: <Registerform />
  },
  {
    path: '/login',
    element: <Loginform />
  },
  {
    path: '/confirm',
    element: <Confirmationform />
  },
  {
    path: '/profile',
    element: <ShowPastResults />,
    loader: guardLoader
  },
  {
    path: '/exercises',
    element: <Exercises />,
    loader: guardLoader
  },
  {
    path: '/main',
    element: <Mainpage />,
    loader: guardLoader
  },
  {
    path: '/exercises/addition',
    element: <Addition />,
    loader: guardLoader
  },
  {
    path: '/exercises/multiplication',
    element: <Multiplication />,
    loader: guardLoader
  },
  {
    path: '/exercises/derivatives',
    element: <Derivatives />,
    loader: guardLoader
  }
]);
