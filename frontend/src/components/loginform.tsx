import React, { FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/base/Button';

const Loginform = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const registerButton = () => {
    navigate('/register');
  };

  const submit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    const response = await fetch(
      import.meta.env.VITE_BACKEND_URL + '/auth/login',
      {
        method: 'POST',
        body: JSON.stringify({ username, password })
      }
    );
    if (!response.ok) {
      const body = await response.json();
      setError(body.error || 'Unkown error occured');
      setLoading(false);
      return;
    }

    const body = await response.json();
    setLoading(false);

    localStorage.setItem('LoginToken', body.AccessToken);
    navigate('/main');
  };

  return (
    <div className="bg-white p-10 rounded-md flex flex-col items-center justify-center">
      <img src="public/images/logo.png" alt="horse" width={100} height={100} />
      <form onSubmit={submit}>
        {error && <div className="text-red-500 text-base">{error}</div>}
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="block border-2 border-gray-300 h-16 rounded-sm pl-2 pr-2 focus:outline-indigo-500 focus:ring-indigo-500 mt-6 mb-6"
          type="text"
          placeholder="Email"
          required
        />
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="block border-2 border-gray-300 h-16 rounded-sm pl-2 pr-2 focus:outline-indigo-500 focus:ring-indigo-500 mb-6"
          type="password"
          placeholder="Password"
          required
        />
        <Button
          type="submit"
          className="mt-4 mx-auto"
          loading={loading}
          disabled={loading}
        >
          Login
        </Button>
      </form>
      <button onClick={registerButton} className="register-text">
        Don&apos;t you have an account? Register here!
      </button>
    </div>
  );
};

export default Loginform;
