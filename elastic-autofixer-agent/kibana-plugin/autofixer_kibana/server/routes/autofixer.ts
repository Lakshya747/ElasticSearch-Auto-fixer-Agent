import { IRouter } from 'kibana/server';
import axios from 'axios';

// Python Backend URL
const PYTHON_BACKEND_URL = 'http://127.0.0.1:8000/api/v1';

export function registerAutofixerRoutes(router: IRouter) {
  
  // 1. Diagnostics Route
  router.get(
    {
      path: '/api/autofixer/diagnose',
      validate: false,
    },
    async (context, request, response) => {
      try {
        const res = await axios.get(`${PYTHON_BACKEND_URL}/diagnose`);
        return response.ok({ body: res.data });
      } catch (err) {
        return response.customError({ statusCode: 502, body: 'Python Backend Unavailable' });
      }
    }
  );

  // 2. Generate Fix Route
  router.post(
    {
      path: '/api/autofixer/generate_fix',
      validate: false,
    },
    async (context, request, response) => {
      try {
        const res = await axios.post(`${PYTHON_BACKEND_URL}/generate-fix`, request.body);
        return response.ok({ body: res.data });
      } catch (err) {
        return response.customError({ statusCode: 500, body: 'Fix Generation Failed' });
      }
    }
  );

  // 3. Apply Fix Route
  router.post(
    {
      path: '/api/autofixer/apply_fix',
      validate: false,
    },
    async (context, request, response) => {
      try {
        const res = await axios.post(`${PYTHON_BACKEND_URL}/apply-fix`, request.body);
        return response.ok({ body: res.data });
      } catch (err) {
        return response.customError({ statusCode: 500, body: 'Apply Fix Failed' });
      }
    }
  );
  
  // 4. Benchmark Route
  router.post(
    {
      path: '/api/autofixer/benchmark',
      validate: false,
    },
    async (context, request, response) => {
      try {
        const res = await axios.post(`${PYTHON_BACKEND_URL}/benchmark`, request.body);
        return response.ok({ body: res.data });
      } catch (err) {
        return response.customError({ statusCode: 500, body: 'Benchmark Failed' });
      }
    }
  );
}