import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { JobDetailPage } from './components/JobDetailPage';
import { SearchPage } from './components/SearchPage';
import { HomePage } from './components/HomePage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/jobs/:jobId" element={<JobDetailPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;