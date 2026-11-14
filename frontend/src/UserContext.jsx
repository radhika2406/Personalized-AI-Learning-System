
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";

import api from "./services/api";

const UserContext = createContext(null);

export function UserProvider({ children }) {
  const [account, setAccount] = useState(null);
  const [userLoading, setUserLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    if (!localStorage.getItem("token")) {
      setAccount(null);
      setUserLoading(false);
      return null;
    }

    try {
      const response = await api.get("/users/me");
      setAccount(response.data);
      return response.data;
    } catch (error) {
      setAccount(null);
      return null;
    } finally {
      setUserLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  return (
    <UserContext.Provider
      value={{ account, setAccount, refreshUser, userLoading }}
    >
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);

  if (!context) {
    throw new Error("useUser must be used inside UserProvider");
  }

  return context;
}
