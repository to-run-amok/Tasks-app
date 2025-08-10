import React, { useState, useEffect } from 'react';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import AuthForm from './AuthForm';
import TodoList from './ToDolist';

const App = () => {
  const [user, setUser] = useState(null);
  const auth = getAuth();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (authUser) => {
      setUser(authUser);
    });
    return () => unsubscribe();
  }, []);

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gray-100 px-4">
      {user ? <TodoList /> : <AuthForm />}
    </div>
  );
};

export default App;
