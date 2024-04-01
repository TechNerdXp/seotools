import { BrowserRouter as Router, Routes,Route } from 'react-router-dom';
import Navbar from './Navbar';
import Home from './Home';
import Files from './Files';
import File from './File';
import Mapping from './Mapping';
import './App.css';

function App() {
  return (
    <div className="App">
      <Router>
        <Navbar />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/files" element={<Files />} />
          <Route path="/file" element={<File />} />
          <Route path="/mapping" element={<Mapping />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
