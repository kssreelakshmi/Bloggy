import {createSlice} from '@reduxjs/toolkit';

const initialState = {
    name: null,
    avatar : null,
    isAuthenticated: false, 
    isAdmin: false,name: null
}

const userSlice = createSlice({
    name:'user_authentication',
    initialState,
    reducers:{
        set_user_authentication: (state, action) => {
        state.name = action.payload.name
        state.avatar = action.payload.avatar
        state.isAuthenticated = action.payload.isAuthenticated;
        state.isAdmin = action.payload.isAdmin;
        },
    }
})

export const { set_user_authentication } = userSlice.actions
export default userSlice.reducer