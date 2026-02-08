import client from './client'

export const getWords = async (skip = 0, limit = 100) => {
  const response = await client.get('/words', {
    params: { skip, limit },
  })
  return response.data
}

export const getWord = async (id) => {
  const response = await client.get(`/words/${id}`)
  return response.data
}

export const toggleFavorite = async (wordId) => {
  const response = await client.post(`/favorite/${wordId}`)
  return response.data
}

export const getFavorites = async () => {
  const response = await client.get('/favorites')
  return response.data
}

export const uploadPDF = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await client.post('/upload-pdf', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const getNotes = async (wordId) => {
  const response = await client.get(`/notes/${wordId}`)
  return response.data
}

export const updateNotes = async (wordId, notes) => {
  const response = await client.put(`/notes/${wordId}`, notes)
  return response.data
}
