import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Exercises() {
  const navigate = useNavigate();

  const backButton = () => {
    navigate('/main');
  };

  const additionButton = () => {
    navigate('/exercises/addition');
  };

  const multiplicationButton = () => {
    navigate('/exercises/multiplication');
  };

  const derivativesButton = () => {
    navigate('/exercises/derivatives');
  };

  return (
    <div className="divWhite">
      <h2 className="title mb-10">Which exercise do you want to solve?</h2>
      <div>
        <button className="button" onClick={additionButton}>
          ADDITION
        </button>
        <button className="button" onClick={multiplicationButton}>
          MULTIPLICATION
        </button>
        <button className="button" onClick={derivativesButton}>
          DERIVATIVES
        </button>
      </div>
      <div>
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

export default Exercises;
