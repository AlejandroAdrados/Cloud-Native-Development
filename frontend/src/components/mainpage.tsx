import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Mainpage = () => {
  const navigate = useNavigate();

  const submit = () => {
    navigate('/exercises');
  };
  const submit2 = () => {
    navigate('/profile');
  };

  const [title, setTitle] = useState('Main Page');
  useEffect(() => {
    document.title = title;
  }, [title]);

  const fetchData = async (token: string) => {
    await fetch(import.meta.env.VITE_BACKEND_URL + '/profile', {
      method: 'GET',
      headers: { Authorization: 'Bearer ' + token },
      mode: 'cors'
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data);
      });
  };

  const logout = () => {
    localStorage.setItem('LoginToken', '');
    navigate('/login');
  };

  useEffect(() => {
    const token = localStorage.getItem('LoginToken');
    if (token) {
      fetchData(token);
    }
  }, []);

  return (
    <div className="divWhite">
      <div className="messageAndLogOut">
        <button className="button" onClick={logout}>
          Log out
        </button>
      </div>
      <div className="photo">
        <img
          src="public/images/logo.png"
          alt="Image"
          width={100}
          height={100}
        />
      </div>
      <div className="messageAndLogOut">Hello User!</div>
      <div className="buttonContainer">
        <button className="button" onClick={submit}>
          Exercises
        </button>
        <button className="button" onClick={submit2}>
          Show past results
        </button>
      </div>
    </div>
  );
};

export default Mainpage;
