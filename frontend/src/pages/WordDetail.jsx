import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { getWord, getNotes, updateNotes, toggleFavorite } from '../api/words'
import { useMutation, useQueryClient } from '@tanstack/react-query'

const WordDetail = () => {
  const { id } = useParams()
  const queryClient = useQueryClient()

  const { data: word, isLoading } = useQuery({
    queryKey: ['word', id],
    queryFn: () => getWord(id),
  })

  const { data: notes } = useQuery({
    queryKey: ['notes', id],
    queryFn: () => getNotes(id),
  })

  const [editing, setEditing] = useState(false)
  const [customMeaning, setCustomMeaning] = useState('')
  const [customSentence1, setCustomSentence1] = useState('')
  const [customSentence2, setCustomSentence2] = useState('')

  const notesMutation = useMutation({
    mutationFn: (data) => updateNotes(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notes', id] })
      setEditing(false)
    },
  })

  const favoriteMutation = useMutation({
    mutationFn: toggleFavorite,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['word', id] })
      queryClient.invalidateQueries({ queryKey: ['words'] })
    },
  })

  const handleSaveNotes = () => {
    notesMutation.mutate({
      custom_meaning: customMeaning,
      custom_sentence_1: customSentence1,
      custom_sentence_2: customSentence2,
    })
  }

  const handleToggleFavorite = () => {
    favoriteMutation.mutate(id)
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-600">Loading word...</div>
      </div>
    )
  }

  if (!word) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-red-600">Word not found</div>
      </div>
    )
  }

  const displayMeaning = notes?.custom_meaning || word.meaning
  const displaySentence1 = notes?.custom_sentence_1 || word.example_sentence_1
  const displaySentence2 = notes?.custom_sentence_2 || word.example_sentence_2

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex justify-between items-start mb-6">
          <h1 className="text-4xl font-bold text-gray-900">{word.word}</h1>
          <button
            onClick={handleToggleFavorite}
            className="text-3xl focus:outline-none"
            aria-label={word.is_favorite ? 'Remove from favorites' : 'Add to favorites'}
          >
            {word.is_favorite ? '❤️' : '🤍'}
          </button>
        </div>

        <div className="space-y-6">
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Meaning</h2>
            {editing ? (
              <textarea
                value={customMeaning}
                onChange={(e) => setCustomMeaning(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                rows="3"
                placeholder={word.meaning || 'Enter custom meaning...'}
              />
            ) : (
              <p className="text-gray-700 text-lg">{displayMeaning || 'No meaning available'}</p>
            )}
          </div>

          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Example Sentences</h2>
            {editing ? (
              <div className="space-y-3">
                <textarea
                  value={customSentence1}
                  onChange={(e) => setCustomSentence1(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  rows="2"
                  placeholder={word.example_sentence_1 || 'Enter first example sentence...'}
                />
                <textarea
                  value={customSentence2}
                  onChange={(e) => setCustomSentence2(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  rows="2"
                  placeholder={word.example_sentence_2 || 'Enter second example sentence...'}
                />
              </div>
            ) : (
              <div className="space-y-3">
                <p className="text-gray-700">
                  <span className="font-medium">1.</span> {displaySentence1 || 'No example available'}
                </p>
                <p className="text-gray-700">
                  <span className="font-medium">2.</span> {displaySentence2 || 'No example available'}
                </p>
              </div>
            )}
          </div>

          <div className="flex gap-3">
            {editing ? (
              <>
                <button
                  onClick={handleSaveNotes}
                  disabled={notesMutation.isPending}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
                >
                  {notesMutation.isPending ? 'Saving...' : 'Save Notes'}
                </button>
                <button
                  onClick={() => {
                    setEditing(false)
                    setCustomMeaning(notes?.custom_meaning || '')
                    setCustomSentence1(notes?.custom_sentence_1 || '')
                    setCustomSentence2(notes?.custom_sentence_2 || '')
                  }}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
              </>
            ) : (
              <button
                onClick={() => {
                  setEditing(true)
                  setCustomMeaning(notes?.custom_meaning || '')
                  setCustomSentence1(notes?.custom_sentence_1 || '')
                  setCustomSentence2(notes?.custom_sentence_2 || '')
                }}
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                Edit Notes
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default WordDetail
