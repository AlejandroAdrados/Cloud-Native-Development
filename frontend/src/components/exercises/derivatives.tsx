import React, {
  ChangeEvent,
  FormEvent,
  MouseEvent,
  useEffect,
  useState
} from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/base/Button';
import { Spinner } from '@/components/base/Spinner';

function Derivatives() {
  const [loading, setLoading] = useState(true);
  const [solution, setSolution] = useState<number[]>([]);
  const [numbers, setNumbers] = useState<number[]>([]);
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
    await fetch(import.meta.env.VITE_BACKEND_URL + '/exercise?type=DERIV', {
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
        setSolution(data.Content.slice(0, -1).fill(0));

        console.log(data);
      });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(solution);

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
      setSolution([]);
      setLoading(true);
      setTimeout(async () => {
        await fetchData();
        setLoading(false);
      }, 1000);
    }
  };

  const updateSolution = (e: ChangeEvent<HTMLInputElement>, index: number) => {
    const copy = [...solution];
    copy[index] = Number.parseInt((e?.target as HTMLInputElement).value);
    setSolution(copy);
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
          {numbers.map((number, i, a) => (
            <span key={i}>
              {number}
              {i === a.length - 1 ? '' : 'x'}
              {i === a.length - 1 ? '' : <sup>{a.length - i - 1}</sup>}
              {i === a.length - 1 ? ' =' : ' + '}
            </span>
          ))}
          <div className="flex items-center justify-space-between mt-12">
            {solution.map((value, index, a) => {
              return (
                <div className="flex" key={index}>
                  <input
                    className="block border-2 border-gray-300 rounded-sm focus:outline-indigo-500 focus:ring-indigo-500 mb-6 w-20 h-8"
                    onChange={(e) => updateSolution(e, index)}
                    value={value}
                    type="number"
                    min={0}
                  />
                  <span>
                    {index === a.length - 1 ? '' : 'x'}
                    {index === a.length - 1 ? (
                      ''
                    ) : (
                      <sup>{a.length - index - 1}</sup>
                    )}
                    {index === a.length - 1 ? '' : ' + '}
                  </span>
                </div>
              );
            })}
          </div>
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

export default Derivatives;
