export function createApiClient(config) {
  const baseUrl = config.baseUrl || 'http://127.0.0.1:8000'
  const role = config.role || 'admin'
  const key = config.apiKey || ''

  async function request(path, options = {}) {
    const isFormData = options.body instanceof FormData
    const headers = {
      'X-Role': role,
      ...(key ? { 'X-API-Key': key } : {}),
      ...(options.headers || {})
    }
    if (!isFormData) {
      headers['Content-Type'] = 'application/json'
    }

    let response
    try {
      response = await fetch(`${baseUrl}${path}`, {
        ...options,
        headers
      })
    } catch (error) {
      const reason = error instanceof Error ? error.message : String(error)
      throw new Error(`Network error calling ${baseUrl}${path}: ${reason}`)
    }

    const text = await response.text()
    let payload = {}
    if (text) {
      try {
        payload = JSON.parse(text)
      } catch {
        payload = { detail: text }
      }
    }

    if (!response.ok) {
      const detail = payload?.detail || text || 'Unknown error'
      throw new Error(`HTTP ${response.status} - ${detail}`)
    }

    return payload
  }

  return {
    get: (path) => request(path, { method: 'GET' }),
    post: (path, body) => request(path, { method: 'POST', body: JSON.stringify(body) }),
    upload: (path, fieldName, file) => {
      const formData = new FormData()
      formData.append(fieldName, file)
      return request(path, { method: 'POST', body: formData })
    }
  }
}

export function pretty(value) {
  return JSON.stringify(value, null, 2)
}
