import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '@api/api';
import { setStatus } from '../status/statusSlice';

const initialState = {
  user: null,
  token: null,
  isAuthenticated: false,
  status: 'idle', // 'idle' | 'loading' | 'succeeded' | 'error'
  error: null,
};

export const createUser = createAsyncThunk(
  'auth/register',
  async ({ email, password }, { rejectWithValue, dispatch }) => {
    try {
      const response = await api.post('/auth/register', { email, password });

      dispatch(
        setStatus({
          message: 'Registration successful. You are now logged in.',
          variant: 'success',
        })
      );

      // Expect { user: {...} }
      return response.data.user;
    } catch (error) {
      dispatch(
        setStatus({
          message: error.response?.data?.message || 'Registration failed.',
          variant: 'error',
        })
      );
      return rejectWithValue(error.response?.data);
    }
  }
);

export const loginUser = createAsyncThunk(
  'auth/login',
  async ({ email, password }, { rejectWithValue, dispatch }) => {
    try {
      const response = await api.post('/auth/login', { email, password });

      dispatch(setStatus({ message: 'Login successful.', variant: 'success' }));

      // Expect { user: {...} }
      return response.data;
    } catch (error) {
      dispatch(
        setStatus({
          message:
            error.response?.data?.message || 'Login failed. Check credentials.',
          variant: 'error',
        })
      );
      return rejectWithValue(error.response?.data);
    }
  }
);

export const checkAuthStatus = createAsyncThunk(
  'auth/check',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/auth/protected');

      // Expect { user }
      return response.data.user;
    } catch (error) {
      return rejectWithValue(error.response?.data);
    }
  }
);

export const logoutUser = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue, dispatch }) => {
    try {
      await api.post('/auth/logout');
      dispatch(
        setStatus({
          message: "Logged out successfully. We'll see you next time!",
          variant: 'info',
        })
      );
      return null;
    } catch (error) {
      dispatch(
        setStatus({
          message: error.response?.data?.message || 'Logout failed.',
          variant: 'error',
        })
      );
      return rejectWithValue(error.response?.data);
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    initializeAuth: (state) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        state.token = token;
        state.isAuthenticated = true;
        state.status = 'succeeded';
        // Note: user will be set when checkAuthStatus is called
      }
    },
    clearAuth: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
      state.status = 'idle';
      state.error = null;
      localStorage.removeItem('access_token');
    },
  },
  extraReducers: (builder) => {
    builder
      // LOGIN
      .addCase(loginUser.fulfilled, (state, action) => {
        console.log('🚀 loginUser.fulfilled action.payload:', action.payload);
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.access_token;
        state.status = 'succeeded';
        // Store token in localStorage
        localStorage.setItem('access_token', action.payload.access_token);
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isAuthenticated = false;
        state.user = null;
        state.error = action.payload;
        state.token = null;
        state.status = 'error';
      })

      // REGISTER
      .addCase(createUser.fulfilled, (state, action) => {
        state.isAuthenticated = true;
        state.user = action.payload;
        state.status = 'succeeded';
      })
      .addCase(createUser.rejected, (state, action) => {
        state.isAuthenticated = false;
        state.user = null;
        state.error = action.payload;
        state.status = 'error';
      })

      // CHECK SESSION
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
        state.status = 'error';
      })

      // LOGOUT
      .addCase(logoutUser.fulfilled, (state) => {
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
        state.status = 'idle';
        // Remove token from localStorage
        localStorage.removeItem('access_token');
      });
  },
});

export const { initializeAuth, clearAuth } = authSlice.actions;
export default authSlice.reducer;
