import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Logo } from './components/Logo';
import { JobDetailPage } from './components/JobDetailPage';
import { SearchPage } from './components/SearchPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="container mx-auto px-4 py-4">
            <Logo />
          </div>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/jobs/:jobId" element={<JobDetailPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;