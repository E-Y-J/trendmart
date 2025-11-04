import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../beConnection/api';

const initialState = {
  user: null,
  isAuthenticated: false,
  status: 'idle', // 'idle' | 'loading' | 'succeeded' | 'error'
  error: null,
};

export const createUser = createAsyncThunk(
  'auth/register',
  async ({ email, password }, { rejectWithValue }) => {
    try {
      const response = await api.post('auth/register', { email, password });

      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Async thunk for user login (backend sets the http-only cookie in response)
export const loginUser = createAsyncThunk(
  'auth/login',
  async ({ email, password }, { rejectWithValue }) => {
    try {
      const response = await api.post('/login', { email, password });

      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Async thunk to check auth status on app load or page refresh
export const checkAuthStatus = createAsyncThunk(
  'auth/protected',
  async (_, { rejectWithValue }) => {
    try {
      // Call a protected endpoint that requires the cookie
      const response = await api.get('/auth/protected');

      return response.data; // Should contain user details if authenticated
    } catch (error) {
      // If the call fails (e.g., 401), the cookie is invalid or missing
      return rejectWithValue(error.response.data);
    }
  }
);

// Async thunk for logging out (backend clears the cookie)
export const logoutUser = createAsyncThunk(
  'auth/logoutUser',
  async (_, { rejectWithValue }) => {
    try {
      // Backend response should clear the Set-Cookie header (e.g., set expiration to past)
      await api.post('/logout');

      return null;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(createUser.fulfilled, (state, action) => {
        state.isAuthenticated = true;
        state.user = action.payload;
        state.status = 'succeeded'
      })
      // Login reducers
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isAuthenticated = true;
        state.user = action.payload;
        state.status = 'succeeded';
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isAuthenticated = false;
        state.error = action.payload;
        state.status = 'error';
      })
      // Check status reducers
      .addCase(checkAuthStatus.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(checkAuthStatus.fulfilled, (state, action) => { 
        state.isAuthenticated = true;
        state.user = action.payload;
        state.status = 'succeeded';
      })
      .addCase(checkAuthStatus.rejected, (state) => {
        state.isAuthenticated = false;
        state.user = null;
        state.status = 'failed';
      })
      // Logout reducers
      .addCase(logoutUser.fulfilled, (state) => {
        state.isAuthenticated = false;
        state.user = null;
        state.status = 'idle';
      });
  },
});

export default authSlice.reducer;