export function Footer() {
  return (
    <div className="w-full py-4 bg-gray-50">
      <div className="flex justify-center space-x-4 text-sm text-gray-500">
        <a
          href="/about"
          className="hover:text-gray-700"
          target="_blank"
          rel="noopener noreferrer"
        >
          About
        </a>
        <span className="text-gray-300">|</span>
        <a
          href="https://realtechjobs.featurebase.app/"
          className="hover:text-gray-700"
          target="_blank"
          rel="noopener noreferrer"
        >
          Feedback
        </a>
      </div>
    </div>
  );
}
