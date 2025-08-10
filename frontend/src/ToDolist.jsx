import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';

const API_URL = 'http://127.0.0.1:8000'; 

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [newTask, setNewTask] = useState('');
  const [token, setToken] = useState(null);
  const auth = getAuth();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        const idToken = await user.getIdToken();
        setToken(idToken);
        fetchTodos(idToken);
      } else {
        setToken(null);
        setTodos([]);
      }
    });
    return () => unsubscribe();
  }, []);

  const fetchTodos = async (idToken) => {
    try {
      const response = await axios.get(`${API_URL}/tasks`, {
        headers: { Authorization: `Bearer ${idToken}` }
      });
      setTodos(response.data);
    } catch (error) {
      console.error("Error fetching todos:", error);
    }
  };

  const addTodo = async (e) => {
    e.preventDefault();
    if (!newTask) return;
    try {
      await axios.post(`${API_URL}/tasks`, {
        task: newTask,
        completed: false,
        timestamp: new Date().toISOString()
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setNewTask('');
      fetchTodos(token);
    } catch (error) {
      console.error("Error adding todo:", error);
    }
  };

  const toggleComplete = async (id, completed) => {
    try {
      await axios.patch(`${API_URL}/tasks/${id}`, { completed: !completed }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchTodos(token);
    } catch (error) {
      console.error("Error updating todo:", error);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await axios.delete(`${API_URL}/tasks/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchTodos(token);
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  };

  const handleLogout = () => {
    signOut(auth);
  };

  if (!token) return null;

  const formatDate = (isoString) => {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleString(); 
  };

  return (
    <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold mb-4 text-center">TASKS</h1>
      <button
        onClick={handleLogout}
        className="p-2 mb-4 bg-red-500 text-white rounded hover:bg-red-600 transition w-full"
      >
        Logout
      </button>

      <form onSubmit={addTodo} className="flex mb-4">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Add a new task"
          className="flex-grow p-2 border rounded-l-md"
        />
        <button type="submit" className="p-2 bg-green-500 text-white rounded-r-md hover:bg-green-600 transition">
          Add
        </button>
      </form>

      <ul>
        {todos.map(todo => (
          <li
            key={todo.id}
            className="flex items-start justify-between p-2 mb-2 bg-gray-100 rounded"
          >
            <div
              onClick={() => toggleComplete(todo.id, todo.completed)}
              className={`cursor-pointer flex flex-col ${todo.completed ? 'line-through text-gray-500' : ''}`}
            >
              <span>{todo.task}</span>
              {todo.timestamp && (
                <small className="text-xs text-gray-400">{formatDate(todo.timestamp)}</small>
              )}
            </div>
           <button
  onClick={() => deleteTodo(todo.id)}
  className="ml-2 text-red-600 hover:text-red-800 text-3xl font-extrabold leading-none"
  title="Delete task"
>
  ×
</button>

          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
