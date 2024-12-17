import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import { JobDetailPage } from './components/JobDetailPage';
import { SearchPage } from './components/SearchPage';
import { HomePage } from './components/HomePage';
import { AboutPage } from './components/AboutPage';

function App() {
  return (
    <HelmetProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <main>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/jobs/:jobId" element={<JobDetailPage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </HelmetProvider>
  );
}

export default App;