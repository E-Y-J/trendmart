import { configureStore } from "@reduxjs/toolkit";
import themeReducer from './theme/themeSlice';
import authReducer from './auth/authButton/authSlice'

const store = configureStore({
  reducer: {
    theme: themeReducer,
    auth: authReducer,
  }
})

export default store;