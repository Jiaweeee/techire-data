import { Logo } from './Logo';
import { Mail, Twitter } from 'lucide-react';

export function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <Logo />
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto pb-16">
        <div className="p-8 space-y-8">
          {/* Mission Section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-900">Motivation</h2>
            <p className="text-gray-600 leading-relaxed">
              We believe finding the right tech job shouldn't involve sifting through outdated listings or dealing with third-party recruiters. RealTechJobs was built to provide tech professionals with direct access to fresh job opportunities, straight from official company career pages.
            </p>
          </section>

          {/* Why RealTechJobs Section */}
          <section className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Why RealTechJobs?</h2>
            <div className="grid gap-6">
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                  💡 Direct Source
                </h3>
                <p className="text-gray-600">
                  Unlike traditional job boards, we collect job listings directly from company career pages, ensuring you get accurate, up-to-date information without any middlemen.
                </p>
              </div>

              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                  🔍 Tech-Focused
                </h3>
                <p className="text-gray-600">
                  We specialize exclusively in technology roles, making it easier for tech professionals to find relevant opportunities without the noise of unrelated listings.
                </p>
              </div>

              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                  ⚡ Always Fresh
                </h3>
                <p className="text-gray-600">
                  Our automated systems continuously monitor company career pages, ensuring job listings are current and removing expired positions automatically.
                </p>
              </div>

              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                  🎯 Smart Analysis
                </h3>
                <p className="text-gray-600">
                  We use advanced AI to analyze each job posting, extracting key information like:
                </p>
                <ul className="list-disc pl-5 text-gray-600 space-y-1">
                  <li>Required skills and experience levels</li>
                  <li>Salary ranges (when available)</li>
                  <li>Remote work options</li>
                  <li>Employment types</li>
                </ul>
              </div>
            </div>
          </section>

          {/* How It Works Section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-900">How It Works</h2>
            <ol className="list-decimal pl-5 space-y-2 text-gray-600">
              <li>We continuously monitor official career pages of leading tech companies</li>
              <li>New job postings are automatically collected and analyzed</li>
              <li>Our AI processes each listing to extract relevant details</li>
              <li>Jobs are indexed and made searchable in real-time</li>
              <li>Expired listings are automatically removed</li>
            </ol>
          </section>

          {/* Future Plans Section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-900">Future Plans</h2>
            <p className="text-gray-600">We're constantly working to improve RealTechJobs. Our upcoming features include:</p>
            <ul className="list-disc pl-5 text-gray-600 space-y-1">
              <li>More company integrations</li>
              <li>Personalized job alerts</li>
              <li>Advanced filtering options</li>
              <li>Salary insights and trends</li>
            </ul>
          </section>

          {/* Contact Section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-900">Get in Touch</h2>
            <p className="text-gray-600">Have suggestions or want to report an issue? We'd love to hear from you:</p>
            <div className="flex flex-col gap-3">
              <a href="mailto:your@email.com" className="flex items-center gap-2 text-gray-600 hover:text-gray-900">
                <Mail className="w-5 h-5" />
                <span>your@email.com</span>
              </a>
              <a href="https://twitter.com/yourhandle" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-gray-600 hover:text-gray-900">
                <Twitter className="w-5 h-5" />
                <span>@YourHandle</span>
              </a>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
} 