import React, { useState } from 'react';
import { api } from '@/lib/api';

interface AddTodoFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

export const AddTodoForm: React.FC<AddTodoFormProps> = ({ onSuccess, onCancel }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    setError('');

    try {
      const res = await api.fetch('/api/todos', {
        method: 'POST',
        body: JSON.stringify({ title, description }),
      });

      if (res.ok) {
        setTitle('');
        setDescription('');
        onSuccess();
      } else {
        setError('Failed to create todo');
      }
    } catch (e) {
      console.error("Error adding todo:", e);
      setError('An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-8 rounded-2xl shadow-xl border border-slate-200 mb-10 relative overflow-hidden">
      
      <div className="flex justify-between items-center mb-6 relative z-10">
        <h3 className="text-xl font-bold text-slate-800">Create New Task</h3>
      </div>
      
      {error && <div className="text-rose-600 mb-6 text-sm bg-rose-500/10 p-3 rounded-lg border border-rose-500/20 font-bold">{error}</div>}
      
      <div className="mb-5 relative z-10">
        <label htmlFor="title" className="block text-xs font-bold text-slate-600 mb-2 uppercase tracking-widest">Title</label>
        <input
          type="text"
          id="title"
          className="block w-full bg-slate-100 backdrop-blur-md border border-slate-200 rounded-xl p-4 text-lg font-bold text-slate-800 placeholder-slate-400 focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all outline-none"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          autoFocus
          placeholder="What needs to be done?"
        />
      </div>
      
      <div className="mb-8 relative z-10">
        <label htmlFor="description" className="block text-xs font-bold text-slate-600 mb-2 uppercase tracking-widest">Description (Optional)</label>
        <textarea
          id="description"
          rows={3}
          className="block w-full bg-slate-100 backdrop-blur-md border border-slate-200 rounded-xl p-4 text-base font-medium text-slate-800 placeholder-slate-400 focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all outline-none resize-none"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add more details..."
        />
      </div>
      
      <div className="flex justify-end space-x-4 relative z-10">
        <button
          type="button"
          onClick={onCancel}
          className="px-6 py-2.5 border border-slate-300 rounded-xl text-sm font-bold text-slate-600 hover:bg-slate-100 hover:text-slate-800 transition-all"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="inline-flex justify-center items-center px-8 py-2.5 border border-transparent shadow-lg shadow-emerald-500/20 text-sm font-black rounded-xl text-white bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-500 hover:to-green-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-70 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95"
        >
          {loading ? 'Adding...' : 'Add Task'}
        </button>
      </div>
    </form>
  );
};
