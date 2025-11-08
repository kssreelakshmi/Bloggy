import { configureStore } from '@reduxjs/toolkit'
import userSliceReducer from './userSlice'

export const userStore = configureStore({
  reducer: {
    user_authentication : userSliceReducer,
  },
})