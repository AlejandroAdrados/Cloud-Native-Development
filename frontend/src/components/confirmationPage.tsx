import React, { FormEvent, useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Button } from '@/components/base/Button';
import { Spinner } from './base/Spinner';

const Confirmationform = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [searchParams] = useSearchParams();

  const queryCode = searchParams.get('code');
  const queryUsername = searchParams.get('username');

  const confirm = async (uname: string, cod: string) => {
    const response = await fetch(
      import.meta.env.VITE_BACKEND_URL + '/auth/confirm',
      {
        method: 'POST',
        body: JSON.stringify({ code: cod, username: uname })
      }
    );
    if (!response.ok) {
      const body = await response.json();
      setError(body.error);
    } else {
      navigate('/login');
    }
  };
  const [username, setUsername] = useState(queryUsername ?? '');
  const [code, setCode] = useState(queryCode ?? '');

  const submit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    confirm(username, code);
  };

  useEffect(() => {
    if (queryUsername && queryCode) confirm(queryUsername, queryCode);
  }, []);

  return (
    <div className="bg-white p-10 rounded-md text-left">
      <img
        src="public/images/logo.png"
        alt="horse"
        width={100}
        height={100}
        className="mx-auto mb-6"
      />
      {queryUsername && queryCode && !error && (
        <div className="flex flex-col items-center mt-8">
          <div className="text-3xl font-bold">
            We are confirming your sign up
          </div>
          <Spinner />
        </div>
      )}
      {(error || !queryUsername || !queryCode) && (
        <form onSubmit={submit}>
          <label className="text-xl mt-8" htmlFor="username">
            Username
          </label>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="block border-2 border-gray-300 h-16 rounded-sm pl-2 pr-2 focus:outline-indigo-500 focus:ring-indigo-500 mb-6"
            type="text"
            placeholder="Username"
            required
            name="username"
          />
          <label className="text-xl" htmlFor="code">
            Code
          </label>
          <input
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="block border-2 border-gray-300 h-16 rounded-sm pl-2 pr-2 focus:outline-indigo-500 focus:ring-indigo-500 mb-6"
            type="text"
            placeholder="Code"
            required
            name="code"
          />
          {error && <div className="text-red-700 text-xl mb-6">{error}</div>}
          <Button type="submit" className="mx-auto mt-8">
            Confirm
          </Button>
        </form>
      )}
    </div>
  );
};

export default Confirmationform;
