import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { getFavorites, toggleFavorite } from '../api/words'
import { useMutation, useQueryClient } from '@tanstack/react-query'

const Favorites = () => {
  const queryClient = useQueryClient()

  const { data: favorites, isLoading, error } = useQuery({
    queryKey: ['favorites'],
    queryFn: getFavorites,
  })

  const favoriteMutation = useMutation({
    mutationFn: toggleFavorite,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['favorites'] })
      queryClient.invalidateQueries({ queryKey: ['words'] })
    },
  })

  const handleToggleFavorite = (wordId) => {
    favoriteMutation.mutate(wordId)
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-600">Loading favorites...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-red-600">Error loading favorites</div>
      </div>
    )
  }

  return (
    <div className="px-4 py-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Favorite Words</h1>
        <p className="mt-2 text-gray-600">Review your saved vocabulary words</p>
      </div>

      {favorites && favorites.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No favorite words yet. Start adding words to your favorites!</p>
          <Link
            to="/"
            className="mt-4 inline-block px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Browse Words
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {favorites?.map((word) => (
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
                  aria-label="Remove from favorites"
                >
                  ❤️
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

export default Favorites
