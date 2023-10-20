import React, { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/base/Button';

function Registerform() {
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [surname, setSurname] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const loginButton = () => {
    navigate('/login');
  };

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    setLoading(true);
    const response = await fetch(import.meta.env.VITE_BACKEND_URL + '/auth', {
      method: 'POST',
      body: formData
    });
    if (!response.ok) {
      const body = await response.json();
      setError(body.error);
    } else {
      navigate('/confirm');
    }
    setLoading(false);
  };

  return (
    <div className="bg-white p-6 rounded-md shadow text-left w-4/5 md:w-1/2 lg:w-1/3 my-4">
      <img
        src="public/images/logo.png"
        alt="logo"
        width={100}
        height={100}
        className="mx-auto mb-6"
      />
      <form onSubmit={onSubmit}>
        <label htmlFor="given_name" className="mt-6 text-xl">
          First name
        </label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="block border-2 border-gray-300 h-16 pl-4 pr-12 rounded-sm focus:outline-indigo-500 focus:ring-indigo-500 mb-6 w-full"
          type="text"
          placeholder="Name"
          name="given_name"
          required
        />
        <label htmlFor="family_name" className="text-xl">
          Family name
        </label>
        <input
          value={surname}
          onChange={(e) => setSurname(e.target.value)}
          className="block border-2 border-gray-300 h-16 rounded-sm pl-4 pr-12 focus:outline-indigo-500 focus:ring-indigo-500 mb-6 w-full"
          type="text"
          placeholder="Surname"
          name="family_name"
          required
        />
        <label htmlFor="email" className="text-xl">
          Email
        </label>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="block border-2 border-gray-300 h-16 rounded-sm pl-4 pr-12 focus:outline-indigo-500 focus:ring-indigo-500 mb-6 w-full"
          type="text"
          placeholder="Email"
          name="username"
          required
        />
        <label htmlFor="Password" className="text-xl">
          Password
        </label>
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="block border-2 border-gray-300 h-16 rounded-sm pl-4 pr-12 focus:outline-indigo-500 focus:ring-indigo-500 mb-6 w-full"
          type="password"
          placeholder="Password"
          name="password"
          required
        />
        <label htmlFor="profile_picture" className="text-xl">
          Profile Picture
        </label>
        <div className="upload-image">
          <input className="mb-6" type="file" name="profile_picture" />
        </div>
        {error && <div className="text-red-700 text-2xl">{error}</div>}
        <Button
          className="mt-4 mx-auto"
          type="submit"
          loading={loading}
          disabled={loading}
        >
          Register
        </Button>
      </form>
      <button onClick={loginButton} className="register-text mx-auto block">
        Do you have an account? Login here!
      </button>
    </div>
  );
}

export default Registerform;
