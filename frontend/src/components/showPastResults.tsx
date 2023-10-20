import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Spinner } from './base/Spinner';

function showPastResults() {
  const navigate = useNavigate();
  const backButton = () => {
    navigate('/main');
  };

  const [title, setTitle] = useState('Show Past Results');
  const [loading, setLoading] = useState(true);
  const [profileUrl, setProfileUrl] = useState('');

  useEffect(() => {
    document.title = title;
  }, [title]);

  const [results, setResults] = useState({
    Results: {} as Record<string, Record<string, string | number>>
  });

  const typeMap = {
    ADD: 'Addition',
    MULT: 'Multiplication',
    DERIV: 'Derivatives'
  };

  const fetchData = async () => {
    await fetch(import.meta.env.VITE_BACKEND_URL + '/profile', {
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
        setResults(data);
        const profilePictureObject = data.UserData.find(
          (o: { Name: string; Value: string }) =>
            o.Name === 'custom:profile_picture'
        );
        if (profilePictureObject.Value !== 'null') {
          setProfileUrl(
            import.meta.env.VITE_S3_BUCKET_URL +
              '/' +
              profilePictureObject.Value
          );
        }
        //TODO When POST solution works, show the grades in screen
      });
  };

  useEffect(() => {
    //console.log(localStorage.getItem("LoginToken"));
    fetchData().then(() => setLoading(false));
  }, []);

  /*
  Maybe use this function to map the grades if needed
  function showGrades(grades) {
    if (Object.keys(results.Grades).length === 0) {
      return console.log("No hay Grades");
    }
    Object.entries(results.Grades).forEach(([key, value]) => {
      console.log(`${key}: ${value}`);
    });
  }*/

  return (
    <div className="w-3/4 md:w-1/2 lg:w-1/3 bg-white p-6">
      {profileUrl && (
        <img
          src={profileUrl}
          height={100}
          width={100}
          className="mx-auto mb-6"
        />
      )}
      <h2 className="text-bold text-3xl mb-8">Grades</h2>

      <div className="w-full">
        {!loading && Object.entries(results.Results).length != 0 && (
          <div className="flex items-center justify-between w-full">
            <table className="table-auto w-full border-collapse border border-slate-700">
              <thead>
                <tr>
                  <th className="border border-slate-300">Topic</th>
                  <th className="border border-slate-300">Grade</th>
                  <th className="border border-slate-300">Total solved</th>
                  <th className="border border-slate-300">Correctly solved</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(results.Results).map(([_type, result], i) => (
                  // <div key={i} className="text-center">
                  //   <span className="block">
                  //     {typeMap[_type as keyof typeof typeMap] ?? _type}
                  //   </span>
                  //   <span className="block">{result.grade}</span>
                  // </div>
                  <tr key={i}>
                    <th className="border border-slate-300">
                      {typeMap[_type as keyof typeof typeMap] ?? _type}
                    </th>
                    <td className="border border-slate-300">{result.grade}</td>
                    <td className="border border-slate-300">{result.total}</td>
                    <td className="border border-slate-300">
                      {result.correct}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {!loading && Object.entries(results.Results).length == 0 && (
          <div className="text-xl text-medium">No results yet.</div>
        )}
        {loading && (
          <div className="flex flex-col justify-center items-center">
            <span className="text-xl block mb-4">Loading results</span>
            <Spinner />
          </div>
        )}
        <button
          className="register-text"
          style={{ fontSize: '25px', width: '100%' }}
          onClick={backButton}
        >
          Back
        </button>
      </div>
    </div>
  );
}

export default showPastResults;
