import client from './client'

export const getCurrentUser = async () => {
  const response = await client.get('/me')
  return response.data
}

// For development: simple email-based auth
// In production, this would use AWS Cognito
export const loginWithGoogle = async (email) => {
  // Mock login - in production, use Cognito
  localStorage.setItem('auth_token', email)
  return { email, name: email.split('@')[0] }
}

export const logout = () => {
  localStorage.removeItem('auth_token')
}
