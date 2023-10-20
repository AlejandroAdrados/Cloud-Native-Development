import React from 'react';
import { RouterProvider } from 'react-router-dom';
import './App.css';
import { router } from './router';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <RouterProvider router={router} />
      </header>
    </div>
  );
}

export default App;
