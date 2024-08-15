import React, { useState, useEffect } from 'react';
import api from './AxiosClient';

const AuthContext = React.createContext({
    isLoggedIn: true,
    isCCSMember: false,
    login: (data) => { },
    logout: () => { },
    user: {},
});

export const AuthContextProvider = (props) => {
    const [userIsLoggedIn, setUserIsLoggedIn] = useState(false);
    const [userIsCCSMember, setUserIsCCSMember] = useState(false);
    const [user, setUser] = useState({});
    const [isAuthChecked, setIsAuthChecked] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            api.get('auth/user/').then(response => {
                setUserIsLoggedIn(true);
                setUserIsCCSMember(response.is_member);
                setUser(response);
            }).catch(error => {
                setUserIsLoggedIn(false);
                setUserIsCCSMember(false);
                setUser({});
            }).finally(() => {
                setIsAuthChecked(true);
            });
        } else {
            setIsAuthChecked(true);
        }
    }, []);

    const loginHandler = (data) => {
        const { token, user } = data;
        localStorage.setItem('token', token);
        setUserIsLoggedIn(true);
        setUserIsCCSMember(user.is_member);
        setUser(user);
    };

    const logoutHandler = () => {
        localStorage.removeItem('token');
        setUserIsLoggedIn(false);
        setUserIsCCSMember(false);
        setUser({});
    };

    const contextValue = {
        isLoggedIn: userIsLoggedIn,
        isCCSMember: userIsCCSMember,
        login: loginHandler,
        logout: logoutHandler,
        isAuthChecked: isAuthChecked,
        user: user,
    };

    return <AuthContext.Provider value={contextValue}>{props.children}</AuthContext.Provider>;
};

export default AuthContext;
