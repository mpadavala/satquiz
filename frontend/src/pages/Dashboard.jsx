import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { getWords, toggleFavorite } from '../api/words'
import { useMutation, useQueryClient } from '@tanstack/react-query'

const Dashboard = () => {
  const queryClient = useQueryClient()

  const { data: words, isLoading, error } = useQuery({
    queryKey: ['words'],
    queryFn: () => getWords(),
  })

  const favoriteMutation = useMutation({
    mutationFn: toggleFavorite,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['words'] })
      queryClient.invalidateQueries({ queryKey: ['favorites'] })
    },
  })

  const handleToggleFavorite = (wordId) => {
    favoriteMutation.mutate(wordId)
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-600">Loading words...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-red-600">Error loading words</div>
      </div>
    )
  }

  return (
    <div className="px-4 py-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">SAT Vocabulary Words</h1>
        <p className="mt-2 text-gray-600">Browse and learn SAT vocabulary words</p>
      </div>

      {words && words.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No words found. Upload a PDF to get started!</p>
          <Link
            to="/upload"
            className="mt-4 inline-block px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Upload PDF
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {words?.map((word) => (
            <div
              key={word.id}
              className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start">
                <Link
                  to={`/word/${word.id}`}
                  className="flex-1"
                >
                  <h3 className="text-xl font-semibold text-gray-900 mb-2 hover:text-indigo-600">
                    {word.word}
                  </h3>
                </Link>
                <button
                  onClick={() => handleToggleFavorite(word.id)}
                  className="ml-2 text-2xl focus:outline-none"
                  aria-label={word.is_favorite ? 'Remove from favorites' : 'Add to favorites'}
                >
                  {word.is_favorite ? '❤️' : '🤍'}
                </button>
              </div>
              {word.meaning && (
                <p className="text-gray-600 text-sm mt-2 line-clamp-2">{word.meaning}</p>
              )}
              <Link
                to={`/word/${word.id}`}
                className="mt-4 inline-block text-indigo-600 text-sm hover:text-indigo-800"
              >
                View details →
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Dashboard
