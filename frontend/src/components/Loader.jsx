export default function Loader() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative w-20 h-20">
        <div className="absolute inset-0 border-4 border-green-200 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-green-600 rounded-full border-t-transparent animate-spin"></div>
        <div className="absolute inset-0 flex items-center justify-center text-2xl">🌿</div>
      </div>
      <p className="mt-4 text-green-700 font-medium animate-pulse">Analyzing your plant...</p>
      <p className="text-sm text-gray-500 mt-1">This may take a few seconds</p>
    </div>
  );
}