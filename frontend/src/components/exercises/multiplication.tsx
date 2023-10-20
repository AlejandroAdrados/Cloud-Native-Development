import React, { FormEvent, MouseEvent, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/base/Button';
import { Spinner } from '@/components/base/Spinner';

function Multiplication() {
  const [loading, setLoading] = useState(true);
  const [solution, setSolution] = useState('');
  const [numbers, setNumbers] = useState([]);
  const [id, setId] = useState('');
  const [_type, setType] = useState('');
  const navigate = useNavigate();

  const backButton = (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    navigate('/exercises');
  };

  useEffect(() => {
    fetchData().then(() => setLoading(false));
  }, []);

  const fetchData = async () => {
    await fetch(import.meta.env.VITE_BACKEND_URL + '/exercise?type=MULT', {
      method: 'GET',
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('LoginToken')
      },
      mode: 'cors'
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setNumbers(data.Content);
        setId(data.Id);
        setType(data.Type);
        console.log(data);
      });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const response = await fetch(
      import.meta.env.VITE_BACKEND_URL + '/exercise/solution',
      {
        method: 'POST',
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('LoginToken')
        },
        mode: 'cors',
        body: JSON.stringify({
          assignmentId: id,
          assignmentType: _type,
          solution
        })
      }
    );
    if (!response.ok) {
      alert(`error with status ${response.status}`);
    } else {
      setSolution('');
      setLoading(true);
      setTimeout(async () => {
        await fetchData();
        setLoading(false);
      }, 1000);
    }
  };

  return (
    <div className="divWhite">
      {loading && (
        <div className="flex flex-col items-center">
          <div className="text-xl">Loading exercise</div>
          <Spinner />
        </div>
      )}
      {!loading && (
        <form onSubmit={handleSubmit}>
          <h2 className="title mb-10">EXERCISES</h2>
          {numbers.join(' * ') + ' ='}
          <input
            className="block border-2 border-gray-300 h-16 pl-4 pr-12 rounded-sm focus:outline-indigo-500 focus:ring-indigo-500 mb-6 w-full"
            type="text"
            onChange={(e) => setSolution(e.target.value)}
            value={solution}
          />
          <Button className="mx-auto mt-6" type="submit">
            Submit
          </Button>
          <div>
            <button
              className="register-text"
              style={{ fontSize: '25px', width: '100%' }}
              onClick={backButton}
            >
              Back
            </button>
          </div>
        </form>
      )}
    </div>
  );
}

export default Multiplication;
